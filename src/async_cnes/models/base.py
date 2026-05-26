"""Base Pydantic compartilhada pelos modelos públicos."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class AsyncCnesModel(BaseModel):
    """Modelo base com serialização JSON por padrão."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Retorna dados já compatíveis com JSON."""
        kwargs.setdefault("mode", "json")
        return super().model_dump(*args, **kwargs)
