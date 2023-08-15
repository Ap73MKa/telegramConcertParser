from abc import ABC
from collections.abc import Sequence
from random import choices

from src.config import configure
from src.database import City, Concert

MAX_NAME_LEN = 40


class Messages(ABC):
    @staticmethod
    def get_site_info() -> str:
        return (
            f"<b><a href='https://{configure.bot.kassir_site}'>Kassir</a></b> - сайт, на котором мы и узнаем "
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
    def get_concert_list(
        current_page: int, max_page: int, concerts: Sequence[Concert], city: City
    ) -> str:
        concert_list = (
            {
                "name": f"{item.name[:37]}..."
                if len(item.name) > MAX_NAME_LEN
                else item.name,
                "date": item.concert_date.strftime("%a, %d %b. %Y"),
                "price": f"{item.price:,.0f}".replace(",", " ") + " ₽",
                "link": item.link,
            }
            for item in concerts
        )

        concert_text = "\n".join(
            f"{item['date']}<i> от {item['price']}</i>\n"
            f"<b><a href='{item['link']}'>{item['name']}</a></b>\n"
            for item in concert_list
        )

        city_name = str(city.name).upper()
        link = f"https://{city.abb}.{configure.bot.kassir_site}"
        pagination = f"Страница [{current_page}/{max_page}]"
        line = "-" * 15

        return (
            f'<a href="{link}">{city_name}</a>. Список концертов\n\n'
            f"{line} {pagination} {line}\n\n\n{concert_text}"
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
