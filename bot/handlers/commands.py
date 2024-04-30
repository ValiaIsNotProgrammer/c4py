from typing import Union, Any

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.exceptions import AiogramError
from aiogram.types import ErrorEvent, InputMediaPhoto

from loguru import logger

from bot.keyboards.keyboards import get_greeting_keyboard, get_screenshot_keyboard, get_group_link_detection_keyboard
from bot.utils.translate import get_answers
from bot.utils.connector import api_connector
from bot.utils.extra import download_file, get_valid_url, get_png_from
from .filters import URLFilter, URLGroupFilter
from aiogram.dispatcher.dispatcher import Dispatcher

from ..model import Screenshot

router = Router(name=__name__)
last_message = None
last_message_url = None


@router.message(Command("start"))
async def start(msg: types.Message, language: str):
    logger.info(f'Started bot with user: {msg.from_user.id}')
    await msg.answer(get_answers(language, "greeting"), reply_markup=get_greeting_keyboard(language))


@router.message(URLGroupFilter())
async def get_group_url(msg: types.Message, language: str):
    logger.info("Getting group url:", msg.text)
    await msg.answer(get_answers(language, "group_request_to_screenshot"),
                     reply_markup=get_group_link_detection_keyboard(language, msg.text))


@router.message(URLFilter())
async def get_screenshot(msg: types.Message, language: str, refresh_url: str = None):
    logger.info("Getting screenshot from {}".format(msg.from_user.id))
    r = await msg.answer(get_answers(language, "request_to_screenshot"), disable_web_page_preview=True)
    global last_message_url
    last_message_url = get_valid_url(refresh_url if refresh_url else msg.text)
    screenshot_model, total_time = await api_connector.create_screenshot(msg.from_user.id, last_message_url, msg.message_id, get_time=True)
    screenshot_png = await get_png_from(screenshot_model)
    await msg.bot.delete_message(msg.chat.id, r.message_id)
    global last_message
    last_message = await msg.answer_photo(photo=screenshot_png,
                                          caption=get_answers(language, "screenshot_answer").format(last_message_url, total_time),
                                          reply_markup=get_screenshot_keyboard(language, user_msg_id=msg.message_id))


@router.error()
async def handle_error(event: ErrorEvent):
    logger.error("Error handling {}".format(event.exception))
    user_id = event.update.message.from_user.id
    language = await api_connector.get_language(user_id)
    await event.update.message.answer(get_answers(language, "error_url"))
    logger.warning("Error was handled with user id: {}".format(user_id))



