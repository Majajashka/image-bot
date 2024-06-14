import logging

from app.core.models.dto.user import User, UserActivity
from app.infrastructure.database.repo.user import UserRepo


async def get_or_create_user_by_id(user_id: int, repo: UserRepo):
    user = await repo.get_or_create_user(User(id=user_id))
    await repo.commit()
    return user


async def get_users_count_by_status(repo: UserRepo) -> UserActivity:
    active = await repo.get_users_count_by_status(status=True)
    inactive = await repo.get_users_count_by_status(status=False)
    return UserActivity(active=active, inactive=inactive)
