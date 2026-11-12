from fastapi import FastAPI, HTTPException, Request
from fatora import __version__
from fatora.documents import DEFAULT_MAX_BYTES, DocumentValidationError, validate_document

app = FastAPI(
    title="Fatora API",
    version=__version__,
    description=(
        "Open-source invoice and receipt extraction. OCR extraction is not "
        "implemented yet; document validation is available."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/v1/documents/validate")
async def validate_uploaded_document(request: Request) -> dict[str, object]:
    """Validate a raw PDF/image request body without persisting its contents.

    Pass the original filename in the X-Filename header. The body is streamed
    with a hard limit so a large upload is rejected before being fully buffered.
    """
    filename = request.headers.get("x-filename", "")
    declared_type = request.headers.get("content-type")
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > DEFAULT_MAX_BYTES:
                raise HTTPException(status_code=413, detail="Document exceeds upload limit.")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.")

    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > DEFAULT_MAX_BYTES:
            raise HTTPException(status_code=413, detail="Document exceeds upload limit.")

    try:
        document = validate_document(
            filename,
            bytes(body),
            declared_media_type=declared_type,
        )
    except DocumentValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "valid": True,
        "filename": document.filename,
        "media_type": document.media_type,
        "size_bytes": document.size_bytes,
        "sha256": document.sha256,
    }


@app.post("/v1/extract")
def extract_not_implemented() -> None:
    raise HTTPException(
        status_code=501,
        detail="OCR and invoice extraction are not implemented yet.",
    )
