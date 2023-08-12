from collections.abc import Callable
from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import Database


class TransferData(TypedDict):
    pool: Callable[[], AsyncSession]
    db: Database
