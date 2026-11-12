from fatora.adapters import OCRCapabilities, OCRResult, TextBlock
from fatora.extraction import Evidence, ExtractedField, InvoiceExtraction


def test_adapter_contract_data_types_are_constructible():
    capabilities = OCRCapabilities(
        media_types=("application/pdf", "image/png"),
        languages=("ara", "eng"),
        supports_layout=True,
    )
    result = OCRResult(
        blocks=(TextBlock(text="فاتورة", page=1, confidence=0.98),),
        provider="test-adapter",
    )
    assert "ara" in capabilities.languages
    assert result.blocks[0].text == "فاتورة"


def test_extraction_fields_can_preserve_evidence():
    evidence = Evidence(page=1, text="Total 115.00", confidence=0.97)
    field = ExtractedField(value="115.00", status="extracted", evidence=(evidence,))
    extraction = InvoiceExtraction(
        fields={"total": field},
        source_sha256="a" * 64,
        adapter="test-adapter",
    )
    assert extraction.fields["total"].evidence[0].page == 1
