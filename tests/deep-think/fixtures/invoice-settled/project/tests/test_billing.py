from app.billing import is_settled


def test_exact_payment():
    assert is_settled([10.0], 10.0) is True


def test_sum_of_floats():
    assert is_settled([0.1, 0.2], 0.3) is True


def test_underpaid():
    assert is_settled([0.1], 0.3) is False
