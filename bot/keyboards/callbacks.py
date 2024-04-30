from typing import Optional


from aiogram.filters.callback_data import CallbackData


class InlineCallback(CallbackData, prefix="inline_callback"):
    """
    Класс для передачи метаданных для bot.handlers.keyboard_handlers

    button_name - парамент который передается в аргумент callback_data
    last_msg_id - парамент, который позволяет сослаться на последнее сообщение связанное с конкретным URL

    """
    button_name: str
    user_msg_id: Optional[int] = None

