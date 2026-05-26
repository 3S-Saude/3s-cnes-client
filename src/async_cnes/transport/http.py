"""Transporte HTTP assíncrono baseado em httpx."""

from __future__ import annotations

from dataclasses import dataclass

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from async_cnes.contracts import SoapOperation
from async_cnes.exceptions import CnesConnectionError, CnesTimeoutError
from async_cnes.models.config import ClientConfig

HTTP_BAD_REQUEST = 400


@dataclass(slots=True)
class _RetryableRequestError(Exception):
    kind: str
    message: str

    def to_public_exception(self) -> CnesConnectionError | CnesTimeoutError:
        if self.kind == "timeout":
            return CnesTimeoutError(self.message)
        return CnesConnectionError(self.message)


class HttpxSoapTransport:
    """Transporte SOAP assíncrono com timeout e retry configuráveis."""

    def __init__(
        self,
        config: ClientConfig,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._client = client
        self._owns_client = client is None

    async def __aenter__(self) -> HttpxSoapTransport:
        self._ensure_client()
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Fecha o cliente HTTP quando ele foi criado pelo transporte."""
        if self._client is not None and self._owns_client:
            await self._client.aclose()
        self._client = None

    async def post(self, operation: SoapOperation, content: bytes) -> bytes:
        """Envia um envelope SOAP e retorna o corpo bruto da resposta."""
        retry = self._config.retry
        if retry.enabled and retry.max_attempts > 1:
            return await self._post_with_retries(operation, content)

        try:
            return await self._post_once(operation, content)
        except _RetryableRequestError as exc:
            raise exc.to_public_exception() from exc

    async def _post_with_retries(self, operation: SoapOperation, content: bytes) -> bytes:
        retry = self._config.retry
        retryer = AsyncRetrying(
            stop=stop_after_attempt(retry.max_attempts),
            wait=wait_exponential(
                multiplier=retry.initial_backoff,
                max=retry.max_backoff,
            ),
            retry=retry_if_exception_type(_RetryableRequestError),
            reraise=True,
        )
        try:
            async for attempt in retryer:
                with attempt:
                    return await self._post_once(operation, content)
        except _RetryableRequestError as exc:
            raise exc.to_public_exception() from exc

        msg = "Retry finalizado sem resposta do CNES."
        raise CnesConnectionError(msg)

    def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            headers = {
                "User-Agent": self._config.user_agent,
                "Accept": "application/soap+xml, text/xml",
            }
            if self._config.headers:
                headers.update(self._config.headers)

            self._client = httpx.AsyncClient(
                timeout=self._config.timeout,
                headers=headers,
                auth=self._config.auth,
                proxy=self._config.proxy,
                verify=self._config.verify,
            )
        return self._client

    async def _post_once(self, operation: SoapOperation, content: bytes) -> bytes:
        client = self._ensure_client()
        headers = {
            "Content-Type": "application/soap+xml; charset=utf-8",
        }
        if operation.soap_action:
            headers["SOAPAction"] = operation.soap_action

        try:
            response = await client.post(self._config.endpoint, content=content, headers=headers)
        except httpx.TimeoutException as exc:
            msg = "Timeout ao comunicar com o serviço CNES."
            raise _RetryableRequestError("timeout", msg) from exc
        except httpx.TransportError as exc:
            msg = f"Falha de conexão ao comunicar com o serviço CNES: {exc}"
            raise _RetryableRequestError("connection", msg) from exc

        if (
            response.status_code in self._config.retry.retry_status_codes
            and not _looks_like_soap_fault(response.content)
        ):
            msg = f"Serviço CNES retornou HTTP {response.status_code}."
            raise _RetryableRequestError("status", msg)

        if (
            response.status_code >= HTTP_BAD_REQUEST
            and not _looks_like_soap_fault(response.content)
        ):
            msg = f"Serviço CNES retornou HTTP {response.status_code}."
            raise CnesConnectionError(msg)

        return response.content


def _looks_like_soap_fault(content: bytes) -> bool:
    sample = content[:4096].lower()
    return b"fault" in sample and (b"envelope" in sample or b"body" in sample)
