# telegramConcertParser

![](https://badgen.net/github/checks/ap73mka/telegramConcertParser)
![](https://badgen.net/github/release/ap73mka/telegramConcertParser)
![](https://badgen.net/badge/Licence/MIT/blue)
![](https://badgen.net/badge/Python/3.10/blue?icon=pypi)

This is a Telegram Bot written in Python for monitoring concerts. Based on [aiogram](https://github.com/aiogram/aiogram).

## Features

- Search for concerts by entering the name of the city
- Search for concerts by city selection via the keyboard
- Repeating the previous request
- Updating the database every 8 hours
- Parsing information from [kassir.ru](https://kassir.ru/)

## Usage

### 1. Install Requirements

- Clone this repository<br>

```
git clone https://github.com/Ap73MKa/telegramConcertParser
```

- Install requirements

```
pip install -r requirements.txt
```

### 2. Setup environment variables

- `TOKEN`: The Telegram Bot Token that you got from [@BotFather](https://t.me/BotFather)
- `ADMIN_ID`: The Telegram User ID (not username) of the Owner of the bot
- `DEBUG`: Insert any symbols to enable debug mode
