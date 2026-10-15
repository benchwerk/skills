from app.config import get_retries
from app.logging_config import get_verbosity


def test_primary_zero_retries():
    assert get_retries({"retries": 0}) == 0


def test_second_zero_verbosity():
    assert get_verbosity({"verbosity": 0}) == 0


def test_regression_defaults_and_values():
    assert get_retries({}) == 3 and get_retries({"retries": 5}) == 5
    assert get_verbosity({}) == 1 and get_verbosity({"verbosity": 2}) == 2
