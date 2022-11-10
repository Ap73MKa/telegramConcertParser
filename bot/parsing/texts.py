from abc import ABC
from bot.misc import Config
from bot.database.methods.get import get_concerts_by_city
from .utils import get_cities


class Texts(ABC):

    @staticmethod
    def get_site_info() -> str:
        return '<b><a href="https://kassir.ru">Kassir</a></b> - сайт, на котором мы и узнаем все информацию об ' \
                'концертах. Если вам неудобен наш бот, то вы всегда можете узнать новую информацию на сайте 🤔'

    @staticmethod
    def get_bot_info() -> str:
        cities = '\n'.join([f'• {city}' for city in get_cities().values()])
        return f'<b>tgConcerts</b> - это особый телеграм бот, который собирает информацию о всех концертах городов ' \
               f'России специально для тебя! Чтобы запустить бота напиши <b>/start</b>\n\nНа данный момент доступны ' \
               f'города:\n{cities}'

    @staticmethod
    def get_concert_list(city_abb: str) -> str:
        city_name = get_cities()[city_abb]
        concert_list = get_concerts_by_city(city_abb)
        concert_list = '\n'.join([f"{concert.date.strftime('%a, %d %b. %Y')} <i>от {concert.price} ₽</i>\n"
                                  f"<b><a href='{concert.url}'>{concert.name}</a></b>\n" for concert in concert_list])
        return f'<a href="https://{city_abb}.{Config.URL}">{city_name.upper()}</a>. ' \
               f'Список концертов\n\n\n{concert_list}'

    @staticmethod
    def get_welcome_msg(user_name: str = 'Пользователь') -> str:
        return f'Привет, {user_name}\n. Давай узнаем новые концерты'
