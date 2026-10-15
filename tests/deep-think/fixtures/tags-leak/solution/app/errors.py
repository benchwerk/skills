def collect_error(message, errors=None):
    """Return a list with message added to the given errors (or to a new list)."""
    if errors is None:
        errors = []
    errors.append(message)
    return errors
