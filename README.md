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
- Updating the database every 12 hours
- Parsing information from [kassir.ru](https://kassir.ru/)

## Usage

- Install [Docker](https://www.docker.com/)

- Clone this repository

```bash
git clone https://github.com/Ap73MKa/telegramConcertParser
```

- Do a copy of .env.dist and named it .env. Fill environment variables using this [guide](assets/env.md).

```bash
cp .env.dist .env
```

- Run bot

```bash
docker compose up
```
