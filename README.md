# telegramConcertParser

![Checks](https://badgen.net/github/checks/ap73mka/telegramConcertParser)
[![CodeFactor](https://www.codefactor.io/repository/github/ap73mka/telegramconcertparser/badge)](https://www.codefactor.io/repository/github/ap73mka/telegramconcertparser)
![Release](https://badgen.net/github/release/ap73mka/telegramConcertParser)
![Licence](https://badgen.net/badge/Licence/MIT/blue)
![Python](https://badgen.net/badge/Python/3.10/blue?icon=pypi)

![banner](https://github.com/Ap73MKa/telegramConcertParser/assets/45181349/af860b57-df03-426a-838f-2210866468b1)

This is a Telegram Bot written in Python for monitoring concerts. Based on [aiogram](https://github.com/aiogram/aiogram).

## Features

- Search for concerts by entering the name of the city
- Search for concerts by city selection via the keyboard
- Repeating the previous request
- Updating the database every 8 hours
- Parsing information from [kassir.ru](https://kassir.ru/)

## Usage

### 1. Install Requirements

- Install [Python 3.10+](https://www.python.org/downloads/)

- Clone this repository<br>

```bash
git clone https://github.com/Ap73MKa/telegramConcertParser
```

- Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

- Run bot

```bash
python -m bot
```

### 2. Setup environment variables

- `TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather)
- `ADMIN_ID`: The Telegram User ID (not username) of the Owner of the bot
- `DEBUG`: Insert any symbols to enable debug mode
