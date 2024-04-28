from aiogram.filters.callback_data import CallbackData


class InlineCallback(CallbackData, prefix="inline_callback"):
    button_name: str