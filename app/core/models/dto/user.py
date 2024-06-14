from datetime import datetime
from dataclasses import dataclass

from app.core.models.dto.base import Base


class User(Base):
    id: int
    active: bool = None
    language: str = None
    created_at: datetime = None
    updated_at: datetime = None

    def __str__(self):
        return f'ID: {self.id}, Active: {self.active}, Language: {self.language}'

    def __repr__(self):
        return (f"User(id={self.id}, active={self.active}, language={self.language}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")


@dataclass
class UserActivity(Base):
    """Сount of active and inactive users"""
    active: int
    inactive: int
