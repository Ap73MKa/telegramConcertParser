from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class DatabaseConfig:
    database: str | None = getenv("POSTGRES_DB")
    user: str | None = getenv("POSTGRES_USER")
    password: str | None = getenv("POSTGRES_PASSWORD")
    host: str = getenv("POSTGRES_HOST", "localhost")
    port: int = int(getenv('POSTGRES_PORT', "5432"))

    database_system: str = "postgresql"
    driver: str = "asyncpg"

    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.database,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    token: str = getenv("BOT_TOKEN", "")
    admin_id: int = int(getenv("ADMIN_ID", "0"))
    kassir_site: str = "kassir.ru"
    kassir_api: str = "https://api.kassir.ru/api/search"


@dataclass
class Config:
    debug: bool = bool(getenv("DEBUG", "").strip())
    db = DatabaseConfig()
    bot = BotConfig()


configure = Config()
