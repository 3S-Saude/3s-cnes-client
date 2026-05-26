"""Normalização de texto e valores simples."""

from __future__ import annotations

LANDLINE_DIGITS = 8
MOBILE_DIGITS = 9


def clean_text(value: str | None) -> str | None:
    """Remove espaços redundantes e preserva valores ausentes."""
    if value is None:
        return None
    normalized = " ".join(value.split())
    return normalized or None


def parse_bool(value: str | None) -> bool | None:
    """Converte representações comuns de booleano vindas do XML."""
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"true", "1", "s", "sim"}:
        return True
    if normalized in {"false", "0", "n", "nao", "não"}:
        return False
    return None


def format_phone(ddd: str | None, number: str | None, ddi: str | None = None) -> str | None:
    """Formata um telefone brasileiro quando há DDD e número."""
    if not number:
        return None

    digits = "".join(ch for ch in number if ch.isdigit())
    if len(digits) == LANDLINE_DIGITS:
        formatted = f"{digits[:4]}-{digits[4:]}"
    elif len(digits) == MOBILE_DIGITS:
        formatted = f"{digits[:5]}-{digits[5:]}"
    else:
        formatted = digits or number

    clean_ddd = "".join(ch for ch in ddd or "" if ch.isdigit())
    if clean_ddd:
        formatted = f"({clean_ddd}) {formatted}"

    clean_ddi = "".join(ch for ch in ddi or "" if ch.isdigit())
    if clean_ddi and clean_ddi != "55":
        formatted = f"+{clean_ddi} {formatted}"

    return formatted
