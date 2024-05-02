import json

from pydantic import BaseModel
from typing import Optional, Dict


class BotUser(BaseModel):
    """
    Класс BotUser для репрезентации json ответа c API
    """
    id: int
    language: str


class Screenshot(BaseModel):
    """
    Класс Screenshot для репрезентации json ответа c API
    """
    user_id: int
    image: str
    uploaded_at: Optional[str]
    url: str
    whois: Dict
    message_id: int
    process_time: float

    def __init__(self, **data):
        "Метод инициализации для переопределния входящих данных пользователя"
        data['whois'] = json.loads(data["whois"])
        if data.get("user", None):
            data["user_id"] = data["user"]
            del data["user"]
        super().__init__(**data)


class Stats(BaseModel):
    "Класс Stats для репрезентации json ответа c API"
    all_users_count: Optional[int]
    all_screenshots_count: Optional[int]
    average_process_time: Optional[float]
    average_len_screenshots_user: Optional[float]
    count_screenshots_on_day: Optional[int]

    def __init__(self, **data):
        "Метод инициализации для округления average_process_time"
        data["average_process_time"] = round(data["average_process_time"], 2)
        super().__init__(**data)

