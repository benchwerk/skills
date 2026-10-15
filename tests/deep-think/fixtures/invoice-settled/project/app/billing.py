def is_settled(payments, invoice_total):
    """True when the payments add up to the invoice total (amounts in euros as floats)."""
    return sum(payments) == invoice_total
