from datetime import date

import pytest
from bs4 import BeautifulSoup

from bot.parsing.kassir import KassirParser


@pytest.fixture
def parser():
    return KassirParser()


@pytest.mark.parametrize(
    "html, expected_html",
    [
        (
            """
            <div class="compilation-tile__title">Title</div>
            <time class="compilation-tile__date" datetime="2022-12-31T23:59:59+00:00"></time>
            <li class="compilation-tile__price-block">
                <span class="text-[0.65rem]">от 2000 P</span>
            </li>
            <a class="compilation-tile__img-block" href="/koncert/1"></a>
            """,
            {
                "name": "Title",
                "date": date(2022, 12, 31),
                "price": 2000,
                "link": "/koncert/1",
            },
        ),
        (
            """
            <div>Title</div>
            <time datetime="2022-12-31T23:59:59+00:00"></time>
            <li>
                <span>от 2000 P</span>
            </li>
            <a href="/koncert/1"></a>
            """,
            {
                "name": "",
                "date": None,
                "price": 0,
                "link": "",
            },
        ),
        (
            """
            <div class="compilation-tile__title">Title😄</div>
            <time class="compilation-tile__date" datetime="2022-12-31T23:59:59"></time>
            <li class="compilation-tile__price-block">
                <span class="text-[0.65rem]">от 2 f0  00 P</span>
            </li>
            <a class="compilation-tile__img-block" href="/koncert/1 1"></a>
            """,
            {
                "name": "Title😄",
                "date": None,
                "price": 2000,
                "link": "/koncert/1 1",
            },
        ),
        (
            """
            <div class="compilation-tile__title"></div>
            <time class="compilation-tile__date"></time>
            <li class="compilation-tile__price-block">
                <span class="text-[0.65rem]">aaa</span>
            </li>
            <a class="compilation-tile__img-block"></a>
            """,
            {
                "name": "",
                "date": None,
                "price": 0,
                "link": "",
            },
        ),
        (
            """
            """,
            {
                "name": "",
                "date": None,
                "price": 0,
                "link": "",
            },
        ),
    ],
)
def test_scrap_data_group(parser, html, expected_html):
    soup = BeautifulSoup(html, "lxml")
    assert parser._scrap_data_group(soup) == expected_html


@pytest.mark.parametrize(
    "data, expected_data",
    [
        (
            {
                "name": "Title",
                "date": date(2022, 12, 31),
                "price": 2000,
                "link": "/koncert/1",
            },
            True,
        ),
        (
            {
                "name": "",
                "date": date(2022, 12, 31),
                "price": 2000,
                "link": "/koncert/1",
            },
            False,
        ),
        (
            {
                "name": "Title",
                "date": None,
                "price": 2000,
                "link": "/koncert/1",
            },
            False,
        ),
        (
            {
                "name": "Title",
                "date": date(2022, 12, 31),
                "price": 0,
                "link": "/koncert/1",
            },
            False,
        ),
        (
            {
                "name": "Title",
                "date": date(2022, 12, 31),
                "price": 2000,
                "link": "",
            },
            False,
        ),
        (
            {
                "name": "Title симфония",
                "date": date(2022, 12, 31),
                "price": 2000,
                "link": "/koncert/1",
            },
            False,
        ),
        (
            {
                "name": "Title",
                "date": date(2022, 12, 31),
                "price": 499,
                "link": "/koncert/1",
            },
            False,
        ),
    ],
)
def test_is_valid_date(parser, data, expected_data):
    assert parser._is_valid_data(data) == expected_data


@pytest.mark.parametrize(
    "html, expected_html",
    [
        (
            """
            <meta property="og:url" content="https://msk.kassir.ru">
            <div>
                <article class="recommendation-item compilation-tile">
                    <div class="compilation-tile__title">Title</div>
                    <time class="compilation-tile__date" datetime="2022-12-31T23:59:59+00:00"></time>
                    <li class="compilation-tile__price-block">
                        <span class="text-[0.65rem]">от 2000 P</span>
                    </li>
                    <a class="compilation-tile__img-block" href="/koncert/1"></a>
                </article>
                <article class="recommendation-item compilation-tile">
                    <div class="compilation-tile__title">Title</div>
                    <time class="compilation-tile__date" datetime="2022-12-31T23:59:59+00:00"></time>
                    <li class="compilation-tile__price-block">
                        <span class="text-[0.65rem]">от 2000 P</span>
                    </li>
                    <a class="compilation-tile__img-block" href="/koncert/1"></a>
                </article>
            </div>
            """,
            [
                {
                    "name": "Title",
                    "date": date(2022, 12, 31),
                    "price": 2000,
                    "link": "https://msk.kassir.ru/koncert/1",
                    "city": "msk",
                },
                {
                    "name": "Title",
                    "date": date(2022, 12, 31),
                    "price": 2000,
                    "link": "https://msk.kassir.ru/koncert/1",
                    "city": "msk",
                },
            ],
        ),
        (
            """
            <meta property="og:url" content="https://kassir.ru">
            <div>
                <article class="recommendation-item compilation-tile">
                    <div class="compilation-tile__title">Title</div>
                    <time class="compilation-tile__date" datetime="2022-12-31T23:59:59+00:00"></time>
                    <li class="compilation-tile__price-block">
                        <span class="text-[0.65rem]">от 2000 P</span>
                    </li>
                    <a class="compilation-tile__img-block" href="/koncert/1"></a>
                </article>
            </div>
            """,
            [],
        ),
        (
            """
                <div>
                    <article class="recommendation-item compilation-tile">
                        <div class="compilation-tile__title">Title</div>
                        <time class="compilation-tile__date" datetime="2022-12-31T23:59:59+00:00"></time>
                        <li class="compilation-tile__price-block">
                            <span class="text-[0.65rem]">от 2000 P</span>
                        </li>
                        <a class="compilation-tile__img-block" href="/koncert/1"></a>
                    </article>
                </div>
                """,
            [],
        ),
        (
            """
                <meta property="og:url" content="https://msk.kassir.ru">
                <div>
                    <article class="recommendation-item compilation-tile">
                        <div class="compilation-tile__title">Title</div>
                        <a class="compilation-tile__img-block" href="/koncert/1"></a>
                    </article>
                    <article class="recommendation-item compilation-tile">
                    </article>
                </div>
                """,
            [],
        ),
        ("", []),
    ],
)
def test_parse_page_data(parser, html, expected_html):
    assert parser._parse_page_data(html) == expected_html
