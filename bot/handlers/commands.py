from aiogram import types, Router
from aiogram.filters import Command

router = Router()
@router.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("Hello! I'm Asyncbot.")
