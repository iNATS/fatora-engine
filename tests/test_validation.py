from decimal import Decimal
from fatora.validation import validate_totals


def test_totals_pass():
    result = validate_totals(Decimal("100.00"), Decimal("15.00"), Decimal("115.00"))
    assert result["status"] == "passed"


def test_totals_fail():
    result = validate_totals(Decimal("100.00"), Decimal("15.00"), Decimal("116.00"))
    assert result["status"] == "failed"
