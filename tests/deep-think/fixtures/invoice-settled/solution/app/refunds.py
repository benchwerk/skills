def fully_refunded(refunds, order_total):
    """True when the refunds add up to the order total (amounts in euros as floats)."""
    return round(sum(refunds) * 100) == round(order_total * 100)
