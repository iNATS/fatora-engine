# Product Requirements — Fatora Engine

**Version:** 0.1-draft  
**Positioning:** open-source invoice and receipt extraction with evidence-backed validation.

## Problem hypothesis

Teams digitizing invoices and receipts combine OCR, layout parsing, custom field extraction, normalization, arithmetic checks and manual review. These steps are repeatedly reimplemented. Arabic and mixed-script documents add complexity around RTL text, numeral forms, table order, decimal separators and bilingual labels.

Our hypothesis: developers need a reusable, self-hostable layer that returns a consistent schema and explains where each value came from. This must be validated with real users before claiming product-market fit.

## Primary users

1. Developers building ERP, POS, procurement, expense and accounting products.
2. Accountants and small businesses processing recurring invoices.
3. Integrators requiring private/on-premise document processing.
4. Researchers evaluating OCR and extraction pipelines.

## MVP scope (P0)

- PDF/JPEG/PNG ingestion with size and page limits.
- One baseline OCR/document adapter behind a stable interface.
- Invoice and receipt document types.
- Header fields: supplier, buyer, invoice number, issue date, due date, currency.
- Line items: description, quantity, unit price, discount, tax rate, line total.
- Totals: subtotal, tax, discount, fees, grand total, amount paid, balance due.
- Evidence per extracted field: page, bounding box when available, raw text, engine and confidence.
- Validation: schema, arithmetic, required fields, duplicate hints, currency/date parsing.
- Python API and local CLI.
- Arabic, English and mixed-script normalization tests.
- Docker-based local deployment.
- Explicit `needs_review` outcome when evidence is insufficient.

## P1

- REST API with asynchronous jobs.
- TypeScript SDK.
- Multiple OCR adapters and adapter comparison.
- Human-review interchange format / optional review UI.
- CSV and JSONL batch export.
- Pluggable locale packs with documented sources.

## Out of scope

- Accounting ledger, billing, payments or tax filing.
- Guaranteed compliance with ZATCA or any jurisdiction.
- Handwriting as a release blocker.
- Hosted multi-tenant SaaS in the first MVP.

## Functional acceptance criteria

| ID | Requirement | Acceptance |
|---|---|---|
| FR-01 | Ingestion | Unsupported MIME and oversized files rejected clearly |
| FR-02 | Header extraction | Schema-valid JSON; unknown values remain null |
| FR-03 | Line items | Preserve row order and cell evidence where available |
| FR-04 | Traceability | Each material field links to raw text and page |
| FR-05 | Arithmetic | Use Decimal; report difference and tolerance |
| FR-06 | Locale | Preserve raw and normalized values |
| FR-07 | Uncertainty | Conflicting/weak evidence produces needs_review |
| FR-08 | Privacy | No external provider call unless configured |
| FR-09 | Reproducibility | Record adapter/model/config versions |
| FR-10 | Extensibility | New OCR adapter does not change public output schema |

## Success metrics

- Field exact match and normalized F1, separately for headers and line items.
- Numeric exact-match rate for totals, tax and quantities.
- Evidence coverage and localization quality.
- Human-review rate.
- Latency and peak memory by hardware profile.
- External integrations, repeat users and merged external contributions.

Do not optimize for GitHub stars alone.

## Validation plan

Interview at least 15 integrators, accountants and SMB operators. Ask about current workflow, monthly document volume, error costs, privacy constraints, languages, and current spend/build effort. Run a permission-based concierge test on 30–50 documents. Publish only synthetic or explicitly redistributable data.

## Risks

- Confident OCR errors → evidence, deterministic checks and review.
- Jurisdiction-specific tax rules → separate versioned locale packs; no universal assumptions.
- Dataset bias → disclose provenance and limitations.
- Model license restrictions → maintain an adapter/model license matrix.
- Sensitive documents → local-first, safe logs and bounded retention.
