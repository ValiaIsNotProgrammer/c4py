from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from bot.model import UserProfile


class LanguageMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        user_profile = UserProfile.objects.get(user_id=user_id)
        language = user_profile.language
        data['language'] = language

        return data

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        pass

