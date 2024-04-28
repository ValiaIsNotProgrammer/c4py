from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BotUser(BaseModel):
    id: int
    language: str


class Screenshot(BaseModel):
    user_id: int
    image: str
    uploaded_at: Optional[datetime]
    url: str




