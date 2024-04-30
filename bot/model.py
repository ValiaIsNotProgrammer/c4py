import json

from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class BotUser(BaseModel):
    """
    Класс для репрезентации ответа User c API
    """
    id: int
    language: str


class Screenshot(BaseModel):
    """
    Класс для репрезентации ответа Screenshot c API
    """
    user_id: int
    image: str
    uploaded_at: Optional[str]
    url: str
    whois: Dict
    message_id: int

    def __init__(self, **data):
        data['whois'] = json.loads(data["whois"])
        if data.get("user", None):
            data["user_id"] = data["user"]
            del data["user"]
        super().__init__(**data)


a = ['user_id', 'image', 'uploaded_at', 'url', 'whois', 'message_id']
b = ['user_id', 'image', 'uploaded_at', 'url', 'whois', 'message_id']
print( a == b)