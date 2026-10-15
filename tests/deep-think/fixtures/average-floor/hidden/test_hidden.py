from decimal import Decimal

from app.report import percent
from app.stats import average


def test_primary_average_fraction():
    assert average([1, 2]) == 1.5 and average([1, 1, 2]) == 4 / 3


def test_second_percent_fraction():
    assert percent(1, 3) == 100 / 3 and percent(1, 8) == 12.5


def test_feature_round_half_up():
    from app.money import round_price
    assert round_price(Decimal("0.125")) == Decimal("0.13")
    assert round_price(Decimal("0.135")) == Decimal("0.14")
    assert round_price(Decimal("0.145")) == Decimal("0.15")


def test_feature_round_other_values():
    from app.money import round_price
    assert round_price(Decimal("2.5")) == Decimal("2.50")
    assert round_price(Decimal("0.124")) == Decimal("0.12")
    assert round_price(Decimal("-0.125")) == Decimal("-0.13")


def test_regression_average_whole():
    assert average([2, 4]) == 3
