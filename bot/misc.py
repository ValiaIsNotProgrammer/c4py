from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from bot.config import BOT_TOKEN
from bot.middlewares.create_user_middleware import CreateUserMiddleware
from bot.middlewares.language_middleware import LanguageMiddleware

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


router = Router()
router.message.middleware(CreateUserMiddleware())
router.message.middleware(LanguageMiddleware())
router.callback_query.middleware(LanguageMiddleware())
logger.info("Router was get middlewares")



