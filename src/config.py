from dataclasses import dataclass
from os import environ

from sqlalchemy import URL


@dataclass
class DatabaseConfig:
    name: str = environ.get("POSTGRES_DB", "")
    user: str = environ.get("POSTGRES_USER", "")
    password: str = environ.get("POSTGRES_PASSWORD", "")
    host: str = environ.get("POSTGRES_HOST", "")
    port: int = environ.get("POSTGRES_PORT", "5432")

    database_system: str = "postgresql"
    driver: str = "asyncpg"

    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    token: str = environ.get("TOKEN", "define me")
    admin_id: int = environ.get("ADMIN_ID", "0")
    kassir_link: str = "kassir.ru"


@dataclass
class Config:
    debug: bool = bool(environ.get("DEBUG", "").strip())
    db = DatabaseConfig()
    bot = BotConfig()


configure = Config()
