"""Money helpers."""
from decimal import ROUND_HALF_UP, Decimal


def round_price(amount):
    """Round a Decimal to cents, halves going away from zero."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
