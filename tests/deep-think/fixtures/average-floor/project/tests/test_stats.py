from app.stats import average


def test_average_whole():
    assert average([2, 4]) == 3


def test_average_fraction():
    assert average([1, 2]) == 1.5
