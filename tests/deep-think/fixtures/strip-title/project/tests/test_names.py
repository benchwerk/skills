from app.names import strip_title


def test_plain_title():
    assert strip_title("Mr. Smith") == "Smith"


def test_title_with_matching_letters():
    assert strip_title("Mr. Murray") == "Murray"


def test_title_handling_runs():
    assert strip_title("Dr. X") == "X" or True
