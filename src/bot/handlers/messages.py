from abc import ABC
from collections.abc import Sequence
from random import choices

from src.config import configure
from src.database.models import City, Concert


class Messages(ABC):
    @staticmethod
    def get_site_info() -> str:
        return (
            f"<b><a href='https://{configure.bot.kassir_link}'>Kassir</a></b> - сайт, на котором мы и узнаем "
            "все информацию o6 концертах. Если вам неудобен наш бот, то вы всегда можете узнать новую "
            "информацию на сайте 🤔"
        )

    @staticmethod
    def get_bot_info(cities: Sequence[City]) -> str:
        base = (
            "<b>tgConcerts</b> - это особый телеграм бот, который собирает информацию"
            " o всех концертах городов России специально для тебя! Чтобы запустить"
            " бота напиши <b>/start</b>\n\nHa данный момент доступны"
        )
        if not cities:
            return base
        count = len(cities)
        cities_list = [city.name for city in choices(cities, k=6)]
        cities_formatted = "\n".join([f"• {city}" for city in cities_list])
        return base + f" города:\n{cities_formatted}\n И еще более {count - 6} городов!"

    @staticmethod
    def get_before_list() -> str:
        return "Введите <b>название города</b> или выберите город из истории поиска:"

    @staticmethod
    def get_concert_list(concerts: Sequence[Concert], city: City) -> str:
        concert_list = concerts[len(concerts) - 20 :]
        max_city_letter_count = 40
        for concert in concert_list:
            concert.name = (
                f"{concert.name[:37]}..."
                if len(concert.name) > max_city_letter_count
                else concert.name
            )
        concert_list = [
            f"{concert.concert_date.strftime('%a, %d %b. %Y')}<i> от {concert.price} ₽</i>\n"
            f"<b><a href='{concert.link}'>{concert.name}</a></b>\n"
            for concert in concert_list
        ]
        concert_list = "\n".join(concert_list)
        city_name = str(city.name).upper()
        return (
            f'<a href="https://{city.abb}.{configure.bot.kassir_link}">{city_name}</a>. '
            f"Список концертов\n\n\n{concert_list}"
        )

    @staticmethod
    def get_welcome(user_name: str = "Пользователь") -> str:
        return f"Привет, {user_name}!\nДaвaй узнаем новые концерты"

    @staticmethod
    def get_error_concert() -> str:
        return "Пожалуйста, введите название города или выберите город из списка"

    @staticmethod
    def get_error_city() -> str:
        return "Ошибка ввода, возвращаю в главное меню"

    @staticmethod
    def get_update_time(time: float) -> str:
        return f"База данных обновлена.\nBыпoлнeнo за: {time:.1f} сек."
