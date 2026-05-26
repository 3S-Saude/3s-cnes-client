"""Configurações de cliente, transporte e retry."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import httpx
from httpx._types import AuthTypes

DEFAULT_ENDPOINT = "https://servicos.saude.gov.br/cnes/CnesService/v1r0"
DEFAULT_USER_AGENT = "3s-cnes-client/0.1.0"
DEFAULT_RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True, slots=True)
class RetryConfig:
    """Configuração de retry com exponential backoff."""

    enabled: bool = True
    max_attempts: int = 3
    initial_backoff: float = 0.2
    max_backoff: float = 2.0
    retry_status_codes: frozenset[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUS_CODES)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            msg = "max_attempts deve ser maior ou igual a 1"
            raise ValueError(msg)
        if self.initial_backoff < 0 or self.max_backoff < 0:
            msg = "backoff não pode ser negativo"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ClientConfig:
    """Configuração de transporte HTTP do cliente CNES."""

    endpoint: str = DEFAULT_ENDPOINT
    timeout: httpx.Timeout | float = 10.0
    retry: RetryConfig = field(default_factory=RetryConfig)
    headers: Mapping[str, str] | None = None
    user_agent: str = DEFAULT_USER_AGENT
    auth: AuthTypes | None = None
    proxy: str | None = None
    verify: bool = True
