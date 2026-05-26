"""Cliente público assíncrono para o CNES."""

from __future__ import annotations

from collections.abc import Mapping

import httpx
from httpx._types import AuthTypes

from async_cnes.contracts import (
    CONSULTAR_ESTABELECIMENTO_SAUDE,
    build_consultar_estabelecimento_envelope,
)
from async_cnes.models import ClientConfig, EstabelecimentoSaude, RetryConfig
from async_cnes.models.config import DEFAULT_ENDPOINT, DEFAULT_USER_AGENT
from async_cnes.parsers import parse_consultar_estabelecimento_response
from async_cnes.transport import HttpxSoapTransport


class CnesClient:
    """Cliente assíncrono para o serviço SOAP oficial do CNES.

    Examples:
        ```python
        async with CnesClient() as client:
            unidade = await client.consultar_estabelecimento("2400737")
        ```
    """

    def __init__(
        self,
        *,
        endpoint: str | None = None,
        timeout: httpx.Timeout | float = 10.0,
        retry: RetryConfig | None = None,
        headers: Mapping[str, str] | None = None,
        user_agent: str | None = None,
        auth: AuthTypes | None = None,
        proxy: str | None = None,
        verify: bool = True,
        http_client: httpx.AsyncClient | None = None,
        transport: HttpxSoapTransport | None = None,
    ) -> None:
        self.config = ClientConfig(
            endpoint=endpoint or DEFAULT_ENDPOINT,
            timeout=timeout,
            retry=retry or RetryConfig(),
            headers=headers,
            user_agent=user_agent or DEFAULT_USER_AGENT,
            auth=auth,
            proxy=proxy,
            verify=verify,
        )
        self._transport = transport or HttpxSoapTransport(self.config, client=http_client)

    async def __aenter__(self) -> CnesClient:
        await self._transport.__aenter__()
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Fecha recursos de rede abertos pelo cliente."""
        await self._transport.aclose()

    async def consultar_estabelecimento(self, cnes: str) -> EstabelecimentoSaude:
        """Consulta um estabelecimento de saúde por código CNES.

        Args:
            cnes: Código CNES com exatamente 7 dígitos.

        Returns:
            Modelo Pydantic `EstabelecimentoSaude`, serializável para JSON.
        """
        envelope = build_consultar_estabelecimento_envelope(cnes)
        response = await self._transport.post(CONSULTAR_ESTABELECIMENTO_SAUDE, envelope)
        return parse_consultar_estabelecimento_response(response)
