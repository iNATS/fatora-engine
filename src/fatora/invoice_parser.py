"""Deterministic first-pass invoice field extraction from OCR text blocks.

This is a conservative baseline, not a trained document model. It only emits
fields when a known label and a parseable value occur in the same text block.
"""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from fatora.adapters import OCRResult
from fatora.extraction import Evidence, ExtractedField, InvoiceExtraction

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_SPACE_RE = re.compile(r"[\u00a0\u202f\s]+")
_AMOUNT_RE = re.compile(
    r"(?<![\w])(?:[-+]?\s*)"
    r"(?:\d{1,3}(?:[ ,٬٫.]\d{3})+|\d+)"
    r"(?:[.,٫٬]\d{1,4})?(?!\w)"
)

_LABELS = {
    "invoice_number": (
        r"invoice\s*(?:no\.?|number|#)",
        r"فاتورة\s*(?:رقم|رقمها)",
        r"رقم\s*الفاتورة",
    ),
    "invoice_date": (
        r"invoice\s*date",
        r"date\s*of\s*issue",
        r"تاريخ\s*الفاتورة",
        r"تاريخ\s*الإصدار",
        r"تاريخ\s*الاصدار",
    ),
    "subtotal": (
        r"sub\s*total",
        r"subtotal",
        r"المجموع\s*(?:قبل\s*الضريبة)?",
        r"الإجمالي\s*قبل\s*الضريبة",
        r"الاجمالي\s*قبل\s*الضريبة",
    ),
    "tax": (
        r"vat",
        r"tax\s*(?:amount)?",
        r"ضريبة\s*القيمة\s*المضافة",
        r"ضريبة",
    ),
    "total": (
        r"grand\s*total",
        r"total\s*(?:due|amount)?",
        r"الإجمالي\s*المستحق",
        r"الاجمالي\s*المستحق",
        r"الإجمالي",
        r"الاجمالي",
        r"المجموع\s*الكلي",
        r"الإجمالي\s*شامل\s*الضريبة",
    ),
}

_DATE_RE = re.compile(r"(?<!\d)(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})(?!\d)")
_CURRENCY_PATTERNS = (
    (re.compile(r"\bSAR\b|ر\.س|ريال\s*سعودي", re.IGNORECASE), "SAR"),
    (re.compile(r"\bAED\b|درهم\s*إماراتي", re.IGNORECASE), "AED"),
    (re.compile(r"\bUSD\b|\$", re.IGNORECASE), "USD"),
    (re.compile(r"\bEUR\b|€", re.IGNORECASE), "EUR"),
    (re.compile(r"\bGBP\b|£", re.IGNORECASE), "GBP"),
    (re.compile(r"\bEGP\b|جنيه\s*مصري", re.IGNORECASE), "EGP"),
    (re.compile(r"\bDZD\b|دج", re.IGNORECASE), "DZD"),
)


def normalize_digits(value: str) -> str:
    return value.translate(_DIGITS)


def normalize_amount(value: str) -> Decimal:
    """Normalize common Arabic/Western digit and decimal separator variants."""
    token = normalize_digits(value).strip()
    token = token.replace("٬", ",").replace("٫", ".")
    token = re.sub(r"[^0-9,\.\-+]", "", token)
    if not token or token in {"-", "+"}:
        raise ValueError("Amount contains no digits.")

    if "," in token and "." in token:
        # The rightmost punctuation is the decimal separator.
        decimal_sep = "," if token.rfind(",") > token.rfind(".") else "."
        grouping_sep = "." if decimal_sep == "," else ","
        token = token.replace(grouping_sep, "").replace(decimal_sep, ".")
    elif "," in token or "." in token:
        sep = "," if "," in token else "."
        left, right = token.rsplit(sep, 1)
        if len(right) in (1, 2, 4):
            token = left.replace(sep, "") + "." + right
        elif len(right) == 3:
            token = left.replace(sep, "") + right
        else:
            token = token.replace(sep, "")
    try:
        return Decimal(token)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc


def _find_currency(text: str) -> str | None:
    for pattern, code in _CURRENCY_PATTERNS:
        if pattern.search(text):
            return code
    return None


def _field_from_block(block, value: str, *, kind: str) -> ExtractedField:
    evidence = (Evidence(
        page=block.page,
        text=block.text,
        confidence=block.confidence,
        polygon=block.polygon,
    ),)
    if kind == "amount":
        try:
            parsed = normalize_amount(value)
        except ValueError:
            return ExtractedField(value=None, status="needs_review", evidence=evidence,
                                  warnings=("Amount could not be normalized.",))
        return ExtractedField(value=str(parsed), status="extracted", evidence=evidence)
    return ExtractedField(value=value.strip(" :：#-"), status="extracted", evidence=evidence)


def extract_invoice_fields(ocr: OCRResult, source_sha256: str) -> InvoiceExtraction:
    """Extract a conservative set of labeled invoice fields from OCR blocks."""
    found: dict[str, ExtractedField] = {}
    currency: str | None = None

    # Specific labels are checked before broad labels to reduce accidental matches.
    for block in ocr.blocks:
        text = normalize_digits(block.text)
        currency = currency or _find_currency(text)
        for field_name, labels in _LABELS.items():
            if field_name in found:
                continue
            label_pattern = "|".join(f"(?:{label})" for label in labels)
            match = re.search(
                rf"(?:{label_pattern})\s*[:：#-]?\s*(.*)$",
                text,
                flags=re.IGNORECASE,
            )
            if not match:
                continue
            remainder = match.group(1).strip()
            if field_name == "invoice_date":
                date_match = _DATE_RE.search(remainder)
                if date_match:
                    found[field_name] = _field_from_block(block, date_match.group(1), kind="text")
            elif field_name == "invoice_number":
                value_match = re.search(r"[A-Za-z0-9٠-٩۰-۹\u0600-\u06FF][A-Za-z0-9٠-٩۰-۹\u0600-\u06FF/_-]{1,}", remainder)
                if value_match:
                    found[field_name] = _field_from_block(block, value_match.group(0), kind="text")
            else:
                amount_match = _AMOUNT_RE.search(remainder)
                if amount_match:
                    found[field_name] = _field_from_block(block, amount_match.group(0), kind="amount")

    if currency:
        # Currency is evidenced by the first OCR block containing its symbol/code.
        source_block = next(
            block for block in ocr.blocks if _find_currency(normalize_digits(block.text))
        )
        found["currency"] = _field_from_block(source_block, currency, kind="text")

    return InvoiceExtraction(
        fields=found,
        source_sha256=source_sha256,
        adapter=ocr.provider,
    )
