from fastapi import FastAPI, HTTPException
from fatora import __version__

app = FastAPI(
    title="Fatora API",
    version=__version__,
    description="Open-source invoice and receipt extraction. Extraction is not implemented yet.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/v1/extract")
def extract_not_implemented() -> None:
    raise HTTPException(
        status_code=501,
        detail="Document extraction is not implemented in this scaffold yet.",
    )
