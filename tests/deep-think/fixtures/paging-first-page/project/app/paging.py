def page_slice(items, page, size):
    """Return the items on a 1-based page."""
    start = page * size
    return items[start:start + size]


def page_count(total, size):
    """Number of pages needed for total items."""
    return -(-total // size)
