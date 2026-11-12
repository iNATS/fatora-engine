from types import SimpleNamespace

import pytest

from fatora.documents import DocumentInput
from fatora.ocr.tesseract import TesseractAdapter


def _document(media_type="image/png"):
    return DocumentInput(
        filename="invoice.png",
        media_type=media_type,
        size_bytes=8,
        sha256="a" * 64,
        content=b"\\x89PNG\\r\\n\\x1a\\n",
    )


def _tsv(*rows):
    header = (
        "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\t"
        "left\ttop\twidth\theight\tconf\ttext\n"
    )
    return header + "".join("\t".join(row) + "\n" for row in rows)


def test_tesseract_adapter_groups_words_into_evidence_blocks(monkeypatch):
    tsv = _tsv(
        ["5", "1", "1", "1", "1", "2", "20", "10", "10", "8", "80", "Total"],
        ["5", "1", "1", "1", "1", "1", "5", "10", "10", "8", "100", "الإجمالي"],
        ["5", "1", "1", "1", "2", "1", "5", "30", "10", "8", "60", "115.00"],
        ["5", "1", "1", "1", "2", "2", "20", "30", "10", "8", "-1", ""],
    )

    def fake_run(*args, **kwargs):
        assert kwargs["input"] == _document().content
        assert kwargs["timeout"] == 30.0
        return SimpleNamespace(returncode=0, stdout=tsv.encode(), stderr=b"")

    monkeypatch.setattr("fatora.ocr.tesseract.subprocess.run", fake_run)
    result = TesseractAdapter().extract(_document())

    assert result.provider == "tesseract"
    assert [block.text for block in result.blocks] == ["الإجمالي Total", "115.00"]
    assert result.blocks[0].page == 1
    assert result.blocks[0].confidence == pytest.approx(0.9)


def test_tesseract_rejects_pdf_before_running_engine(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("Tesseract must not be invoked for PDF input.")

    monkeypatch.setattr("fatora.ocr.tesseract.subprocess.run", fail_if_called)
    with pytest.raises(ValueError, match="does not support"):
        TesseractAdapter().extract(_document("application/pdf"))


def test_tesseract_reports_missing_executable(monkeypatch):
    def missing(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr("fatora.ocr.tesseract.subprocess.run", missing)
    with pytest.raises(RuntimeError, match="executable was not found"):
        TesseractAdapter().extract(_document())
