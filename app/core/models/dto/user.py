from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from app.core.models.dto.base import Base


class User(Base):
    tg_id: int
    active: bool = None
    language: str = None
    created_at: datetime = None
    updated_at: datetime = None
    banned: bool = None
    binded_chat: Optional[int] = None

    def __str__(self):
        return f'ID: {self.tg_id}, Active: {self.active}, Language: {self.language}, Bind_chat: {self.bind_chat}'

    def __repr__(self):
        return (f"User(id={self.tg_id}, active={self.active}, language={self.language}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}, bind_chat={self.bind_chat})")


@dataclass
class UserActivity(Base):
    """Сount of active and inactive users"""
    active: int
    inactive: int
