from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from loguru import logger

from bot.utils.translate import get_answers
from .callbacks import InlineCallback
from ..model import Screenshot

# TODO: решить проблему длины передаваемого URL в callback_data (<64)

def get_greeting_keyboard(language) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    add_chat_button = InlineKeyboardButton(text=get_answers(language, "add_to_chat_button"),
                                           callback_data=InlineCallback(button_name="add_to_chat_button").pack(),
                                           url='https://t.me/truepositivetesttaskbot?startgroup=soulu')
    change_language_button = InlineKeyboardButton(text=get_answers(language, "change_language_button"),
                                                  callback_data=InlineCallback(button_name="change_language_button").pack())
    inline_kb.add(add_chat_button, change_language_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    ru_button = InlineKeyboardButton(text="Русский", callback_data=InlineCallback(button_name="ru_button").pack())
    en_button = InlineKeyboardButton(text="English", callback_data=InlineCallback(button_name="en_button").pack())
    inline_kb.add(ru_button, en_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_screenshot_keyboard(language, screenshot_model: Screenshot, last_msg_id: int=None) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    refresh_button = InlineKeyboardButton(text=get_answers(language, "refresh_button"),
                                          callback_data=InlineCallback(button_name="refresh_button",
                                                                       url=screenshot_model.url.replace("https://", "www.")).pack())
    whois_button = InlineKeyboardButton(text=get_answers(language, "whois_button"),
                                        callback_data=InlineCallback(button_name="whois_button",
                                                                     url=screenshot_model.url.replace("https://", "www.")).pack())
    inline_kb.add(refresh_button, whois_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()


def get_group_link_detection_keyboard(language, url: str) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    url = url.replace("https://", "www.")
    url_chat_button = InlineKeyboardButton(text=get_answers(language, "group_requests_to_screenshot_button"),
                                        callback_data=InlineCallback(button_name="gs_button",
                                                                     url=url).pack())
    inline_kb.add(url_chat_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb.buttons))
    return inline_kb.as_markup()
