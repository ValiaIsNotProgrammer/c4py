from typing import Union, Any

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.exceptions import AiogramError
from aiogram.types import ErrorEvent

from loguru import logger

from bot.keyboards.keyboards import get_greeting_keyboard, get_screenshot_keyboard, get_group_link_detection_keyboard
from bot.utils.translate import get_answers
from bot.utils.connector import api_connector
from bot.utils.extra import download_file, get_valid_url, get_png_from
from .filters import URLFilter, URLGroupFilter
from aiogram.dispatcher.dispatcher import Dispatcher

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
    url = get_valid_url(refresh_url if refresh_url else msg.text)
    screenshot_model, total_time = await api_connector.create_screenshot(msg.from_user.id, url, get_time=True)
    screenshot_png = await get_png_from(screenshot_model)
    request_msg = await msg.answer(get_answers(language, "request_to_screenshot"))
    await msg.bot.delete_message(msg.chat.id, request_msg.message_id)
    global last_message
    last_message = await msg.bot.send_photo(msg.chat.id, screenshot_png,
                             caption=get_answers(language, "screenshot_answer").format(url, total_time),
                             reply_markup=get_screenshot_keyboard(language, screenshot_model))


@router.errors()
async def handle_my_custom_exception(ee: ErrorEvent) -> Any:
    logger.error(ee)
    # if "Resulted callback data is too long" in ee.exception:
    #     await ee.update.message.answer()
    await ee.update.message.answer(text="Something went wrong. Please try again later or change your URL")






