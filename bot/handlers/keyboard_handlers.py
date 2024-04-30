from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from loguru import logger

from bot.handlers.commands import start, get_screenshot
from bot.keyboards.callbacks import InlineCallback
from bot.keyboards.keyboards import get_language_keyboard
from bot.utils.connector import api_connector
from bot.utils.extra import get_language_from
from bot.utils.translate import get_answers


router = Router(name=__name__)


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
    logger.info("Changing language to", language, "from", query.from_user.id)
    new_language = get_language_from(callback_data.button_name)
    await query.message.delete_reply_markup(query.inline_message_id)
    await api_connector.change_language(query.from_user.id, new_language)
    await query.message.delete()
    await start(query.message, new_language)


@router.callback_query(InlineCallback.filter(F.button_name == "gs_button"))  # gs: group_screenshot. Так как передавать можно небольшие данные (<64), то сокращаем
async def get_group_screenshot(query: CallbackQuery, callback_data: InlineCallback, language: str, refresh_url: str = None):
    logger.info("Getting group screenshot from", query.from_user.id)
    url = callback_data.url if callback_data.url or refresh_url is None else refresh_url
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await get_screenshot(query.message, language, refresh_url=url)


@router.callback_query(InlineCallback.filter(F.button_name == "whois_button"))
async def whois(query: CallbackQuery, callback_data: InlineCallback, language: str):
    logger.info("Getting whois from", query.from_user.id)
    from bot.handlers.commands import last_message_url
    whois = await api_connector.get_whois(last_message_url)
    text = f"""
    WHOIS
    {get_answers(language, "domain_name")}: {whois["domain_name"]}
    {get_answers(language, "registrar")}: {whois["registrar"]}
    {get_answers(language, "updated_date")}: {whois["updated_date"]}
    {get_answers(language, "country")}: {whois["country"]}
    """
    await query.answer(text, show_alert=True)


@router.callback_query(InlineCallback.filter(F.button_name == "refresh_button"))
async def refresh(query: CallbackQuery, callback_data: InlineCallback, language: str):
    logger.info("Refreshing screenshot from", query.from_user.id)
    from bot.handlers.commands import last_message, last_message_url
    await query.bot.delete_message(query.message.chat.id, last_message.message_id)
    await get_screenshot(query.message, language, refresh_url=last_message_url)