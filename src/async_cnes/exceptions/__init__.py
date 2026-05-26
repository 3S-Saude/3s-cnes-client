"""Exceções públicas do async-cnes."""

from __future__ import annotations

from typing import Any


class CnesError(Exception):
    """Erro base para todas as falhas tratadas pela biblioteca."""


class CnesConnectionError(CnesError):
    """Falha de conexão, status HTTP inesperado ou indisponibilidade transitória."""


class CnesTimeoutError(CnesError):
    """Tempo limite excedido ao comunicar com o serviço CNES."""


class CnesSoapFaultError(CnesError):
    """Fault SOAP retornado pelo serviço CNES."""

    def __init__(
        self,
        message: str,
        *,
        fault_code: str | None = None,
        fault_string: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.fault_code = fault_code
        self.fault_string = fault_string
        self.detail = detail or {}


class CnesValidationError(CnesError):
    """Entrada inválida ou resposta incompatível com o contrato esperado."""


class CnesNotFoundError(CnesError):
    """Nenhum estabelecimento de saúde foi encontrado para a consulta."""


__all__ = [
    "CnesConnectionError",
    "CnesError",
    "CnesNotFoundError",
    "CnesSoapFaultError",
    "CnesTimeoutError",
    "CnesValidationError",
]
