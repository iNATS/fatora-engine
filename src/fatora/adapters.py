"""Provider-neutral OCR/layout adapter contract."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence

from fatora.documents import DocumentInput


@dataclass(frozen=True, slots=True)
class TextBlock:
    text: str
    page: int
    confidence: float | None = None
    polygon: tuple[tuple[float, float], ...] = ()


@dataclass(frozen=True, slots=True)
class OCRResult:
    blocks: Sequence[TextBlock]
    provider: str
    provider_version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class OCRCapabilities:
    media_types: tuple[str, ...]
    languages: tuple[str, ...] = ()
    supports_layout: bool = False
    supports_tables: bool = False


class OCRAdapter(Protocol):
    """An OCR adapter must be deterministic about its declared capabilities."""

    @property
    def name(self) -> str: ...

    @property
    def capabilities(self) -> OCRCapabilities: ...

    def extract(self, document: DocumentInput) -> OCRResult: ...
