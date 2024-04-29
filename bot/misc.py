from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from bot.config import BOT_TOKEN
from bot.middlewares.create_user_middleware import CreateUserMiddleware
from bot.middlewares.language_middleware import LanguageMiddleware
from bot.handlers import commands
from bot.handlers import keyboard_handlers


class BotSetup:
    def __init__(self, token):
        self.bot = Bot(token=token, parse_mode='HTML')
        self.dp = Dispatcher()
        self.is_setup = False

    def setup(self):
        self.dp.include_router(commands.router)
        self.dp.include_router(keyboard_handlers.router)
        logger.info(f'Bot wag get routers: {self.dp.sub_routers}')
        self.dp.message.middleware(CreateUserMiddleware())
        self.dp.message.middleware(LanguageMiddleware())
        logger.info(f"Messages wag get middlewares: {self.dp.message.middleware.__dict__['_middlewares']}")
        self.dp.callback_query.middleware(LanguageMiddleware())
        logger.info(f"Callbacks was get middlewares: {self.dp.callback_query.middleware.__dict__['_middlewares']}")

    async def start(self):
        if not self.is_setup:
            logger.info("Bot setup started")
            self.setup()
        logger.info("Starting bot")
        await self.dp.start_polling(self.bot)


bot = BotSetup(BOT_TOKEN)




