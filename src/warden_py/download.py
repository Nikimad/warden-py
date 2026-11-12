import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from .constants import MAX_REDIRECTS, TIMEOUT


@dataclass(frozen=True)
class DownloadResult:
    url: str
    downloaded_at: datetime
    content: bytes | None = None
    status_code: int | None = None
    error: str | None = None


def create_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=True, max_redirects=MAX_REDIRECTS)


async def download_feed(client: httpx.AsyncClient, url: str) -> DownloadResult:
    status_code: int | None = None
    error: str | None = None

    downloaded_at = datetime.now(timezone.utc)

    try:
        response = await client.get(url)
        response.raise_for_status()

        return DownloadResult(
            url=url,
            downloaded_at=downloaded_at,
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

    return DownloadResult(
        url=url,
        downloaded_at=downloaded_at,
        status_code=status_code,
        error=error,
    )


async def download_feeds(urls: list[str]) -> list[DownloadResult]:
    async with create_client() as client:
        tasks = [download_feed(client, url) for url in urls]
        return await asyncio.gather(*tasks)
