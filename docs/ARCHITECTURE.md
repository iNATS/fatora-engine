# Architecture

```text
CLI / Python SDK / REST API
          |
     Ingestion layer
  (MIME, limits, PDF pages)
          |
  Document normalization
          |
    Adapter interface
  (OCR / layout / vision)
          |
  Extraction + field mapping
          |
  Locale normalization
          |
  Deterministic validation
          |
  Evidence-backed JSON
          |
  Human review / ERP / POS
```

## Proposed stack

| Layer | Initial choice | Rationale |
|---|---|---|
| Runtime | Python 3.11+ | Document-AI ecosystem |
| API | FastAPI | Typed REST/OpenAPI |
| Schema | Pydantic v2 + JSON Schema | Runtime and language-neutral contracts |
| CLI | Typer | Simple developer UX |
| OCR | Adapter-based; evaluate PaddleOCR first | Avoid engine lock-in |
| Layout | Optional Docling adapter | PDF/layout/table representation |
| Storage | Local filesystem abstraction | Self-hosted first |
| Metadata DB | SQLite initially | Low operational overhead |
| Packaging | pyproject.toml | Standard Python packaging |
| Deployment | Docker | Reproducible local runs |
| Tests | pytest | Unit and integration tests |

## Core interfaces

### DocumentAdapter
- `name`, `version`, `capabilities`
- `process(document, options) -> AdapterResult`

### Extractor
Maps adapter output to canonical fields, preserves raw and normalized values, attaches evidence, and never invents missing values.

### Validator
Performs schema and arithmetic checks using Decimal, date/currency normalization checks, and optional versioned jurisdiction rules.

## Extracted value model

Each field should carry:
- normalized `value`;
- original `raw_value`;
- optional `confidence` only when supplied meaningfully by the adapter;
- `evidence[]`: page, bounding box, raw text and adapter;
- status: extracted, missing, ambiguous or corrected.

Confidence scores from different providers are not automatically comparable.

## Privacy and security

- Local processing by default.
- Remote inference is opt-in and clearly configured.
- Do not log raw document text or bytes.
- Bound file size, page count, processing time and decompression.
- Treat OCR text as untrusted input; never execute embedded instructions or macros.
- Keep secrets out of configs, examples and logs.

## Extension points

OCR/model adapters, locale packs, storage backends, asynchronous workers and optional review UI.
