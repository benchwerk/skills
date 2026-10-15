from app.billing import is_settled
from app.refunds import fully_refunded


def test_primary_float_sums():
    assert is_settled([0.1, 0.2], 0.3) is True
    assert is_settled([0.1, 0.7], 0.8) is True


def test_regression_still_detects_a_difference_of_one_cent():
    assert is_settled([0.1, 0.2], 0.31) is False
    assert is_settled([19.99], 20.00) is False


def test_second_refunds():
    assert fully_refunded([0.1, 0.2], 0.3) is True
    assert fully_refunded([0.1, 0.2], 0.31) is False


def test_regression_exact_and_under():
    assert is_settled([10.0], 10.0) is True and is_settled([0.1], 0.3) is False
