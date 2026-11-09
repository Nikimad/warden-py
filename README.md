# warden-py

[![CI](https://github.com/Nikimad/warden-py/actions/workflows/ci.yml/badge.svg)](https://github.com/Nikimad/warden-py/actions/workflows/ci.yml)

Uptime-монитор: проверяет, доступен ли сайт, и сообщает код ответа и время отклика.

Сейчас это MVP: одна проверка одного адреса из консоли. Расписание, история проверок и алерты в Telegram появятся на следующих этапах.

## Запуск

Нужны Python 3.14+ и [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m warden_py https://github.com
```

Или через установленную команду:

```bash
uv run warden-py https://github.com
```

## Вывод

```
UP | https://github.com/Nikimad | 200 | 1411 ms
DOWN | https://github.com/no-such-page | 404 | 752 ms | Error response 404 while requesting ...
DOWN | https://no-such-host.invalid | Connection timeout while requesting ...
```

## Разработка

| Команда | Что делает |
|---|---|
| `make test` | тесты (pytest, сеть замокана через respx) |
| `make lint` | ruff check |
| `make format` | ruff format |
| `make typecheck` | mypy в строгом режиме |
| `make check` | всё вышеперечисленное, как в CI |
