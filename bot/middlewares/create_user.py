from aiogram import types
from aiogram.client.session import aiohttp
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from bot.model import UserProfile


class CreateUserMiddleware(BaseMiddleware):
    def __init__(self, create_user_url):
        self.create_user_url = create_user_url

    async def on_process_message(self, message, data):
        async with aiohttp.ClientSession() as session:
            user_id = message.from_user.id
            async with session.get(f"{self.create_user_url}?user_id={user_id}") as response:
                if response.status == 404:
                    async with session.post(self.create_user_url, json={'user_id': user_id}) as response:
                        if response.status == 201:
                            print(f"User with id {user_id} created successfully")
                        else:
                            print(f"Failed to create user with id {user_id}")
        return data
