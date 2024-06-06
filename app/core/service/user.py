from sqlalchemy.exc import NoResultFound

from app.core.models.dto.user import User, UserActivity
from app.infrastructure.database.repo.user import UserRepo


async def create_user(user: User, repo: UserRepo) -> User:
    user = await repo.create_user(user)
    await repo.commit()
    return user


async def get_user_by_id(user_id: int, repo: UserRepo):
    try:
        user = await repo.get_by_id(user_id)
    except NoResultFound:
        user = None
    return user


async def get_users_count_by_status(repo: UserRepo) -> UserActivity:
    active = await repo.get_users_count_by_status(status=True)
    inactive = await repo.get_users_count_by_status(status=False)
    return UserActivity(active=active, inactive=inactive)
