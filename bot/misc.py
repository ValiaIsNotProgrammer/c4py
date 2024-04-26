from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=MemoryStorage())
