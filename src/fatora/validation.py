from decimal import Decimal
from typing import Any


def validate_totals(
    subtotal: Decimal,
    tax: Decimal,
    total: Decimal,
    *,
    tolerance: Decimal = Decimal("0.01"),
) -> dict[str, Any]:
    """Check the generic subtotal + tax = total equation.

    This is an arithmetic check, not tax-law or accounting compliance advice.
    """
    expected = subtotal + tax
    difference = total - expected
    passed = abs(difference) <= tolerance
    return {
        "rule": "subtotal_plus_tax_equals_total",
        "status": "passed" if passed else "failed",
        "expected_total": str(expected),
        "reported_total": str(total),
        "difference": str(difference),
        "tolerance": str(tolerance),
    }
