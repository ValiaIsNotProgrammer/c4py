from typing import Union

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from time import time


from loguru import logger

from bot.keyboards.keyboards import get_greeting_keyboard, get_screenshot_keyboard, get_group_link_detection_keyboard
from bot.utils.translate import get_answers
from bot.utils.connector import api_connector
from bot.utils.extra import download_file
from .filters import URLFilter, URLGroupFilter
# from ..misc import router

router = Router(name=__name__)
last_message: Union[types.Message, None] = None


@router.message(Command("start"))
async def start(msg: types.Message, language: str):
    logger.info(f'Started bot with user: {msg.from_user.id}')
    await msg.answer(get_answers(language, "greeting"), reply_markup=get_greeting_keyboard(language))


@router.message(URLGroupFilter())
async def get_group_url(msg: types.Message, language: str):
    logger.info("Getting group url:", msg.text)
    await msg.answer(get_answers(language, "group_request_to_screenshot"),
                     reply_markup=get_group_link_detection_keyboard(language, msg.text))


# TODO: сделать обработку ошибки неправильного URL с ответа API
# TODO: сделать обработчик URL, чтобы корректировать URL на стороне клиента, а не сервера
@router.message(URLFilter())
async def get_screenshot(msg: types.Message, language: str, refresh_url: str = None):
    logger.info("Getting screenshot from {}".format(msg.from_user.id))
    url = refresh_url if refresh_url else msg.text
    logger.trace(f"URL: {url}")
    start_time = time()
    screenshot_model = await api_connector.create_screenshot(msg.from_user.id, url)
    logger.trace(f"Screenshot model: {screenshot_model}")
    screenshot_bytes = await download_file(screenshot_model.image)
    screenshot_file = BufferedInputFile(screenshot_bytes, filename=f"{screenshot_model.image}.png")
    end_time = time() - start_time
    logger.success(f"Screenshot took {end_time}")
    requests_msg = await msg.answer(get_answers(language, "request_to_screenshot"))
    requests_msg_id = requests_msg.message_id
    await msg.bot.delete_message(msg.chat.id, requests_msg_id)
    global last_message
    last_message = await msg.bot.send_photo(msg.chat.id, screenshot_file,
                             caption=get_answers(language, "screenshot_answer").format(url, end_time),
                             reply_markup=get_screenshot_keyboard(language, screenshot_model))
                             # reply_to_message_id=msg.message_id)









