import pytest

from fatora.documents import DocumentValidationError, validate_document

PDF = b"%PDF-1.7\nexample"
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 16
JPEG = b"\xff\xd8\xff" + b"0" * 16
WEBP = b"RIFF" + b"0000" + b"WEBP" + b"data"


def test_accepts_pdf_and_hashes_content():
    result = validate_document("invoice.pdf", PDF, declared_media_type="application/pdf")
    assert result.media_type == "application/pdf"
    assert result.size_bytes == len(PDF)
    assert len(result.sha256) == 64


@pytest.mark.parametrize(
    ("name", "content", "media_type"),
    [
        ("scan.png", PNG, "image/png"),
        ("photo.jpg", JPEG, "image/jpeg"),
        ("scan.webp", WEBP, "image/webp"),
    ],
)
def test_accepts_supported_images(name, content, media_type):
    assert validate_document(name, content).media_type == media_type


def test_rejects_empty_document():
    with pytest.raises(DocumentValidationError, match="empty"):
        validate_document("empty.pdf", b"")


def test_rejects_oversized_document():
    with pytest.raises(DocumentValidationError, match="exceeds"):
        validate_document("invoice.pdf", PDF, max_bytes=4)


def test_rejects_mime_spoofing():
    with pytest.raises(DocumentValidationError, match="content type"):
        validate_document("invoice.pdf", PDF, declared_media_type="image/png")


def test_rejects_extension_spoofing():
    with pytest.raises(DocumentValidationError, match="extension"):
        validate_document("invoice.png", PDF)


def test_rejects_unknown_format():
    with pytest.raises(DocumentValidationError, match="Unsupported"):
        validate_document("invoice.pdf", b"not a pdf")


def test_strips_path_components_from_filename():
    result = validate_document("../../invoice.pdf", PDF)
    assert result.filename == "invoice.pdf"
