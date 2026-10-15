def is_settled(payments, invoice_total):
    """True when the payments add up to the invoice total (amounts in euros as floats)."""
    return round(sum(payments) * 100) == round(invoice_total * 100)
