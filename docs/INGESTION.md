# Document ingestion and adapter contract

## Current behavior

Sprint 1 adds bounded, in-memory validation for PDF, PNG, JPEG, WebP and TIFF
files. The default maximum size is 15 MiB. The validator checks the file
signature, filename extension and (when supplied) declared MIME type. The API
does not persist the uploaded bytes and returns only document metadata and a
SHA-256 digest.

### HTTP endpoint

Send the raw document bytes to `POST /v1/documents/validate`:

- `X-Filename: receipt.pdf`
- `Content-Type: application/pdf`
- Request body: original file bytes

The endpoint streams the body and stops when the configured size limit is
exceeded. Invalid or unsupported documents return HTTP 422; oversized uploads
return HTTP 413.

## OCR adapter contract

Implementations should satisfy `fatora.adapters.OCRAdapter` and expose:

- a stable adapter name;
- explicit media-type and language capabilities;
- whether layout and table extraction are supported;
- an `extract(document)` method returning text blocks with page numbers,
  optional confidence and optional polygon coordinates.

The core must not assume a particular OCR vendor or model. Provider-specific
dependencies belong in optional adapter packages, not in the core dependency
set.

## Evidence contract

Extracted fields use `ExtractedField` and carry an explicit status:
`extracted`, `missing` or `needs_review`. Values should retain one or more
`Evidence` records with page number, source text, optional confidence and
optional normalized polygon coordinates. Missing values must remain missing;
adapters must not invent values to fill gaps.

## Security and privacy notes

- Treat filenames, MIME headers and document bytes as untrusted input.
- Do not log document contents or extracted personal data.
- Do not send documents to remote OCR services without explicit configuration
  and user authorization.
- The current implementation is memory-only; persistent storage, malware
  scanning, PDF page-count limits and decompression-bomb defenses are still
  required before exposing this endpoint to untrusted public traffic.
- OCR and invoice extraction are not implemented by this sprint. The
  `/v1/extract` endpoint intentionally remains HTTP 501.
