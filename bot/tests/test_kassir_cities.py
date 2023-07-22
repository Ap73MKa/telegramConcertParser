import pytest

from bot.parsing.kassir_cities import KassirCitiesParser


@pytest.fixture
def parser():
    return KassirCitiesParser()


@pytest.mark.parametrize(
    "html, expected_html",
    [
        (
            """
            <div class="city-container-wrapper">
                <ul>
                    <li>
                        <a href="https://msk.kassir.ru">Москва</a>
                    </li>
                    <li>
                        <a href="https://spb.kassir.ru">Санкт-Петербург</a>
                    </li>
                </ul>
            </div>
            """,
            [
                {
                    "abb": "msk",
                    "name": "Москва",
                    "simple_name": "москва",
                },
                {
                    "abb": "spb",
                    "name": "Санкт-Петербург",
                    "simple_name": "санктпетербург",
                },
            ],
        ),
        (
            """
            <div class="city-container-wrapper">
                <ul>
                    <li>
                        <a href="https://kassir.ru">Москва</a>
                    </li>
                    <li>
                        <a href="https://spb.kassir.ru"></a>
                    </li>
                </ul>
            </div>
            """,
            [],
        ),
        (
            """
            <div class="city-container-wrapper">
                <ul>
                    <li>
                        <a>Москва</a>
                    </li>
                    <li>
                        <a href="https://spb.kassir.ru">Санкт Петербур г</a>
                    </li>
                </ul>
            </div>
            """,
            [
                {
                    "abb": "spb",
                    "name": "Санкт Петербур г",
                    "simple_name": "санктпетербург",
                }
            ],
        ),
        ("", []),
    ],
)
def test_parse_page_data(parser, html, expected_html):
    assert parser._parse_page_data(html) == expected_html
