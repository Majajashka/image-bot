import os
from dataclasses import dataclass
from sqlalchemy.engine.url import URL

from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    user: str  # Username пользователя базы данных
    password: str  # Пароль к базе данных
    host: str  # URL-адрес базы данных
    port: str = None  # Порт базы данных

    def construct_sqlalchemy_url(self, driver="psycopg", host=None, port=None) -> str:
        if not host:
            host = self.host
        if not port:
            port = self.port
        url = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return url.render_as_string(hide_password=False)


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список айди админов


@dataclass
class RedisConfig:
    redis_host: str

    @property
    def url(self) -> str:
        return f"redis://{self.redis_host}/0"


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    redis: RedisConfig


def load_config_from_file(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            database=env('POSTGRES_DB'),
            host=env('POSTGRES_HOST'),
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            port=env('DB_PORT', None)),
        redis=RedisConfig(
            redis_host=env.str("REDIS_HOST", None)
        )
    )


def load_config_from_env() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_ids=list(map(int, os.getenv('ADMIN_IDS').split(',')))
        ),
        db=DatabaseConfig(
            database=os.getenv('POSTGRES_DB'),
            host=os.getenv('POSTGRES_HOST'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT', 5432)
        ),
        redis=RedisConfig(
            redis_host=os.getenv('REDIS_HOST')
        )
    )


if __name__ == '__main__':
    config = load_config_from_file()
    print('BOT_TOKEN:', config.tg_bot.token)
    print('ADMIN_IDS:', config.tg_bot.admin_ids)
    print()
    print('DATABASE:', config.db.database)
    print('DB_PORT', config.db.port)
    print('DB_HOST:', config.db.host)
    print('DB_USER:', config.db.user)
    print('DB_PASSWORD:', config.db.password)
    print('DB_URL:', config.db.construct_sqlalchemy_url())
    print()
    print(config.redis)
