from datetime import datetime, timezone

import httpx

from warden_py.models import CheckResult

MAX_TIMEOUT_S = 8.0
CONNECT_TIMEOUT_S = 3.0
TIMEOUT = httpx.Timeout(MAX_TIMEOUT_S, connect=CONNECT_TIMEOUT_S)

MAX_REDIRECTS = 10


def get_response_ms(response: httpx.Response) -> int:
    return round(sum(r.elapsed.total_seconds() * 1000 for r in (*response.history, response)))


async def check(url: str) -> CheckResult:
    response_ms: int | None = None
    status_code: int | None = None
    error: str | None = None

    checked_at = datetime.now(timezone.utc)

    try:
        async with httpx.AsyncClient(max_redirects=MAX_REDIRECTS) as client:
            response = await client.get(url, timeout=TIMEOUT, follow_redirects=True)
            response.raise_for_status()

            return CheckResult(
                url=url,
                checked_at=checked_at,
                success=True,
                response_ms=get_response_ms(response),
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
        response_ms = get_response_ms(exc.response)
        status_code = exc.response.status_code
        error = f"Error response {status_code} while requesting {exc.request.url}."

    return CheckResult(
        url=url,
        checked_at=checked_at,
        success=False,
        response_ms=response_ms,
        status_code=status_code,
        error=error,
    )
