# Benchmark protocol

## Goal

Measure invoice/receipt extraction quality independently from vendor claims. OCR text accuracy alone is insufficient.

## Dataset governance

Each sample must record source or generation recipe, license, redistribution permission, document type, language/script, locale if known, annotation process, split and provenance. Never commit private customer invoices. Public availability does not automatically grant redistribution rights.

## Metrics

- Character Error Rate (CER) and Word Error Rate (WER).
- Header field exact match and normalized F1.
- Line-item row/cell precision, recall and F1.
- Numeric exact match for quantity, price, tax and totals.
- Table structure metric where appropriate.
- Evidence coverage and localization quality.
- Review rate, latency, throughput and peak memory.

Report by language, script direction, document quality, document type and field. Include sample counts and confidence intervals.

## Initial strata

Arabic-only printed invoice; English invoice; Arabic/English mixed invoice; Arabic-Indic and Western digits; RTL tables with LTR product codes; thermal receipt; low-resolution phone photo; skewed/shadowed scan; multi-page invoice; discounts and multiple tax rates.

## Baselines

Evaluate PaddleOCR, Tesseract, Docling-based pipelines and selected model adapters only after checking exact code/model licenses, versions, configurations and hardware.

## Reporting

A score is valid only for the exact benchmark split, version and configuration used. Disclose whether the run was performed by project maintainers.
