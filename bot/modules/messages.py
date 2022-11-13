from abc import ABC

from .config import Config
from .get_cities import get_cities
from bot.database.methods.get import get_concerts_by_city


# todo remade Message to module type, remove dependencies
class Messages(ABC):

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
        concert_list = get_concerts_by_city(city_abb)
        concert_list = concert_list[len(concert_list) - 20:]
        for concert in concert_list:
            concert.name = f'{concert.name[:37]}...' if len(concert.name) > 40 else concert.name
        concert_list = '\n'.join([f"{concert.date.strftime('%a, %d %b. %Y')}<i> от {concert.price} ₽</i>\n"
                                  f"<b><a href='{concert.url}'>{concert.name}</a></b>\n" for concert in concert_list])
        return f'<a href="https://{city_abb}.{Config.KASSIR_SITE}">{get_cities()[city_abb].upper()}</a>. ' \
               f'Список концертов\n\n\n{concert_list}'

    @staticmethod
    def get_welcome_msg(user_name: str = 'Пользователь') -> str:
        return f'Привет, {user_name}!\nДавай узнаем новые концерты'
