def add_tag(tag, tags=None):
    """Return a list with tag added to the given tags (or to a new list)."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
