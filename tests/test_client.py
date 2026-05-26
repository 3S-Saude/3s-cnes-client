import httpx
import pytest

from async_cnes import CnesClient, RetryConfig
from async_cnes.exceptions import CnesConnectionError, CnesTimeoutError, CnesValidationError

from .fixtures import SOAP_SUCCESS_RESPONSE


@pytest.mark.asyncio
async def test_client_consultar_estabelecimento() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert b"requestConsultarEstabelecimentoSaude" in request.content
        return httpx.Response(200, content=SOAP_SUCCESS_RESPONSE)

    async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async with CnesClient(endpoint="https://example.test/cnes", http_client=async_client) as client:
        unidade = await client.consultar_estabelecimento("2400737")

    assert unidade.cnes == "2400737"
    assert requests[0].url == "https://example.test/cnes"


@pytest.mark.asyncio
async def test_client_validates_cnes_before_request() -> None:
    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _request: httpx.Response(500)),
    )

    async with CnesClient(endpoint="https://example.test/cnes", http_client=async_client) as client:
        with pytest.raises(CnesValidationError):
            await client.consultar_estabelecimento("abc")


@pytest.mark.asyncio
async def test_client_retries_transient_status() -> None:
    calls = 0

    def handler(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(503, content=b"service unavailable")
        return httpx.Response(200, content=SOAP_SUCCESS_RESPONSE)

    async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async with CnesClient(
        endpoint="https://example.test/cnes",
        retry=RetryConfig(enabled=True, max_attempts=2, initial_backoff=0, max_backoff=0),
        http_client=async_client,
    ) as client:
        unidade = await client.consultar_estabelecimento("2400737")

    assert unidade.cnes == "2400737"
    assert calls == 2


@pytest.mark.asyncio
async def test_client_timeout_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("boom")

    async_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async with CnesClient(
        endpoint="https://example.test/cnes",
        retry=RetryConfig(enabled=False),
        http_client=async_client,
    ) as client:
        with pytest.raises(CnesTimeoutError):
            await client.consultar_estabelecimento("2400737")


@pytest.mark.asyncio
async def test_client_connection_error_on_http_error() -> None:
    async_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _request: httpx.Response(404, content=b"not found")),
    )

    async with CnesClient(
        endpoint="https://example.test/cnes",
        retry=RetryConfig(enabled=False),
        http_client=async_client,
    ) as client:
        with pytest.raises(CnesConnectionError):
            await client.consultar_estabelecimento("2400737")
