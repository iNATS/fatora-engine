from fastapi.testclient import TestClient

from fatora.api import app

client = TestClient(app)


def test_validate_document_endpoint_returns_metadata_only():
    response = client.post(
        "/v1/documents/validate",
        content=b"%PDF-1.7\nminimal",
        headers={
            "X-Filename": "invoice.pdf",
            "Content-Type": "application/pdf",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is True
    assert payload["media_type"] == "application/pdf"
    assert "content" not in payload


def test_validate_document_endpoint_rejects_mismatched_mime():
    response = client.post(
        "/v1/documents/validate",
        content=b"%PDF-1.7\nminimal",
        headers={"X-Filename": "invoice.pdf", "Content-Type": "image/png"},
    )
    assert response.status_code == 422


def test_extract_endpoint_remains_explicitly_unimplemented():
    response = client.post("/v1/extract")
    assert response.status_code == 501
