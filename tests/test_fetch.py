from datetime import timedelta

import httpx
import pytest
from respx import MockRouter

from warden_py.fetch import MAX_REDIRECTS, fetch

URL = "https://example.test/feed.xml"
HTTP_URL = "http://example.test/feed.xml"
LOOP_URL = "https://example.test/loop"

FEED_BODY = b"<rss version='2.0'><channel><title>Test</title></channel></rss>"

BAD_STATUS_CODES = (404, 500, 503)
REDIRECT_STATUS_CODES = (301, 302, 307, 308)

NETWORK_FAILURES = [
    pytest.param(httpx.ConnectTimeout, "Connection timeout", id="connect_timeout"),
    pytest.param(httpx.ReadTimeout, "Read timeout", id="read_timeout"),
    pytest.param(httpx.ConnectError, "Connection error", id="connect_error"),
    pytest.param(httpx.RequestError, "An error occurred", id="other_request_error"),
]


async def test_fetch_success(respx_mock: MockRouter) -> None:
    respx_mock.get(URL).mock(return_value=httpx.Response(200, content=FEED_BODY))

    result = await fetch(URL)
    assert result.content == FEED_BODY
    assert result.status_code == 200
    assert result.url == URL
    assert result.error is None
    assert result.fetched_at.utcoffset() == timedelta(0)


@pytest.mark.parametrize("status_code", BAD_STATUS_CODES)
async def test_fetch_bad_status_code(respx_mock: MockRouter, status_code: int) -> None:
    respx_mock.get(URL).mock(return_value=httpx.Response(status_code))

    result = await fetch(URL)
    assert result.content is None
    assert result.status_code == status_code
    assert result.error is not None
    assert str(status_code) in result.error


@pytest.mark.parametrize(("exception", "error_fragment"), NETWORK_FAILURES)
async def test_fetch_network_failure(
    respx_mock: MockRouter, exception: type[httpx.RequestError], error_fragment: str
) -> None:
    respx_mock.get(URL).mock(side_effect=exception)

    result = await fetch(URL)
    assert result.content is None
    assert result.status_code is None
    assert result.error is not None
    assert error_fragment in result.error


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_fetch_redirect(respx_mock: MockRouter, redirect_status_code: int) -> None:
    respx_mock.get(HTTP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": URL})
    )
    respx_mock.get(URL).mock(return_value=httpx.Response(200, content=FEED_BODY))

    result = await fetch(HTTP_URL)
    assert result.content == FEED_BODY
    assert result.status_code == 200
    assert result.url == HTTP_URL
    assert result.error is None


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_fetch_redirect_not_found(respx_mock: MockRouter, redirect_status_code: int) -> None:
    respx_mock.get(HTTP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": URL})
    )
    respx_mock.get(URL).mock(return_value=httpx.Response(404))

    result = await fetch(HTTP_URL)
    assert result.content is None
    assert result.status_code == 404
    assert result.url == HTTP_URL
    assert result.error is not None
    assert "404" in result.error


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_fetch_redirect_loop(respx_mock: MockRouter, redirect_status_code: int) -> None:
    route = respx_mock.get(LOOP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": LOOP_URL})
    )

    result = await fetch(LOOP_URL)

    assert result.content is None
    assert result.status_code is None
    assert result.error is not None
    assert "Too many redirects" in result.error
    assert route.call_count == MAX_REDIRECTS + 1
