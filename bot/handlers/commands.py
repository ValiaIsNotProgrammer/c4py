from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ErrorEvent

from loguru import logger

from keyboards.keyboards import get_greeting_keyboard, get_screenshot_keyboard, get_group_link_detection_keyboard, get_admin_panel_keyboard
from utils.translate import get_answer
from utils.connector import api_connector
from utils.extra import get_valid_url, get_png_from
from .filters import URLFilter, URLGroupFilter, IsAdminFilter

router = Router(name=__name__)
last_message = None
last_message_url = None


@router.message(Command("start"))
async def start(msg: types.Message, language: str):
    "Функция для приветствия по команде /start"
    logger.info(f'Started bot with user: {msg.from_user.id}')
    await msg.answer(get_answer(language, "greeting"), reply_markup=get_greeting_keyboard(language))


@router.message(Command("admin"), IsAdminFilter())
async def start_admin(msg: types.Message, language: str):
    "Функция для приветствия по команде /admin"
    logger.info("Started bot with admin {}".format(msg.from_user.id))
    await msg.answer(get_answer(language, "admin_greeting"), reply_markup=get_admin_panel_keyboard(language))


@router.message(URLGroupFilter())
async def get_group_url(msg: types.Message, language: str):
    "Функция для определения в чате url"
    logger.info("Getting group url:", msg.text)
    global last_message_url
    last_message_url = msg.text
    await msg.answer(get_answer(language, "group_request_to_screenshot"),
                     reply_markup=get_group_link_detection_keyboard(language, msg.text))


@router.message(URLFilter())
async def get_screenshot(msg: types.Message, language: str, refresh_url: str = None, user_id: int = None):
    "Функция для создания скришота при получении URL"
    logger.info("Getting screenshot from {}".format(msg.from_user.id))
    user_id = user_id if user_id else msg.from_user.id
    r = await msg.answer(get_answer(language, "request_to_screenshot"), disable_web_page_preview=True)
    global last_message_url
    last_message_url = get_valid_url(refresh_url if refresh_url else msg.text)
    screenshot_model = await api_connector.create_screenshot(user_id, last_message_url, msg.message_id)
    screenshot_png = await get_png_from(screenshot_model)
    await msg.bot.delete_message(msg.chat.id, r.message_id)
    global last_message
    last_message = await msg.answer_photo(photo=screenshot_png,
                                          caption=get_answer(language, "screenshot_answer").format(last_message_url,
                                                                                                   screenshot_model.process_time),
                                          reply_markup=get_screenshot_keyboard(language, user_msg_id=user_id))


@router.error()
async def handle_error(event: ErrorEvent):
    "Функция для обработки ошибки, которые могут возникнуть при получении URL"
    logger.error("Error handling {}".format(event.exception))
    user_id = event.update.message.from_user.id
    language = await api_connector.get_language(user_id)
    await event.update.message.answer(get_answer(language, "error_url"))
    logger.warning("Error was handled with user id: {}".format(user_id))



