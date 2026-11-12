from pathlib import Path

import httpx

SOURCES_PATH = Path("sources.yaml")

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///warden.db"

MAX_TIMEOUT_S = 8.0
CONNECT_TIMEOUT_S = 3.0
TIMEOUT = httpx.Timeout(MAX_TIMEOUT_S, connect=CONNECT_TIMEOUT_S)

MAX_REDIRECTS = 10
