"""Contratos SOAP suportados pela biblioteca."""

from async_cnes.contracts.cnes_service import (
    CONSULTAR_ESTABELECIMENTO_SAUDE,
    SoapOperation,
    build_consultar_estabelecimento_envelope,
)

__all__ = [
    "CONSULTAR_ESTABELECIMENTO_SAUDE",
    "SoapOperation",
    "build_consultar_estabelecimento_envelope",
]
