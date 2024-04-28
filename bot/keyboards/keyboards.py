from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from loguru import logger

from bot.utils.translate import get_answers
from .callbacks import InlineCallback


def get_greeting_keyboard(language) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    add_chat_button = InlineKeyboardButton(text=get_answers(language, "add_to_chat_button"),
                                           callback_data=InlineCallback(button_name="add_to_chat_button").pack())
    change_language_button = InlineKeyboardButton(text=get_answers(language, "change_language_button"),
                                                  callback_data=InlineCallback(button_name="change_language_button").pack())
    inline_kb.add(add_chat_button, change_language_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb))
    return inline_kb.as_markup()


def get_language_keyboard() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardBuilder()
    ru_button = InlineKeyboardButton(text="Русский", callback_data=InlineCallback(button_name="ru_button").pack())
    en_button = InlineKeyboardButton(text="English", callback_data=InlineCallback(button_name="en_button").pack())
    inline_kb.add(ru_button, en_button)
    inline_kb.adjust(repeat=True)
    logger.trace("Inline keyboard: {}".format(inline_kb))
    return inline_kb.as_markup()
