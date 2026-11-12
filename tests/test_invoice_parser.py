from decimal import Decimal

from fatora.adapters import OCRResult, TextBlock
from fatora.invoice_parser import (
    extract_invoice_fields,
    normalize_amount,
    normalize_digits,
)


def _ocr(*lines):
    return OCRResult(
        blocks=tuple(TextBlock(text=line, page=1, confidence=0.95) for line in lines),
        provider="fixture",
    )


def test_normalize_arabic_indic_digits():
    assert normalize_digits("١٢٣٤٥٦٧٨٩٠") == "1234567890"


def test_normalize_amount_arabic_and_western_separators():
    assert normalize_amount("1,234.56") == Decimal("1234.56")
    assert normalize_amount("1.234,56") == Decimal("1234.56")
    assert normalize_amount("١٬٢٣٤٫٥٠") == Decimal("1234.50")
    assert normalize_amount("95,50") == Decimal("95.50")


def test_extracts_labeled_english_invoice_fields_with_evidence():
    result = extract_invoice_fields(
        _ocr(
            "Invoice No: INV-2026-001",
            "Invoice Date: 2026-11-12",
            "Subtotal: 100.00 SAR",
            "VAT: 15.00 SAR",
            "Grand Total: 115.00 SAR",
        ),
        source_sha256="b" * 64,
    )
    assert result.fields["invoice_number"].value == "INV-2026-001"
    assert result.fields["invoice_date"].value == "2026-11-12"
    assert result.fields["subtotal"].value == "100.00"
    assert result.fields["tax"].value == "15.00"
    assert result.fields["total"].value == "115.00"
    assert result.fields["currency"].value == "SAR"
    assert result.fields["total"].evidence[0].page == 1
    assert result.fields["total"].evidence[0].text == "Grand Total: 115.00 SAR"


def test_extracts_basic_arabic_fields_and_arabic_digits():
    result = extract_invoice_fields(
        _ocr(
            "رقم الفاتورة: ف-2026-١٢",
            "تاريخ الفاتورة: ١٢/١١/٢٠٢٦",
            "المجموع قبل الضريبة: ١٠٠٫٠٠",
            "ضريبة القيمة المضافة: ١٥٫٠٠",
            "الإجمالي المستحق: ١١٥٫٠٠ ر.س",
        ),
        source_sha256="c" * 64,
    )
    assert result.fields["invoice_number"].value == "ف-2026-١٢"
    assert result.fields["invoice_date"].value == "12/11/2026"
    assert result.fields["subtotal"].value == "100.00"
    assert result.fields["tax"].value == "15.00"
    assert result.fields["total"].value == "115.00"
    assert result.fields["currency"].value == "SAR"


def test_does_not_invent_missing_fields():
    result = extract_invoice_fields(_ocr("Thank you for your purchase"), "d" * 64)
    assert result.fields == {}
    assert result.source_sha256 == "d" * 64
