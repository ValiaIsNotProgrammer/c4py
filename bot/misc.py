from aiogram import Bot, Dispatcher
from loguru import logger

from config import BOT_TOKEN
from middlewares.create_user_middleware import CreateUserMiddleware
from middlewares.language_middleware import LanguageMiddleware
from handlers import commands
from handlers import keyboard_handlers


class BotSetup:
    """
    Класс для инициализации бота
    Все необходимые данные находяться в .env файле
    """
    def __init__(self, token):
        self.bot = Bot(token=token, parse_mode='HTML')
        self.dp = Dispatcher()
        self.is_setup = False

    def setup(self):
        "Метод для подключения маршрутов и middlewares"
        self.dp.include_router(commands.router)
        self.dp.include_router(keyboard_handlers.router)
        logger.info(f'Bot wag get routers: {self.dp.sub_routers}')
        self.dp.message.middleware(CreateUserMiddleware())
        self.dp.message.middleware(LanguageMiddleware())
        logger.info(f"Messages wag get middlewares: {self.dp.message.middleware.__dict__['_middlewares']}")
        self.dp.callback_query.middleware(LanguageMiddleware())
        logger.info(f"Callbacks was get middlewares: {self.dp.callback_query.middleware.__dict__['_middlewares']}")

    async def start(self):
        "Метод для запуска бота"
        if not self.is_setup:
            logger.info("Bot setup started")
            self.setup()
        logger.info("Starting bot")
        await self.dp.start_polling(self.bot)


bot = BotSetup(BOT_TOKEN)




