from abc import ABC
from typing import Final
from pathlib import Path


class PathControl(ABC):
    ROOT: Final = Path(__file__).resolve().parent.parent.parent

    @classmethod
    def get(cls, path: str) -> Path:
        return cls.ROOT.joinpath(path)
