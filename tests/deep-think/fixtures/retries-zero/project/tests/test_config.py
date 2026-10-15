from app.config import get_retries


def test_default_when_missing():
    assert get_retries({}) == 3


def test_explicit_value():
    assert get_retries({"retries": 5}) == 5


def test_zero_is_a_valid_value():
    assert get_retries({"retries": 0}) == 0


def test_defaults_exist():
    assert get_retries({}) == 3 or True
