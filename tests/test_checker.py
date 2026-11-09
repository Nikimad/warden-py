from datetime import timedelta

import httpx
import pytest
from respx import MockRouter

from warden_py.checker import MAX_REDIRECTS, check

URL = "https://example.test/"
HTTP_URL = "http://example.test/"
LOOP_URL = "https://example.test/loop"

MAX_MOCK_RESPONSE_MS = 1000

BAD_STATUS_CODES = (404, 500, 503)
REDIRECT_STATUS_CODES = (301, 302, 307, 308)

NETWORK_FAILURES = [
    pytest.param(httpx.ConnectTimeout, "Connection timeout", id="connect_timeout"),
    pytest.param(httpx.ReadTimeout, "Read timeout", id="read_timeout"),
    pytest.param(httpx.ConnectError, "Connection error", id="connect_error"),
    pytest.param(httpx.RequestError, "An error occurred", id="other_request_error"),
]


def assert_valid_response_ms(response_ms: int | None) -> None:
    assert response_ms is not None
    assert 0 <= response_ms < MAX_MOCK_RESPONSE_MS


async def test_check_success(respx_mock: MockRouter) -> None:
    respx_mock.get(URL).mock(return_value=httpx.Response(200))

    result = await check(URL)
    assert result.success is True
    assert result.status_code == 200
    assert_valid_response_ms(result.response_ms)
    assert result.url == URL
    assert result.error is None
    assert result.checked_at.utcoffset() == timedelta(0)


@pytest.mark.parametrize("status_code", BAD_STATUS_CODES)
async def test_check_bad_status_code(respx_mock: MockRouter, status_code: int) -> None:
    respx_mock.get(URL).mock(return_value=httpx.Response(status_code))

    result = await check(URL)
    assert result.success is False
    assert result.status_code == status_code
    assert_valid_response_ms(result.response_ms)
    assert result.error is not None
    assert str(status_code) in result.error


@pytest.mark.parametrize(("exception", "error_fragment"), NETWORK_FAILURES)
async def test_check_network_failure(
    respx_mock: MockRouter, exception: type[httpx.RequestError], error_fragment: str
) -> None:
    respx_mock.get(URL).mock(side_effect=exception)

    result = await check(URL)
    assert result.success is False
    assert result.status_code is None
    assert result.response_ms is None
    assert result.error is not None
    assert error_fragment in result.error


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_check_redirect(respx_mock: MockRouter, redirect_status_code: int) -> None:
    respx_mock.get(HTTP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": URL})
    )
    respx_mock.get(URL).mock(return_value=httpx.Response(200))

    result = await check(HTTP_URL)
    assert result.success is True
    assert result.status_code == 200
    assert_valid_response_ms(result.response_ms)
    assert result.url == HTTP_URL
    assert result.error is None


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_check_redirect_not_found(respx_mock: MockRouter, redirect_status_code: int) -> None:
    respx_mock.get(HTTP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": URL})
    )
    respx_mock.get(URL).mock(return_value=httpx.Response(404))

    result = await check(HTTP_URL)
    assert result.success is False
    assert result.status_code == 404
    assert_valid_response_ms(result.response_ms)
    assert result.url == HTTP_URL
    assert result.error is not None
    assert "404" in result.error


@pytest.mark.parametrize("redirect_status_code", REDIRECT_STATUS_CODES)
async def test_check_redirect_loop(respx_mock: MockRouter, redirect_status_code: int) -> None:
    route = respx_mock.get(LOOP_URL).mock(
        return_value=httpx.Response(redirect_status_code, headers={"Location": LOOP_URL})
    )

    result = await check(LOOP_URL)

    assert result.success is False
    assert result.status_code is None
    assert result.response_ms is None
    assert result.error is not None
    assert "Too many redirects" in result.error
    assert route.call_count == MAX_REDIRECTS + 1
