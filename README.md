# Fatora Engine

**Open-source invoice and receipt extraction with evidence-backed validation.**

Fatora turns business documents into structured, reviewable data. It is designed for global use, with first-class support for Arabic and mixed right-to-left / left-to-right documents.

> Status: early scaffold. OCR extraction adapters are not implemented yet. No accuracy, tax-compliance, or production-readiness claims are made.

## Why Fatora?

Production document workflows need more than OCR:
- a stable invoice and receipt schema;
- line-item extraction and normalization;
- arithmetic and consistency checks;
- evidence linking each value to its source;
- confidence and human-review signals;
- local/self-hosted processing and explicit control over external providers.

Fatora is an orchestration and validation layer. It integrates existing OCR/document models rather than training a new OCR model in the first release.

## Goals

1. Extract invoice and receipt fields into predictable JSON.
2. Preserve evidence for every material extracted value.
3. Validate totals, line items, currencies and dates.
4. Run locally or self-hosted by default.
5. Support Arabic, English and mixed-script documents.
6. Provide Python SDK, REST API and CLI.

## Non-goals for v0.1

- Accounting, bookkeeping, ERP or POS.
- Tax/legal advice or certification of regulatory compliance.
- Automatic payment execution.
- Training a proprietary OCR model from scratch.
- Silent correction of uncertain values.

## Planned architecture

Ingestion → OCR/layout adapters → extraction → locale normalization → deterministic validation → evidence-backed JSON.

See [PRD](docs/PRD.md), [Architecture](docs/ARCHITECTURE.md), [Roadmap](docs/ROADMAP.md), and [Benchmark protocol](docs/BENCHMARK.md).

## Privacy principles

- Local processing is the default.
- Remote inference adapters must be explicitly enabled by the operator.
- Never log raw document contents.
- Never commit private customer invoices or personal data.
- User documents are not used for training by default.

## Current status

This repository starts with product requirements, architecture, schema and contribution guidance. Extraction is not implemented yet. See the roadmap for milestones and open tasks.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome contributions in Arabic/RTL testing, locale normalization, OCR adapters, validation rules and documentation.

## License

Code: Apache-2.0. Dataset assets and model weights may have separate licenses and must retain provenance and license metadata.
