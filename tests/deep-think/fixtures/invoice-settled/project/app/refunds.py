def fully_refunded(refunds, order_total):
    """True when the refunds add up to the order total (amounts in euros as floats)."""
    return sum(refunds) == order_total
