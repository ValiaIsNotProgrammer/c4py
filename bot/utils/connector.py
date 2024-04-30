from typing import Union, List

import aiohttp
from loguru import logger

from bot.config import BACKEND_URL
from bot.model import BotUser, Screenshot
from bot.config import DEFAULT_BOT_LANGUAGE
from bot.utils.extra import timer


def log_request_data(func):
    async def wrapper(*args, **kwargs):
        endpoint = args[1]
        model = kwargs

        logger.info(f"Calling {func.__name__} method with:")
        logger.info(f"Endpoint: {endpoint}")
        logger.info(f"Model: {model}")

        result = await func(*args, **kwargs)
        logger.info(f"Method {func.__name__} /{endpoint} return result: {result}")
        return result

    return wrapper


class BaseConnector:

    def __init__(self, backend_url: str = BACKEND_URL):
        self.backend_url = backend_url
        logger.info("Connector initialized. BackendUrl: {}".format(self.backend_url))

    @log_request_data
    async def get(self, endpoint: str, model: Union[BotUser, Screenshot] = None) -> dict:
        params = self.get_dict_from(model) if model else {}
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    @log_request_data
    async def post(self, endpoint: str, model: Union[BotUser, Screenshot] = None, **kwargs) -> dict:
        data = self.get_dict_from(model) if model else {}
        data = data | kwargs
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(
                headers={'Content-Type': 'application/json', "accept": "application/json"}) as session:
            async with session.post(url, json=data) as response:
                return await response.json()

    @log_request_data
    async def put(self, endpoint: str, model: Union[BotUser, Screenshot]) -> dict:
        data = self.get_dict_from(model)
        url = self.get_full_url(endpoint)
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            async with session.put(url, json=data) as response:
                return await response.json()

    def get_full_url(self, endpoint: str) -> str:
        full_url = f"{self.backend_url}{endpoint}/"
        logger.trace("Full url: {}".format(full_url))
        return full_url

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
    ENDPOINTS_MODELS = [BotUser, Screenshot]
    logger.info("Connector initialized. BackendUrl: {} Endpoints: {}".format(BACKEND_URL, ENDPOINTS))

    async def model_or_error_from(self, json: dict) -> Union[BotUser, Screenshot, None]:
        model = self.__get_model_from_data(json)
        if model:
            logger.info(f"Model: {model}")
            return model
        logger.error(f"Model response error {json}")
        raise ValueError(f'Unexpected response answer: {json}')

    async def models_or_error_from(self, json: dict) -> Union[List[BotUser], List[Screenshot], None]:
        models = []
        for model_dict in json:
            models.append(self.__get_model_from_data(model_dict))
        if models:
            logger.info(f"Models: {models}")
            return models
        logger.error(f"Models response error {json}")
        raise ValueError(f'Unexpected response answer: {json}')

    async def get_user(self, user_id: int) -> Union[BotUser, None]:
        endpoint = self.ENDPOINTS["get_user"].format(user_id)
        logger.info("Getting user: {}".format(endpoint))
        json = await self.get(endpoint)
        logger.success("User was get successfully")
        return await self.model_or_error_from(json)

    async def create_user(self, user: BotUser) -> Union[BotUser, None]:
        logger.info("Creating user: {}".format(user))
        try:
            exist_user = await self.get_user(user.id)
            if exist_user:
                logger.success("User already exists. Returning user: {}".format(user))
                return exist_user
        except ValueError:
            logger.warning("User does not exist. Creating user: {}".format(user))
        endpoint = self.ENDPOINTS["user"]
        json = await self.post(endpoint, model=user)
        logger.success("User was created successfully")
        return await self.model_or_error_from(json)

    async def update_user(self, user: BotUser) -> Union[BotUser, None]:
        endpoint = self.ENDPOINTS["user"]
        logger.info("Updating user: {}".format(user))
        json = await self.put(endpoint, model=user)
        logger.success("User was updated successfully")
        return await self.model_or_error_from(json)

    async def get_language(self, user_id: int) -> str:
        logger.info("Getting language: {}".format(user_id))
        user = await self.get_user(user_id)
        if user:
            logger.success("User exists. Returning language: {}".format(user.language))
            return user.language
        logger.warning("User does not exist. Returning default language: {}".format(DEFAULT_BOT_LANGUAGE))
        return DEFAULT_BOT_LANGUAGE

    async def change_language(self, user_id: int, new_language: str):
        user = BotUser(id=user_id, language=new_language)
        endpoint = self.ENDPOINTS["put_user"].format(user_id)
        logger.info("Updating user language: {}".format(user_id))
        user = await self.put(endpoint, model=user)
        logger.success("User language was updated successfully")
        return user

    async def get_screenshot_url_from_message_id(self, user_id: int, message_id: int) -> str:
        endpoint = self.ENDPOINTS["screenshot"]
        logger.info("Getting screenshot url from message id: {}".format(message_id))
        response = await self.get(endpoint)
        screenshots = await self.models_or_error_from(response)
        for screenshot in screenshots:
            if screenshot.message_id == message_id:
                return screenshot.url

    @timer
    async def create_screenshot(self, user_id: int, url: str, message_id: int, get_time=False) -> Union[Screenshot, dict]:
        logger.info("Creating screenshot: {}, user: {}".format(url, user_id))
        endpoint = self.ENDPOINTS["screenshot"]
        json = await self.post(endpoint, id=user_id, url=url, message_id=message_id)
        try:
            screenshot = await self.model_or_error_from(json)
        except ValueError as ex:
            logger.error(f"Screenshot response error {json}, error: {ex}")
            return json
        logger.success("Screenshot was created successfully {}".format(screenshot))
        return self.screenshot_with_full_url_field(screenshot)

    async def get_whois(self, url: str) -> Union[dict, None]:
        logger.info("Getting whois: {}".format(url))
        endpoint = self.ENDPOINTS["screenshot"]
        json = await self.get(endpoint)
        screenshots = await self.models_or_error_from(json)
        logger.success("Whois was retrieved successfully")
        return self.get_whois_from(screenshots, url)

    @staticmethod
    def get_whois_from(screenshots: List[Screenshot], url) -> Union[dict, None]:
        logger.info("Getting valid whois from screenshots: {}".format(screenshots))
        for screenshot in screenshots:
            if url == screenshot.url:
                logger.success("Whois was retrieved successfully")
                return screenshot.whois
        logger.warning("No valid whois was retrieved successfully")
        raise KeyError("No whois found for url: {}".format(url))

    def screenshot_with_full_url_field(self, screenshots: Screenshot) -> Screenshot:
        logger.info("Get image URL: {}".format(screenshots.image))
        screenshots.image = self.backend_url + screenshots.image[1:]
        logger.info("Edt image URL to: {}".format(screenshots.image))
        return screenshots

    def __get_model_from_data(self, json: dict) -> Union[BotUser, Screenshot, None]:
        for model in self.ENDPOINTS_MODELS:
            logger.trace(f"Added model {model}")
            try:
                m = model(**json)
                return m
            except Exception:
                pass
            logger.warning("Model fields do not match json fields: {}".format(json))


api_connector = APIConnector()
