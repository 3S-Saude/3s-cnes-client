"""Validadores de domínio."""

from __future__ import annotations

from async_cnes.exceptions import CnesValidationError

CNES_LENGTH = 7


def validate_cnes(cnes: str) -> str:
    """Valida e normaliza um código CNES conforme o XSD oficial."""
    normalized = str(cnes).strip()
    if len(normalized) != CNES_LENGTH or not normalized.isdigit():
        msg = "CNES deve conter exatamente 7 dígitos numéricos."
        raise CnesValidationError(msg)
    return normalized
