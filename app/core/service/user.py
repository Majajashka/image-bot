from sqlalchemy.exc import NoResultFound

from app.core.models.dto.user import User, UserActivity
from app.infrastructure.database.repo.user import UserRepo


async def get_or_create_user(tg_id: int, repo: UserRepo) -> User:
    try:
        user = await repo.get_user_by_id(user_id=tg_id)
    except NoResultFound:
        user = await repo.upsert_user(User(tg_id=tg_id))
    await repo.commit()
    return user


async def get_users_count_by_status(repo: UserRepo) -> UserActivity:
    active = await repo.get_users_count_by_status(status=True)
    inactive = await repo.get_users_count_by_status(status=False)
    return UserActivity(active=active, inactive=inactive)


async def bind_chat(user_id: int, chat_id: int, repo: UserRepo) -> User:
    try:
        user = await repo.bind_chat(user_id=user_id, chat_id=chat_id)
        await repo.commit()
    except NoResultFound:
        raise
    return user
