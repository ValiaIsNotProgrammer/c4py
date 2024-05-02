from typing import Optional


from aiogram.filters.callback_data import CallbackData


class InlineCallback(CallbackData, prefix="inline_callback"):
    """
    Класс для передачи метаданных для bot.handlers.keyboard_handlers

    :button_name - парамент который передается в аргумент callback_data
    :user_msg_id - опциональный аргумент, который используется для получения ссылки, с user.id
    Т.к. CallbackData позволяет сохраняться данные, длина которых < 64, передавать ссылку мы не можем

    """
    button_name: str
    user_msg_id: Optional[int] = None

