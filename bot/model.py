import json

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
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
    user: int
    image: str
    uploaded_at: Optional[datetime]
    url: str
    whois: Dict

    def __init__(self, **data):
        data['whois'] = json.loads(data["whois"])
        if data.get("user_id", None):
            data["user"] = data["user_id"]
            del data["user_id"]
        super().__init__(**data)
