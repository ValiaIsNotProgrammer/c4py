from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from loguru import logger

from utils.translate import get_answer
from .callbacks import InlineCallback


def get_greeting_keyboard(language: str) -> InlineKeyboardMarkup:
    "Функция для получения клавиатуры приветствия"
    inline_kb = InlineKeyboardBuilder()
    add_chat_button = InlineKeyboardButton(text=get_answer(language, "add_to_chat_button"),
                                           callback_data=InlineCallback(button_name="add_to_chat_button").pack(),
                                           url='https://t.me/truepositivetesttaskbot?startgroup=soulu')
    change_language_button = InlineKeyboardButton(text=get_answer(language, "change_language_button"),
                                                  callback_data=InlineCallback(button_name="change_language_button").pack())
    inline_kb.add(add_chat_button, change_language_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    "Функция для получения клавиатуры выбора языка"
    inline_kb = InlineKeyboardBuilder()
    ru_button = InlineKeyboardButton(text="Русский", callback_data=InlineCallback(button_name="ru_button").pack())
    en_button = InlineKeyboardButton(text="English", callback_data=InlineCallback(button_name="en_button").pack())
    inline_kb.add(ru_button, en_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_screenshot_keyboard(language: str, user_msg_id: int = None) -> InlineKeyboardMarkup:
    "Функция для получения информации по скриншоту"
    inline_kb = InlineKeyboardBuilder()
    refresh_button = InlineKeyboardButton(text=get_answer(language, "refresh_button"),
                                          callback_data=InlineCallback(button_name="refresh_button",
                                                                       user_msg_id=user_msg_id).pack())
    whois_button = InlineKeyboardButton(text=get_answer(language, "whois_button"),
                                        callback_data=InlineCallback(button_name="whois_button").pack())
    inline_kb.add(refresh_button, whois_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_group_link_detection_keyboard(language, url: str) -> InlineKeyboardMarkup:
    "Функция для получения клавиатуры после обнаружения ссылки в группе"
    inline_kb = InlineKeyboardBuilder()
    url = url.replace("https://", "www.")
    url_chat_button = InlineKeyboardButton(text=get_answer(language, "group_requests_to_screenshot_button"),
                                           callback_data=InlineCallback(button_name="gs_button").pack())
    inline_kb.add(url_chat_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_admin_panel_keyboard(language: str) -> InlineKeyboardMarkup:
    "Функция для получения клавиатуры администратора"
    inline_kb = InlineKeyboardBuilder()
    stats_button = InlineKeyboardButton(text=get_answer(language, "stats_button"),
                                        callback_data=InlineCallback(button_name="stats_button").pack())
    inline_kb.add(stats_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()