from aiogram import types, BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Message
from loguru import logger

from bot.utils.connector import api_connector


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = data["event_context"].user_id
        logger.info(f"Middleware called from {user_id}. Starting requests to API")
        lang = await api_connector.get_language(user_id)
        data["language"] = lang
        logger.success(f"Language for {user_id} was successful edited to {lang}")

        return await handler(event, data)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        pass

