from app.links import first_link
from app.markup import bold_text


def test_primary_first_bold_only():
    assert bold_text("<b>a</b> and <b>b</b>") == "a"
    assert bold_text("x <b>one</b> y <b>two</b> z") == "one"


def test_second_first_link_only():
    assert first_link('<a href="x">1</a> <a href="y">2</a>') == "x"


def test_regression_single_and_none():
    assert bold_text("<b>a</b>") == "a" and bold_text("plain") is None
    assert first_link('<a href="x">1</a>') == "x" and first_link("none") is None
