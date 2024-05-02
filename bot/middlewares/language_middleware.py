from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Message
from loguru import logger

from utils.connector import api_connector


# TODO: оптимизировать запросы к БД через API (можно создать класс Repo или использовать кеш)

class LanguageMiddleware(BaseMiddleware):
    """
    Middleware для получения языка пользователя
    По-умолчанию, если пользователь еще не создан, выберается язык DEFAULT_BOT_LANGUAGE
    Срабатывает перед всеми обработчиками
    """
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


    def __str__(self):
        return "LanguageMiddleware"

