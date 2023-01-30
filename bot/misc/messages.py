from abc import ABC
from random import choices

from bot.database import get_concerts_by_city_or_none, get_city_by_abb_or_none, get_all_cities_by_order_or_none
from .config import Config


class Messages(ABC):

    @staticmethod
    def get_site_info() -> str:
        return '<b><a href="https://kassir.ru">Kassir</a></b> - сайт, на котором мы и узнаем все информацию об ' \
               'концертах. Если вам неудобен наш бот, то вы всегда можете узнать новую информацию на сайте 🤔'

    @staticmethod
    def get_bot_info() -> str:
        cities = get_all_cities_by_order_or_none()
        count = len(cities)
        cities = '\n'.join([f'• {city.name}' for city in choices(cities, k=6)])
        return '<b>tgConcerts</b> - это особый телеграм бот, который собирает информацию о всех концертах городов ' \
               'России специально для тебя! Чтобы запустить бота напиши <b>/start</b>\n\nНа данный момент доступны ' \
               f'города:\n{cities}\n И еще более {count - 6} городов!'

    @staticmethod
    def get_before_list() -> str:
        return 'Введите <b>название города</b> или выберите город из истории поиска:'

    @staticmethod
    def get_concert_list(city_abb: str) -> str:
        concert_list = get_concerts_by_city_or_none(city_abb)

        if len(concert_list) > 20:
            concert_list = concert_list[len(concert_list) - 20:]

        for concert in concert_list:
            concert.name = f'{concert.name[:37]}...' if len(concert.name) > 40 else concert.name

        concert_list = '\n'.join([f"{concert.date.strftime('%a, %d %b. %Y')}<i> от {concert.price} ₽</i>\n"
                                  f"<b><a href='{concert.link}'>{concert.name}</a></b>\n" for concert in concert_list])
        city = get_city_by_abb_or_none(city_abb).name.upper()
        return f'<a href="https://{city_abb}.{Config.KASSIR_SITE}">{city}</a>. ' \
               f'Список концертов\n\n\n{concert_list}'

    @staticmethod
    def get_welcome(user_name: str = 'Пользователь') -> str:
        return f'Привет, {user_name}!\nДавай узнаем новые концерты'

    @staticmethod
    def get_welcome_photo():
        return 'https://sun1-87.userapi.com/impg/wEoV6bpiSXmT3uCKUaB7Cpmj2Nmym5l4hMKnLw/55rB5oNouD4.jpg?size=2000x793' \
               '&quality=96&sign=7f6fe46af2cbdecd238dfa3d7c435248&type=album '

    @staticmethod
    def get_random() -> str:
        messages = (
            'Не пропустите ни одного концерта!🔥',
            'Быстрый доступ ко всем концертам страны!',
            '😎🤏\n😳🕶🤏',
        )
        return choices(messages)[0]

    @staticmethod
    def get_error_concert() -> str:
        return 'Пожалуйста, введите название города или выберите город из списка'

    @staticmethod
    def get_error_city() -> str:
        return 'Ошибка ввода, возвращаю в главное меню'

    @staticmethod
    def get_update_time(time) -> str:
        return f'База данных обновлена.\nВыполнено за: {time:.1f} сек.'
