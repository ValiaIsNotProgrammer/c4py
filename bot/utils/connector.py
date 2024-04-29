from typing import Union, List

import aiohttp
from aiohttp import ClientResponse
from loguru import logger

from bot.config import BACKEND_URL
from bot.model import BotUser, Screenshot
from bot.config import DEFAULT_BOT_LANGUAGE


def log_request_data(func):
    async def wrapper(*args, **kwargs):
        endpoint = args[1]
        model = args[2] if len(args) > 2 else None
        data = kwargs.get('model') if kwargs.get('model') else {}

        logger.info(f"Calling {func.__name__} method with:")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Model: {model}")
        logger.info(f"Data: {data}")

        return await func(*args, **kwargs)

    return wrapper


class BaseConnector:

    def __init__(self, backend_url: str = BACKEND_URL):
        self.backend_url = backend_url
        self.model_endpoints = {
            "users": BotUser,
            "screenshots": Screenshot,
        }
        logger.info("Connector initialized. BackendUrl: {} Endpoints: {}".format(self.backend_url, self.model_endpoints))

    async def model_or_nan_from(self, response: ClientResponse) -> Union[BotUser, Screenshot, None]:

        endpoint = response.real_url.path.split("/")[1]
        logger.trace("Model response from endpoint: {}".format(endpoint))
        if response.status in [200, 201]:
            data = await response.json()
            logger.trace("Model response: {}".format(data))
            return self.model_endpoints[endpoint](**data)
        elif response.status == 400:
            logger.error("Model response from endpoint: {}, error: {}".format(endpoint, response.json()))
            return None
        else:
            logger.error("Model response from endpoint: {}, error: {}".format(endpoint, response.json()))
            raise ValueError(f'Unexpected response status {response.status}, reason: {response.reason}')

    async def models_or_nan_from(self, response: ClientResponse) -> Union[List[BotUser], List[BotUser], None]:
        endpoint = response.real_url.path.split("/")[1]
        logger.trace("Model response from endpoint: {}".format(endpoint))
        models = []
        if response.status in [200, 201]:
            data = await response.json()
            for model in data:
                logger.trace("Model response: {}".format(data))
                models.append(self.model_endpoints[endpoint](**model))
            return models
        elif response.status == 400:
            logger.error("Model response from endpoint: {}, error: {}".format(endpoint, response.json()))
            return None
        else:
            logger.error("Model response from endpoint: {}, error: {}".format(endpoint, response.json()))
            raise ValueError(f'Unexpected response status {response.status}, reason: {response.reason}')


    def get_full_url(self, url: str) -> str:
        full_url = f"{self.backend_url}{url}/"
        logger.trace("Full url: {}".format(full_url))
        return full_url

    @log_request_data
    async def get(self, endpoint: str, model: Union[BotUser, Screenshot] = None, is_list=False) -> Union[BotUser, Screenshot, None, List[BotUser], List[BotUser]]:
        params = self.get_dict_from(model) if model else {}
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            async with session.get(url, params=params) as response:
                if is_list:
                    return await self.models_or_nan_from(response)
                return await self.model_or_nan_from(response)

    @log_request_data
    async def post(self, endpoint: str, model: Union[BotUser, Screenshot]=None, **kwargs) -> Union[BotUser, Screenshot, None]:
        data = self.get_dict_from(model) if model else {}
        data = data | kwargs
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json', "accept": "application/json"}) as session:
            async with session.post(url, json=data) as response:
                return await self.model_or_nan_from(response)

    @log_request_data
    async def put(self, endpoint: str, model: Union[BotUser, Screenshot]) -> Union[BotUser, None]:
        data = self.get_dict_from(model)
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            async with session.put(url, json=data) as response:
                return await self.model_or_nan_from(response)

    @staticmethod
    def get_dict_from(model: Union[BotUser, Screenshot]) -> dict:
        return model.dict()


class APIConnector(BaseConnector):
    ENDPOINTS = {
        "user": "users",
        "get_user": "users/{}",
        "put_user": "users/{}",
        "screenshot": "screenshots",
        "get_screenshot": "screenshots/{}",
    }
    logger.info("Connector initialized. BackendUrl: {} Endpoints: {}".format(BACKEND_URL, ENDPOINTS))

    async def get_user(self, user_id: int) -> Union[BotUser, None]:
        endpoint = self.ENDPOINTS["get_user"].format(user_id)
        logger.info("Getting user: {}".format(endpoint))
        return await self.get(endpoint)

    async def create_user(self, user: BotUser) -> Union[BotUser, None]:
        logger.info("Creating user: {}".format(user))
        exist_user = await self.get_user(user.id)
        if exist_user:
            logger.success("User already exists. Returning user: {}".format(user))
            return exist_user
        endpoint = self.ENDPOINTS["user"]
        return await self.post(endpoint, model=user)

    async def update_user(self, user: BotUser) -> Union[BotUser, None]:
        endpoint = self.ENDPOINTS["user"]
        logger.info("Updating user: {}".format(user))
        return await self.put(endpoint, model=user)

    async def get_language(self, user_id: int) -> str:
        logger.info("Getting language: {}".format(user_id))
        user = await self.get_user(user_id)
        if user:
            logger.success("User exists. Returning language: {}".format(user.language))
            return user.language
        logger.warning("User does not exist. Returning language: {}".format(DEFAULT_BOT_LANGUAGE))
        return DEFAULT_BOT_LANGUAGE

    async def change_language(self, user_id: int, new_language: str):
        user = BotUser(id=user_id, language=new_language)
        endpoint = self.ENDPOINTS["put_user"].format(user_id)
        logger.info("Updating user language: {}".format(user_id))
        return await self.put(endpoint, model=user)

    async def get_screenshot(self, url: str) -> Screenshot:
        "UNUSED"
        # endpoint = self.ENDPOINTS["get_screenshot"].format(url)
        return await self.get(url)

    async def create_screenshot(self, user_id: int, url: str, full_url=True) -> Screenshot:
        logger.info("Creating screenshot: {}, user: {}".format(url, user_id))
        endpoint = self.ENDPOINTS["screenshot"]
        screenshot = await self.post(endpoint, id=user_id, url=url)
        if full_url:
            media_root = "media/"
            media_endpoint = media_root + screenshot.image
            screenshot.image = self.get_full_url(media_endpoint)
            logger.info("Full screenshot URL: {}".format(screenshot.image))
        return screenshot

    async def get_whois(self, url: str) -> Union[dict, None]:
        logger.info("Getting whois: {}".format(url))
        endpoint = self.ENDPOINTS["screenshot"]
        screenshots = await self.get(endpoint, is_list=True)
        return self.get_whois_from(screenshots, url)

    @staticmethod
    def get_whois_from(screenshots: List[Screenshot], url) -> Union[dict, None]:
        for screenshot in screenshots:
            if url == screenshot.url:
                return screenshot.whois
        raise KeyError("No whois found for url: {}".format(url))


api_connector = APIConnector()
