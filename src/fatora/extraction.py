"""Evidence-backed extraction result contracts (no OCR implementation yet)."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class Evidence:
    page: int
    text: str
    confidence: float | None = None
    # Optional normalized polygon coordinates in the range 0..1.
    polygon: tuple[tuple[float, float], ...] = ()


@dataclass(frozen=True, slots=True)
class ExtractedField:
    value: Any
    status: Literal["extracted", "missing", "needs_review"]
    evidence: tuple[Evidence, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class InvoiceExtraction:
    fields: dict[str, ExtractedField]
    source_sha256: str
    adapter: str
    language_hints: tuple[str, ...] = ()


def decimal_from_text(value: str) -> Decimal:
    """Parse a normalized decimal string; locale normalization belongs upstream."""
    try:
        return Decimal(value)
    except Exception as exc:
        raise ValueError(f"Invalid normalized decimal value: {value!r}") from exc
