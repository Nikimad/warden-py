# warden-py

[![CI](https://github.com/Nikimad/warden-py/actions/workflows/ci.yml/badge.svg)](https://github.com/Nikimad/warden-py/actions/workflows/ci.yml)

Персональный RSS-ридер: раз в сутки скачивает статьи из списка фидов, собирает дайджест и показывает его на веб-странице мелкими карточками. Позже добавятся резюме и оценка релевантности через LLM и отправка в Telegram.

## Запуск

Нужны Python 3.14+ и [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m warden_py https://feeds.bbci.co.uk/news/technology/rss.xml
```

Или через установленную команду:

```bash
uv run warden-py https://feeds.bbci.co.uk/news/technology/rss.xml
```

## Вывод

```
OK | https://feeds.bbci.co.uk/news/technology/rss.xml | 200 | 15507 bytes
ERROR | https://no-such-host.invalid | Connection timeout while requesting ...
```

## Разработка

| Команда | Что делает |
|---|---|
| `make test` | тесты (pytest, сеть замокана через respx) |
| `make lint` | ruff check |
| `make format` | ruff format |
| `make typecheck` | mypy в строгом режиме |
| `make check` | всё вышеперечисленное, как в CI |
