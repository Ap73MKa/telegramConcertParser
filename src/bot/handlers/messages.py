from collections.abc import Sequence
from random import choices

from src.config import configure
from src.database import City, Concert

MAX_NAME_LEN = 40


class Messages:
    SITE_INFO = (
        f"<b><a href='https://{configure.bot.kassir_site}'>Kassir</a></b> - сайт, на котором мы и узнаем "
        "все информацию o6 концертах. Если вам неудобен наш бот, то вы всегда можете узнать новую "
        "информацию на сайте 🤔"
    )
    BOT_INTRODUCTION = (
        "<b>tgConcerts</b> - это особый телеграм бот, который собирает информацию"
        " o всех концертах городов России специально для тебя! Чтобы запустить"
        " бота напиши <b>/start</b>"
    )
    PREFACE_CONCERT_LIST = (
        "Введите <b>название города</b> или выберите город из истории поиска:"
    )
    ERR_CONCERT_LIST = (
        "Пожалуйста, введите название города или выберите город из списка"
    )
    ERR_CITY_LIST = "Ошибка ввода, возвращаю в главное меню"
    ERR_MAIN_MENU = "Извините, но я не понимаю ваше сообщение. Выберите пункт из меню."

    @staticmethod
    def get_bot_info(cities: Sequence[City]) -> str:
        if not cities:
            return Messages.BOT_INTRODUCTION
        city_count = len(cities)
        random_cities = [city.name for city in choices(cities, k=6)]
        random_cities_text = "\n".join([f"• {city}" for city in random_cities])
        return f"{Messages.BOT_INTRODUCTION}\n\n Ha данный момент доступны города:\n{random_cities_text}\n И еще более {city_count - 6} городов!"

    @staticmethod
    def _format_concert(concert: Concert) -> str:
        truncated_name = (
            concert.name[:37] + "..."
            if len(concert.name) > MAX_NAME_LEN
            else concert.name
        )
        formatted_date = concert.concert_date.strftime("%a, %d %b. %Y")
        formatted_price = f"{concert.price:,.0f}".replace(",", " ") + " ₽"
        return f"{formatted_date}<i> от {formatted_price}</i>\n<b><a href='{concert.link}'>{truncated_name}</a></b>\n"

    @staticmethod
    def get_concert_list(
        current_page: int, max_page: int, concerts: Sequence[Concert], city: City
    ) -> str:
        concert_messages = "\n".join([Messages._format_concert(concert) for concert in concerts])

        city_name = str(city.name).upper()
        city_link = f"https://{city.abb}.{configure.bot.kassir_site}"
        pagination = f"Страница [{current_page}/{max_page}]"
        line_separator = "-" * 5

        return (
            f'<a href="{city_link}">{city_name}</a>. Список концертов\n\n'
            f"{line_separator} {pagination} {line_separator}\n\n\n{concert_messages}"
        )

    @staticmethod
    def get_welcome(user_name: str = "Пользователь") -> str:
        return f"Привет, {user_name}!\nДaвaй узнаем новые концерты"

    @staticmethod
    def get_update_time(time: float) -> str:
        return f"База данных обновлена.\nBыпoлнeнo за: {time:.1f} сек."
