from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import BufferedInputFile
from time import time

from loguru import logger

from bot.keyboards.callbacks import InlineCallback
from bot.middlewares.create_user_middleware import CreateUserMiddleware
from bot.middlewares.language_middleware import LanguageMiddleware
from bot.keyboards.keyboards import get_greeting_keyboard, get_language_keyboard
from bot.utils.translate import get_answers
from bot.utils.connector import api_connector
from bot.utils.extra import get_language_from, download_file
from .filters import URLFilter
from ..misc import router


@router.message(Command("start"))
async def start(msg: types.Message, language: str):
    logger.info(f'Started bot with user: {msg.from_user.id}')
    await msg.answer(get_answers(language, "greeting"), reply_markup=get_greeting_keyboard(language))


@router.callback_query(InlineCallback.filter(F.button_name == "change_language_button"))
async def change_language_buttons(query: CallbackQuery, callback_data: InlineCallback, language: str):
    logger.info("Changing language buttons from", query.from_user.id)
    await query.message.delete_reply_markup(query.inline_message_id)
    await query.message.edit_text(text=get_answers(language, "change_language_text"), reply_markup=get_language_keyboard())


@router.callback_query(InlineCallback.filter(F.button_name == "add_to_chat_button"))
async def add_to_chat_buttons(query: CallbackQuery, callback_data: InlineCallback, language: str):
    logger.info("Adding chat buttons to from", query.from_user.id)
    await query.message.delete_reply_markup(query.inline_message_id)
    await query.message.edit_text(text=get_answers(language, "add_to_chat_text"))


@router.callback_query(InlineCallback.filter((F.button_name == "en_button") | (F.button_name == "ru_button")))
async def change_language(query: CallbackQuery, callback_data: InlineCallback, language: str):
    logger.info("Changing language to %s", language, "from", query.from_user.id)
    new_language = get_language_from(callback_data.button_name)
    await query.message.delete_reply_markup(query.inline_message_id)
    await api_connector.change_language(query.from_user.id, new_language)
    await query.message.delete()
    await start(query.message, new_language)


@router.message(URLFilter())
async def get_screenshot(msg: types.Message, language: str):
    logger.info("Getting screenshot from", msg.from_user.id)
    url = msg.text
    logger.trace(f"URL: {url}")
    start_time = time()
    screenshot_model = await api_connector.create_screenshot(msg.from_user.id, url)
    logger.trace(f"Screenshot model: {screenshot_model}")
    screenshot_bytes = await download_file(screenshot_model.image)
    screenshot_file = BufferedInputFile(screenshot_bytes, filename=f"{screenshot_model.image}.png")
    end_time = time() - start_time
    logger.success(f"Screenshot took {end_time}")
    requests_msg = await msg.answer(get_answers(language, "request_to_screenshot"))
    await msg.bot.delete_message(msg.chat.id, requests_msg.message_id)
    await msg.bot.send_photo(msg.chat.id, screenshot_file, caption=get_answers(language, "screenshot_answer").format(url, end_time))
