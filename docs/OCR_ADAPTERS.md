# OCR adapters

Fatora keeps OCR engines optional and provider-neutral. The first executable
adapter is Tesseract, invoked through its local command-line binary.

## Tesseract adapter

The adapter is intended as a low-dependency CPU baseline for printed Arabic and
English text. It accepts PNG, JPEG and TIFF images, sends the in-memory bytes to
the local Tesseract process over stdin, and parses TSV output into line-level
`TextBlock` values with page numbers and normalized confidence.

### Install

Install Tesseract 5 and the Arabic and English trained data using your operating
system package manager. Package names vary by distribution; common Debian/Ubuntu
packages are:

```bash
sudo apt-get install tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng
```

No Python package is required for this adapter. The `tesseract` executable must
be available on PATH. The adapter defaults to `ara+eng`; override the language
string when constructing it if needed.

### Use

```python
from fatora.documents import validate_document
from fatora.ocr.tesseract import TesseractAdapter

document = validate_document(
    "invoice.png",
    image_bytes,
    declared_media_type="image/png",
)
result = TesseractAdapter(languages="ara+eng").extract(document)
```

The source bytes are passed through stdin. This adapter does not write the
document to disk, call a remote service, or log OCR text. A configurable timeout
bounds the subprocess runtime.

## Current limits

- PDF input is not supported by this adapter yet; PDF rasterization needs a
  separate bounded page-count and resource-limited stage.
- Tesseract's output is line-level text, not table structure or semantic layout.
- Confidence is the mean of Tesseract word confidence values for each line;
  confidence values are engine-specific and must not be compared directly with
  other providers.
- Mixed Arabic/English reading order and numeric grouping must be evaluated on
  a representative, permissioned invoice set before production use.
- Installing the engine does not guarantee the best Arabic invoice accuracy.
  Compare it with PaddleOCR on the same redacted or synthetic benchmark.

## Engine selection notes

Tesseract is the initial lightweight baseline because it is CPU-oriented, has
an Apache-2.0 engine license, and provides Arabic and English trained data.
PaddleOCR is the next candidate for a benchmark: its repository is Apache-2.0
and its current multilingual model family includes Arabic. Its runtime and model
footprint are larger, so it should remain an optional adapter rather than a
mandatory dependency.

Do not treat either engine's license as automatically covering every model
artifact, training dataset, or downstream deployment. Recheck the exact
third-party model/data terms before bundling weights or redistributing them.
