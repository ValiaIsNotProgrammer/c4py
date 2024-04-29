import re

from aiogram.filters import Filter
from aiogram.types import Message
from loguru import logger


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

