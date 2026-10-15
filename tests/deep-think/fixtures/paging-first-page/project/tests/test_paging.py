from app.paging import page_count, page_slice


def test_page_count():
    assert page_count(25, 10) == 3


def test_first_page():
    assert page_slice(list(range(25)), 1, 10) == list(range(10))
