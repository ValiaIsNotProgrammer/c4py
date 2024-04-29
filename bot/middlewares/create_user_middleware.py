from typing import Callable, Dict, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from bot.model import BotUser
from bot.utils.connector import api_connector
from bot.config import DEFAULT_BOT_LANGUAGE

# TODO: оптимизировать запросы к БД через API (можно создать класс Repo или использовать кеш)

class CreateUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = data["event_context"].user_id
        logger.info(f"Middleware called from {user_id}. Starting requests to API")
        await self._create_user(user_id)

        return await handler(event, data)

    async def _create_user(self, user_id: int):
        user = BotUser(id=user_id, language=DEFAULT_BOT_LANGUAGE)
        logger.trace(f"Created user model {user}")
        await api_connector.create_user(user)


    def __str__(self):
        return "CreateUserMiddleware"

