from app.files import base_name
from app.names import strip_title


def test_primary_names():
    assert strip_title("Mr. Murray") == "Murray"
    assert strip_title("Dr. Dre") == "Dre"
    assert strip_title("Mr. Marrow") == "Marrow"


def test_second_base_name():
    assert base_name("text.txt") == "text"
    assert base_name("notes.txt") == "notes"
    assert base_name("tax.txt") == "tax"


def test_regression_untouched_names():
    assert strip_title("Mrs. Jones") == "Mrs. Jones"
    assert base_name("data.csv") == "data.csv"
    assert strip_title("Mr. Smith") == "Smith"
