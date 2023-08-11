from collections.abc import Callable
from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import Database


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    db: Database
    bot: Bot
