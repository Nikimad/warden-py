from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

MAX_TIMEOUT_S = 8.0
CONNECT_TIMEOUT_S = 3.0
TIMEOUT = httpx.Timeout(MAX_TIMEOUT_S, connect=CONNECT_TIMEOUT_S)

MAX_REDIRECTS = 10


@dataclass(frozen=True)
class FetchResult:
    url: str
    fetched_at: datetime
    content: bytes | None = None
    status_code: int | None = None
    error: str | None = None


async def fetch(url: str) -> FetchResult:
    status_code: int | None = None
    error: str | None = None

    fetched_at = datetime.now(timezone.utc)

    try:
        async with httpx.AsyncClient(max_redirects=MAX_REDIRECTS) as client:
            response = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
            response.raise_for_status()

            return FetchResult(
                url=url,
                fetched_at=fetched_at,
                content=response.content,
                status_code=response.status_code,
            )
    except httpx.ConnectTimeout as exc:
        error = f"Connection timeout while requesting {exc.request.url}."
    except httpx.ReadTimeout as exc:
        error = f"Read timeout while requesting {exc.request.url}."
    except httpx.ConnectError as exc:
        error = f"Connection error while requesting {exc.request.url}."
    except httpx.TooManyRedirects as exc:
        error = f"Too many redirects while requesting {exc.request.url}."
    except httpx.RequestError as exc:
        error = f"An error occurred while requesting {exc.request.url}."
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        error = f"Error response {status_code} while requesting {exc.request.url}."

    return FetchResult(
        url=url,
        fetched_at=fetched_at,
        status_code=status_code,
        error=error,
    )
