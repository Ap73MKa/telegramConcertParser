from os import environ


class Config:
    TOKEN: str = environ.get("TOKEN", "define me")
    ADMIN_ID: int = environ.get("ADMIN_ID", 0)
    KASSIR_SITE: str = "kassir.ru/bilety-na-koncert?"
    DATABASE: str = "database.db"
    BAN_WORDS: list[str] = [
        "оркестр",
        "фестиваль",
        "джаз",
        "сертификат",
        "ансамбль",
        "абонемент",
        "симфон",
        "диско",
        "скрипка",
        "орган",
        "jazz",
        "хор",
        "театр",
        "премия",
        "радио",
        "radio",
        "фестиваля",
    ]
