from app.paging import page_count


def results_page(results, page, per_page=10):
    """Return (rows, has_next) for a 1-based page number."""
    start = (page - 1) * per_page
    rows = results[start:start + per_page]
    return rows, page < page_count(len(results), per_page)
