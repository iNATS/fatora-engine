# First-pass invoice extraction

## Scope

`fatora.invoice_parser.extract_invoice_fields` is a deterministic baseline
that consumes OCR text blocks. It does not perform OCR and is not a general
invoice understanding model.

The first pass recognizes common English and Arabic labels for:

- invoice number;
- invoice date;
- subtotal;
- tax / VAT amount;
- total;
- currency (SAR, AED, USD, EUR, GBP, EGP and DZD).

Every extracted value carries evidence from the OCR block that contained its
label and value, including page number and available confidence / geometry.
Fields that are not found are omitted rather than guessed.

## Numeric normalization

`normalize_amount` accepts Western and Arabic-Indic digits, Arabic thousands
and decimal separators, and common comma/dot grouping conventions. When both
comma and dot appear, the rightmost separator is treated as the decimal
separator. With one separator, one, two or four trailing digits are treated
as decimals; three trailing digits are treated as grouping.

This is a heuristic. Ambiguous values should be routed to human review by the
calling application rather than treated as accounting truth.

## Known limitations

- Labels and layouts are heuristic and will not cover all invoice templates.
- Dates are returned as recognized text; no ambiguous day/month interpretation
  is attempted.
- Line items, supplier identity, tax registration identifiers, discounts,
  withholding, multi-currency documents and totals spanning multiple blocks
  are not implemented.
- OCR quality, language identification and reading order are outside this
  module's scope.
- This parser is not a tax compliance or accounting rules engine.

Use a representative, consented, redacted evaluation set before relying on
these outputs in production. Track exact-match accuracy separately for Arabic,
English, mixed RTL/LTR, scanned quality and each field type.
