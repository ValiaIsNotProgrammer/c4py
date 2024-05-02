import os
import re

from aiogram.filters import Filter
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger

from utils.connector import api_connector

load_dotenv()


def filter(text: str) -> bool:
    """
    Функция для поиска совпадения с url текстом. Вынесена в отдельную функцию из-за специфики метода object.__call__
    """
    if text is None:
        return False
    url_patterns = [
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)",
        "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
    ]
    for url_pattern in url_patterns:
        if re.match(url_pattern, text):
            return True
    return False


class URLFilter(Filter):
    """
    Фильтр для отслеживания URL
    """
    async def __call__(self, message: Message) -> bool:
        logger.info(f"Getting message from {message.from_user.id} chat type {message.chat.type}, text {message.text}")
        return filter(message.text)


class URLGroupFilter(Filter):
    """
    Фильтр для отслеживания URL в группах
    """
    async def __call__(self, message: Message) -> bool:
        logger.info(f"Getting message from {message.from_user.id} chat {message.chat.type}, text {message.text}")
        if message.chat.type == "group":
            return filter(message.text)


class IsAdminFilter(Filter):
    """
    Фильтр для определения админа по user id
    ВАЖНО: админ определеяется по id, которые указаны в BOT_ADMIMS_ID
    по-умолчания, если не указнны id, админом является первый созданный user
    """
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        logger.info("Getting request to admin panel from {}".format(user_id))
        if os.environ.get("bot_admims_id") is None:
            users = await api_connector.list_users()
            first_user = users[0]
            logger.warning("Id's for admin panel not found. Default admin is first user {}".format(first_user.id))
            if user_id == first_user.id:
                return True
        else:
            if str(user_id) in os.environ.get("bot_admims_id"):
                return True
        return False




