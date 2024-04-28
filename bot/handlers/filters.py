import re

from aiogram.filters import Filter
from aiogram.types import Message
from loguru import logger

class URLFilter(Filter):
    """
    Фильтр для отслеживания URL
    """

    def filter(self, text: str) -> bool:
        url_patterns = [
            "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
            "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)",
            "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        ]
        for url_pattern in url_patterns:
            if re.match(url_pattern, text):
                return True
        return False

    async def __call__(self, message: Message) -> bool:
        logger.info(f"Getting message from {message.from_user.id}, text {message.text}")
        return self.filter(message.text)
