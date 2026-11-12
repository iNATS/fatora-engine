"""Safe, bounded document validation for Fatora Engine.

This module validates in-memory uploads only. It deliberately does not persist
documents or send them to external services.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import PurePath


class DocumentValidationError(ValueError):
    """Raised when an uploaded document is unsupported or unsafe."""


@dataclass(frozen=True, slots=True)
class DocumentInput:
    filename: str
    media_type: str
    size_bytes: int
    sha256: str
    content: bytes


# Signatures are checked against bytes; client-provided MIME types are untrusted.
_SIGNATURES: tuple[tuple[str, bytes, bytes | None], ...] = (
    ("application/pdf", b"%PDF-", None),
    ("image/png", b"\x89PNG\r\n\x1a\n", None),
    ("image/jpeg", b"\xff\xd8\xff", None),
    ("image/webp", b"RIFF", b"WEBP"),
    ("image/tiff", b"II*\x00", None),
    ("image/tiff", b"MM\x00*", None),
)
_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}
DEFAULT_MAX_BYTES = 15 * 1024 * 1024


def _detect_media_type(content: bytes) -> str | None:
    for media_type, prefix, secondary in _SIGNATURES:
        if not content.startswith(prefix):
            continue
        if secondary is not None and content[8:12] != secondary:
            continue
        return media_type
    return None


def validate_document(
    filename: str,
    content: bytes,
    *,
    declared_media_type: str | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> DocumentInput:
    """Validate size, file signature, extension and optional declared MIME type."""
    if not isinstance(content, bytes) or not content:
        raise DocumentValidationError("The uploaded document is empty.")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive.")
    if len(content) > max_bytes:
        raise DocumentValidationError(
            f"Document exceeds the {max_bytes}-byte upload limit."
        )

    safe_name = PurePath(filename.replace("\\", "/")).name.strip()
    if not safe_name or safe_name in {".", ".."}:
        raise DocumentValidationError("A valid filename is required.")

    detected = _detect_media_type(content)
    if detected is None:
        raise DocumentValidationError("Unsupported or unrecognized document format.")

    extension = PurePath(safe_name).suffix.lower()
    expected = _EXTENSIONS.get(extension)
    if expected is None:
        raise DocumentValidationError("File extension is not supported.")
    if expected != detected:
        raise DocumentValidationError("File extension does not match document content.")

    if declared_media_type:
        declared = declared_media_type.split(";", 1)[0].strip().lower()
        if declared not in {"application/octet-stream", detected}:
            raise DocumentValidationError("Declared content type does not match file content.")

    return DocumentInput(
        filename=safe_name,
        media_type=detected,
        size_bytes=len(content),
        sha256=sha256(content).hexdigest(),
        content=content,
    )
