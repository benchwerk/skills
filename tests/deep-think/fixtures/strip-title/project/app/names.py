def strip_title(name):
    """Remove a leading 'Mr. ' or 'Dr. ' from a name."""
    for title in ("Mr. ", "Dr. "):
        if name.startswith(title):
            return name.strip(title)
    return name
