def remove_empty(groups):
    """groups maps name -> list. Remove groups whose list is empty; return the mapping."""
    for name in groups:
        if not groups[name]:
            groups.pop(name)
    return groups
