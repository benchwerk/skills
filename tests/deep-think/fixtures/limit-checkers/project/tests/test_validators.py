from app.validators import make_checkers


def test_last_checker():
    assert make_checkers([1, 10])[1](5) is True


def test_first_checker():
    assert make_checkers([1, 10])[0](5) is False
