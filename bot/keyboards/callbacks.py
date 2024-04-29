from typing import Optional


from aiogram.filters.callback_data import CallbackData


class InlineCallback(CallbackData, prefix="inline_callback"):
    """
    Класс для передачи метаданных для bot.handlers.keyboard_handlers

    button_name - парамент который передается в аргумент callback_data
    url - парамент который позволяет передать прошлый использованный URL в аргумент callback_data (Предназначен для функциональности кнопки refresh)

    """
    button_name: str
    url: Optional[str] = None
    # last_msg_id: Optional[int] = None
