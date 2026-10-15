def remove_empty(groups):
    """groups maps name -> list. Remove groups whose list is empty; return the mapping."""
    for name in [n for n, items in groups.items() if not items]:
        groups.pop(name)
    return groups
