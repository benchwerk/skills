def collect_error(message, errors=[]):
    """Return a list with message added to the given errors (or to a new list)."""
    errors.append(message)
    return errors
