from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from loguru import logger

from handlers.commands import start, get_screenshot
from keyboards.callbacks import InlineCallback
from keyboards.keyboards import get_language_keyboard
from utils.connector import api_connector
from utils.extra import get_language_from
from utils.translate import get_answer


router = Router(name=__name__)


@router.callback_query(InlineCallback.filter(F.button_name == "change_language_button"))
async def change_language_buttons(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки выбора языка"
    logger.info("Changing language buttons from", query.from_user.id)
    await query.message.delete_reply_markup(query.inline_message_id)
    await query.message.edit_text(text=get_answer(language, "change_language_text"), reply_markup=get_language_keyboard())


@router.callback_query(InlineCallback.filter(F.button_name == "add_to_chat_button"))
async def add_to_chat_buttons(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки добавления в час"
    logger.info("Adding chat buttons to from", query.from_user.id)
    await query.message.delete_reply_markup(query.inline_message_id)
    await query.message.edit_text(text=get_answer(language, "add_to_chat_text"))


@router.callback_query(InlineCallback.filter((F.button_name == "en_button") | (F.button_name == "ru_button")))
async def change_language(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки изменения языка"
    logger.info("Changing language to", language, "from", query.from_user.id)
    new_language = get_language_from(callback_data.button_name)
    await query.message.delete_reply_markup(query.inline_message_id)
    await api_connector.update_language(query.from_user.id, new_language)
    await query.message.delete()
    await start(query.message, new_language)


@router.callback_query(InlineCallback.filter(F.button_name == "gs_button"))  # gs: group_screenshot. Так как передавать можно небольшие данные (<64), то сокращаем
async def get_group_screenshot(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки, для получения скриншота в группе"
    logger.info("Getting group screenshot from", query.from_user.id)
    from handlers.commands import last_message_url
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    await get_screenshot(query.message, language, refresh_url=last_message_url, user_id=query.from_user.id)


@router.callback_query(InlineCallback.filter(F.button_name == "whois_button"))
async def whois(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки получения WHOIS"
    logger.info("Getting whois from", query.from_user.id)
    from handlers.commands import last_message_url
    whois = await api_connector.get_whois(last_message_url)
    text = f"""
    WHOIS
    {get_answer(language, "domain_name")}: {whois["domain_name"]}
    {get_answer(language, "registrar")}: {whois["registrar"]}
    {get_answer(language, "updated_date")}: {whois["updated_date"]}
    {get_answer(language, "country")}: {whois["country"]}
    """
    await query.answer(text, show_alert=True)


@router.callback_query(InlineCallback.filter(F.button_name == "refresh_button"))
async def refresh(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки для перезапуска скриншота"
    logger.info("Refreshing screenshot from", query.from_user.id)
    from handlers.commands import last_message, last_message_url
    await query.bot.delete_message(query.message.chat.id, last_message.message_id)
    logger.info(f"{query.from_user.id}: Refreshing screenshot from {last_message_url}")
    await get_screenshot(query.message, language, refresh_url=last_message_url, user_id=query.from_user.id)


@router.callback_query(InlineCallback.filter(F.button_name == "stats_button"))
async def stats(query: CallbackQuery, callback_data: InlineCallback, language: str):
    "Функция для обработки кнопки для статистики"
    logger.info("Getting stats from", query.from_user.id)
    await query.bot.delete_message(query.message.chat.id, query.message.message_id)
    stats = await api_connector.get_stats()
    stats_text = get_answer(language, "stats_text").format(*list(stats.dict().values()))
    await query.bot.send_message(query.message.chat.id, text=stats_text)