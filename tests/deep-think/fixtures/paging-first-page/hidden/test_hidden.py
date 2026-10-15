from app.paging import page_count, page_slice
from app.search import results_page

ITEMS = list(range(25))


def test_primary_first_page():
    assert page_slice(ITEMS, 1, 10) == list(range(10))


def test_primary_last_partial_page():
    assert page_slice(ITEMS, 3, 10) == [20, 21, 22, 23, 24]


def test_second_results_first_page():
    rows, has_next = results_page(ITEMS, 1, 10)
    assert rows == list(range(10)) and has_next is True


def test_second_results_last_page():
    rows, has_next = results_page(ITEMS, 3, 10)
    assert rows == [20, 21, 22, 23, 24] and has_next is False


def test_regression_page_count():
    assert page_count(25, 10) == 3 and page_count(20, 10) == 2
