from datetime import datetime
from dataclasses import dataclass

from app.core.models.dto.base import Base


class User(Base):
    id: int
    active: bool = None
    language: str = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class UserActivity(Base):
    """Сount of active and inactive users"""
    active: int
    inactive: int
