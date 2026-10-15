#!/usr/bin/env python3
"""Builds the 12 coding fixtures for the deep-think test (Part 17).

Each fixture is a tiny Python project with:
  project/   what the model sees: source, a pytest.ini and visible tests (one of them fails because of the planted bug;
             in six fixtures another visible test can never fail)
  hidden/    the test file used only for scoring (never copied into the model's working folder)
  solution/  full replacement files that fix the planted bug in BOTH places, used to prove the fixture is solvable
  task.txt   the prompt given to the model: it describes only the first bug
  meta.json  what was planted

  python build_fixtures.py      -> writes fixtures/<id>/...
  python validate_fixtures.py   -> proves, for every fixture, that the visible symptom fails, the hidden tests fail before and pass after the solution
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "fixtures"
INI = "[pytest]\npythonpath = .\n"

F = []


def fx(**kw):
    F.append(kw)


# 1 ------------------------------------------------------------------ pagination off by one
fx(id="paging-first-page",
   task="The first page of search results comes back empty: page_slice(items, 1, 10) skips the first ten items. Please fix it.",
   primary="app/paging.py::page_slice", second="app/search.py::results_page", cannot_fail=None, trap=None,
   project={
       "app/__init__.py": "",
       "app/paging.py": r'''def page_slice(items, page, size):
    """Return the items on a 1-based page."""
    start = page * size
    return items[start:start + size]


def page_count(total, size):
    """Number of pages needed for total items."""
    return -(-total // size)
''',
       "app/search.py": r'''from app.paging import page_count


def results_page(results, page, per_page=10):
    """Return (rows, has_next) for a 1-based page number."""
    start = page * per_page
    rows = results[start:start + per_page]
    return rows, page < page_count(len(results), per_page)
''',
       "tests/test_paging.py": r'''from app.paging import page_count, page_slice


def test_page_count():
    assert page_count(25, 10) == 3


def test_first_page():
    assert page_slice(list(range(25)), 1, 10) == list(range(10))
''',
   },
   hidden=r'''from app.paging import page_count, page_slice
from app.search import results_page

ITEMS = list(range(25))


def test_primary_first_page():
    assert page_slice(ITEMS, 1, 10) == list(range(10))


def test_primary_last_partial_page():
    assert page_slice(ITEMS, 3, 10) == [20, 21, 22, 23, 24]


def test_second_results_first_page():
    rows, has_next = results_page(ITEMS, 1, 10)
    assert rows == list(range(10)) and has_next is True


def test_second_results_last_page():
    rows, has_next = results_page(ITEMS, 3, 10)
    assert rows == [20, 21, 22, 23, 24] and has_next is False


def test_regression_page_count():
    assert page_count(25, 10) == 3 and page_count(20, 10) == 2
''',
   solution={
       "app/paging.py": r'''def page_slice(items, page, size):
    """Return the items on a 1-based page."""
    start = (page - 1) * size
    return items[start:start + size]


def page_count(total, size):
    """Number of pages needed for total items."""
    return -(-total // size)
''',
       "app/search.py": r'''from app.paging import page_count


def results_page(results, page, per_page=10):
    """Return (rows, has_next) for a 1-based page number."""
    start = (page - 1) * per_page
    rows = results[start:start + per_page]
    return rows, page < page_count(len(results), per_page)
''',
   })

# 2 ------------------------------------------------------------------ mutable default argument
fx(id="tags-leak",
   task="Tags from one request leak into the next one: after add_tag('a'), add_tag('b') returns ['a', 'b'] instead of ['b']. Please fix it.",
   primary="app/tags.py::add_tag", second="app/errors.py::collect_error", cannot_fail="tests/test_tags.py::test_module_imports", trap=None,
   project={
       "app/__init__.py": "",
       "app/tags.py": r'''def add_tag(tag, tags=[]):
    """Return a list with tag added to the given tags (or to a new list)."""
    tags.append(tag)
    return tags
''',
       "app/errors.py": r'''def collect_error(message, errors=[]):
    """Return a list with message added to the given errors (or to a new list)."""
    errors.append(message)
    return errors
''',
       "tests/test_tags.py": r'''from app.tags import add_tag


def test_add_to_given_list():
    assert add_tag("a", ["x"]) == ["x", "a"]


def test_fresh_list_each_call():
    add_tag("a")
    assert add_tag("b") == ["b"]


def test_module_imports():
    assert True
''',
   },
   hidden=r'''from app.errors import collect_error
from app.tags import add_tag


def test_primary_fresh_list_each_call():
    add_tag("a")
    add_tag("b")
    assert add_tag("c") == ["c"]


def test_second_errors_fresh_each_call():
    collect_error("one")
    collect_error("two")
    assert collect_error("three") == ["three"]


def test_regression_given_list_is_extended_and_returned():
    given = ["x"]
    result = add_tag("a", given)
    assert result == ["x", "a"] and result is given


def test_regression_errors_given_list():
    given = ["x"]
    assert collect_error("a", given) == ["x", "a"]
''',
   solution={
       "app/tags.py": r'''def add_tag(tag, tags=None):
    """Return a list with tag added to the given tags (or to a new list)."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
''',
       "app/errors.py": r'''def collect_error(message, errors=None):
    """Return a list with message added to the given errors (or to a new list)."""
    if errors is None:
        errors = []
    errors.append(message)
    return errors
''',
   })

# 3 ------------------------------------------------------------------ integer division + rounding trap
fx(id="average-floor",
   task="average([1, 2]) returns 1 instead of 1.5. Please fix it. Also add round_price(amount) to app/money.py: it takes a Decimal and rounds it to cents, with halves going up (Decimal('0.125') gives Decimal('0.13')).",
   primary="app/stats.py::average", second="app/report.py::percent", cannot_fail=None,
   trap="round() on Decimal rounds half to even; the requirement is half up",
   project={
       "app/__init__.py": "",
       "app/stats.py": r'''def average(values):
    """Mean of a non-empty list of numbers."""
    return sum(values) // len(values)
''',
       "app/report.py": r'''def percent(part, whole):
    """Part as a percentage of whole, for example 1 and 4 give 25.0."""
    return part * 100 // whole
''',
       "app/money.py": r'''"""Money helpers."""
''',
       "tests/test_stats.py": r'''from app.stats import average


def test_average_whole():
    assert average([2, 4]) == 3


def test_average_fraction():
    assert average([1, 2]) == 1.5
''',
   },
   hidden=r'''from decimal import Decimal

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
''',
   solution={
       "app/stats.py": r'''def average(values):
    """Mean of a non-empty list of numbers."""
    return sum(values) / len(values)
''',
       "app/report.py": r'''def percent(part, whole):
    """Part as a percentage of whole, for example 1 and 4 give 25.0."""
    return part * 100 / whole
''',
       "app/money.py": r'''"""Money helpers."""
from decimal import ROUND_HALF_UP, Decimal


def round_price(amount):
    """Round a Decimal to cents, halves going away from zero."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
''',
   })

# 4 ------------------------------------------------------------------ str.strip takes a character set
fx(id="strip-title",
   task="strip_title('Mr. Murray') returns 'urray'. Names that start with the same letters as the title get cut. Please fix it.",
   primary="app/names.py::strip_title", second="app/files.py::base_name", cannot_fail="tests/test_names.py::test_title_handling_runs", trap=None,
   project={
       "app/__init__.py": "",
       "app/names.py": r'''def strip_title(name):
    """Remove a leading 'Mr. ' or 'Dr. ' from a name."""
    for title in ("Mr. ", "Dr. "):
        if name.startswith(title):
            return name.strip(title)
    return name
''',
       "app/files.py": r'''def base_name(filename):
    """Remove the .txt extension from a file name."""
    if filename.endswith(".txt"):
        return filename.strip(".txt")
    return filename
''',
       "tests/test_names.py": r'''from app.names import strip_title


def test_plain_title():
    assert strip_title("Mr. Smith") == "Smith"


def test_title_with_matching_letters():
    assert strip_title("Mr. Murray") == "Murray"


def test_title_handling_runs():
    assert strip_title("Dr. X") == "X" or True
''',
   },
   hidden=r'''from app.files import base_name
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
''',
   solution={
       "app/names.py": r'''def strip_title(name):
    """Remove a leading 'Mr. ' or 'Dr. ' from a name."""
    for title in ("Mr. ", "Dr. "):
        if name.startswith(title):
            return name[len(title):]
    return name
''',
       "app/files.py": r'''def base_name(filename):
    """Remove the .txt extension from a file name."""
    if filename.endswith(".txt"):
        return filename[:-len(".txt")]
    return filename
''',
   })

# 5 ------------------------------------------------------------------ naive and aware datetimes
fx(id="token-expiry",
   task="is_expired('2000-01-01T00:00:00+00:00') crashes with 'can't compare offset-naive and offset-aware datetimes'. Please fix it.",
   primary="app/tokens.py::is_expired", second="app/sessions.py::seconds_left", cannot_fail=None,
   trap="datetime.now() is naive; fromisoformat of a string with an offset is aware",
   project={
       "app/__init__.py": "",
       "app/tokens.py": r'''from datetime import datetime


def is_expired(expires_at):
    """expires_at is an ISO 8601 string with an offset, such as 2026-10-08T10:00:00+00:00."""
    return datetime.fromisoformat(expires_at) < datetime.now()
''',
       "app/sessions.py": r'''from datetime import datetime


def seconds_left(expires_at):
    """Seconds until expires_at (an ISO 8601 string with an offset); negative when past."""
    return (datetime.fromisoformat(expires_at) - datetime.now()).total_seconds()
''',
       "tests/test_tokens.py": r'''from app.tokens import is_expired


def test_past_token_is_expired():
    assert is_expired("2000-01-01T00:00:00+00:00") is True


def test_future_token_is_not_expired():
    assert is_expired("2099-01-01T00:00:00+00:00") is False
''',
   },
   hidden=r'''from app.sessions import seconds_left
from app.tokens import is_expired


def test_primary_expired_with_offsets():
    assert is_expired("2000-01-01T00:00:00+00:00") is True
    assert is_expired("2000-01-01T00:00:00+02:00") is True
    assert is_expired("2099-01-01T00:00:00+05:30") is False


def test_second_seconds_left():
    assert seconds_left("2099-01-01T00:00:00+00:00") > 0
    assert seconds_left("2000-01-01T00:00:00+00:00") < 0


def test_second_far_future_is_big():
    assert seconds_left("2099-01-01T00:00:00+00:00") > 10**9
''',
   solution={
       "app/tokens.py": r'''from datetime import datetime, timezone


def is_expired(expires_at):
    """expires_at is an ISO 8601 string with an offset, such as 2026-10-08T10:00:00+00:00."""
    return datetime.fromisoformat(expires_at) < datetime.now(timezone.utc)
''',
       "app/sessions.py": r'''from datetime import datetime, timezone


def seconds_left(expires_at):
    """Seconds until expires_at (an ISO 8601 string with an offset); negative when past."""
    return (datetime.fromisoformat(expires_at) - datetime.now(timezone.utc)).total_seconds()
''',
   })

# 6 ------------------------------------------------------------------ dict changed size during iteration
fx(id="cache-purge",
   task="drop_expired raises 'RuntimeError: dictionary changed size during iteration' as soon as an entry has expired. Please fix it.",
   primary="app/cache.py::drop_expired", second="app/registry.py::remove_empty", cannot_fail="tests/test_cache.py::test_function_exists", trap=None,
   project={
       "app/__init__.py": "",
       "app/cache.py": r'''def drop_expired(cache, now):
    """cache maps key -> expiry time. Remove entries whose expiry is at or before now; return the cache."""
    for key in cache:
        if cache[key] <= now:
            del cache[key]
    return cache
''',
       "app/registry.py": r'''def remove_empty(groups):
    """groups maps name -> list. Remove groups whose list is empty; return the mapping."""
    for name in groups:
        if not groups[name]:
            groups.pop(name)
    return groups
''',
       "tests/test_cache.py": r'''from app.cache import drop_expired


def test_nothing_expired():
    assert drop_expired({"a": 10}, 5) == {"a": 10}


def test_expired_entries_are_removed():
    assert drop_expired({"a": 1, "b": 10}, 5) == {"b": 10}


def test_function_exists():
    assert drop_expired({}, 1) == {} or True
''',
   },
   hidden=r'''from app.cache import drop_expired
from app.registry import remove_empty


def test_primary_expired_removed():
    assert drop_expired({"a": 1, "b": 10, "c": 5}, 5) == {"b": 10}


def test_primary_same_object_returned():
    cache = {"a": 1}
    assert drop_expired(cache, 5) is cache and cache == {}


def test_second_empty_groups_removed():
    assert remove_empty({"x": [], "y": [1], "z": []}) == {"y": [1]}


def test_regression_nothing_to_remove():
    assert drop_expired({"a": 10}, 5) == {"a": 10}
    assert remove_empty({"y": [1]}) == {"y": [1]}
''',
   solution={
       "app/cache.py": r'''def drop_expired(cache, now):
    """cache maps key -> expiry time. Remove entries whose expiry is at or before now; return the cache."""
    for key in [k for k, expiry in cache.items() if expiry <= now]:
        del cache[key]
    return cache
''',
       "app/registry.py": r'''def remove_empty(groups):
    """groups maps name -> list. Remove groups whose list is empty; return the mapping."""
    for name in [n for n, items in groups.items() if not items]:
        groups.pop(name)
    return groups
''',
   })

# 7 ------------------------------------------------------------------ float equality for money
fx(id="invoice-settled",
   task="is_settled([0.1, 0.2], 0.3) returns False although the payments add up to the invoice. Please fix it.",
   primary="app/billing.py::is_settled", second="app/refunds.py::fully_refunded", cannot_fail=None, trap=None,
   project={
       "app/__init__.py": "",
       "app/billing.py": r'''def is_settled(payments, invoice_total):
    """True when the payments add up to the invoice total (amounts in euros as floats)."""
    return sum(payments) == invoice_total
''',
       "app/refunds.py": r'''def fully_refunded(refunds, order_total):
    """True when the refunds add up to the order total (amounts in euros as floats)."""
    return sum(refunds) == order_total
''',
       "tests/test_billing.py": r'''from app.billing import is_settled


def test_exact_payment():
    assert is_settled([10.0], 10.0) is True


def test_sum_of_floats():
    assert is_settled([0.1, 0.2], 0.3) is True


def test_underpaid():
    assert is_settled([0.1], 0.3) is False
''',
   },
   hidden=r'''from app.billing import is_settled
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
''',
   solution={
       "app/billing.py": r'''def is_settled(payments, invoice_total):
    """True when the payments add up to the invoice total (amounts in euros as floats)."""
    return round(sum(payments) * 100) == round(invoice_total * 100)
''',
       "app/refunds.py": r'''def fully_refunded(refunds, order_total):
    """True when the refunds add up to the order total (amounts in euros as floats)."""
    return round(sum(refunds) * 100) == round(order_total * 100)
''',
   })

# 8 ------------------------------------------------------------------ path traversal
fx(id="upload-path",
   task="A user uploaded a file named '../../etc/passwd' and it was written outside the upload folder. upload_path must refuse names that leave UPLOAD_DIR. Please fix it.",
   primary="app/uploads.py::upload_path", second="app/attachments.py::attachment_path", cannot_fail="tests/test_uploads.py::test_module_has_upload_dir",
   trap="posixpath.join discards the folder when the second part is absolute",
   project={
       "app/__init__.py": "",
       "app/uploads.py": r'''import posixpath

UPLOAD_DIR = "/srv/uploads"


def upload_path(name):
    """Where an uploaded file with this name is stored."""
    return posixpath.join(UPLOAD_DIR, name)
''',
       "app/attachments.py": r'''import posixpath

ATTACHMENT_DIR = "/srv/attachments"


def attachment_path(folder, filename):
    """Where an attachment is stored: ATTACHMENT_DIR/folder/filename."""
    return posixpath.join(ATTACHMENT_DIR, folder, filename)
''',
       "tests/test_uploads.py": r'''import pytest

from app.uploads import UPLOAD_DIR, upload_path


def test_plain_name():
    assert upload_path("report.pdf") == "/srv/uploads/report.pdf"


def test_parent_directory_is_refused():
    with pytest.raises(ValueError):
        upload_path("../secret")


def test_module_has_upload_dir():
    assert UPLOAD_DIR or True
''',
   },
   hidden=r'''import pytest

from app.attachments import attachment_path
from app.uploads import upload_path


@pytest.mark.parametrize("name", ["../secret", "../../etc/passwd", "/etc/passwd", "a/../../b", ".."])
def test_primary_names_that_escape_are_refused(name):
    with pytest.raises(ValueError):
        upload_path(name)


@pytest.mark.parametrize("folder,filename", [("../x", "a.txt"), ("ok", "../../a.txt"), ("/abs", "a.txt"), ("ok", "/etc/passwd")])
def test_second_attachment_names_that_escape_are_refused(folder, filename):
    with pytest.raises(ValueError):
        attachment_path(folder, filename)


def test_regression_good_names_still_work():
    assert upload_path("report.pdf") == "/srv/uploads/report.pdf"
    assert upload_path("a/b.txt") == "/srv/uploads/a/b.txt"
    assert attachment_path("inv", "1.pdf") == "/srv/attachments/inv/1.pdf"
''',
   solution={
       "app/uploads.py": r'''import posixpath

UPLOAD_DIR = "/srv/uploads"


def upload_path(name):
    """Where an uploaded file with this name is stored."""
    path = posixpath.normpath(posixpath.join(UPLOAD_DIR, name))
    if path != UPLOAD_DIR and not path.startswith(UPLOAD_DIR + "/"):
        raise ValueError("name leaves the upload folder")
    if path == UPLOAD_DIR or not name or posixpath.isabs(name):
        raise ValueError("invalid name")
    return path
''',
       "app/attachments.py": r'''import posixpath

ATTACHMENT_DIR = "/srv/attachments"


def attachment_path(folder, filename):
    """Where an attachment is stored: ATTACHMENT_DIR/folder/filename."""
    if posixpath.isabs(folder) or posixpath.isabs(filename):
        raise ValueError("absolute path")
    path = posixpath.normpath(posixpath.join(ATTACHMENT_DIR, folder, filename))
    if not path.startswith(ATTACHMENT_DIR + "/"):
        raise ValueError("name leaves the attachment folder")
    return path
''',
   })

# 9 ------------------------------------------------------------------ greedy regex
fx(id="bold-greedy",
   task="bold_text('<b>a</b> and <b>b</b>') returns 'a</b> and <b>b' but should return 'a'. Please fix it.",
   primary="app/markup.py::bold_text", second="app/links.py::first_link", cannot_fail=None, trap=None,
   project={
       "app/__init__.py": "",
       "app/markup.py": r'''import re


def bold_text(html):
    """Return the text of the first <b>...</b> in html, or None."""
    match = re.search(r"<b>(.*)</b>", html)
    return match.group(1) if match else None
''',
       "app/links.py": r'''import re


def first_link(html):
    """Return the target of the first <a href="..."> in html, or None."""
    match = re.search(r'<a href="(.*)">', html)
    return match.group(1) if match else None
''',
       "tests/test_markup.py": r'''from app.markup import bold_text


def test_single_bold():
    assert bold_text("<b>a</b>") == "a"


def test_two_bold_elements():
    assert bold_text("<b>a</b> and <b>b</b>") == "a"


def test_no_bold():
    assert bold_text("plain") is None
''',
   },
   hidden=r'''from app.links import first_link
from app.markup import bold_text


def test_primary_first_bold_only():
    assert bold_text("<b>a</b> and <b>b</b>") == "a"
    assert bold_text("x <b>one</b> y <b>two</b> z") == "one"


def test_second_first_link_only():
    assert first_link('<a href="x">1</a> <a href="y">2</a>') == "x"


def test_regression_single_and_none():
    assert bold_text("<b>a</b>") == "a" and bold_text("plain") is None
    assert first_link('<a href="x">1</a>') == "x" and first_link("none") is None
''',
   solution={
       "app/markup.py": r'''import re


def bold_text(html):
    """Return the text of the first <b>...</b> in html, or None."""
    match = re.search(r"<b>(.*?)</b>", html)
    return match.group(1) if match else None
''',
       "app/links.py": r'''import re


def first_link(html):
    """Return the target of the first <a href="..."> in html, or None."""
    match = re.search(r'<a href="(.*?)">', html)
    return match.group(1) if match else None
''',
   })

# 10 ----------------------------------------------------------------- version strings sorted as text
fx(id="latest-version",
   task="latest(['1.9.0', '1.10.0']) returns '1.9.0'. Please fix it. Use only the standard library; this project has no dependencies.",
   primary="app/versions.py::latest", second="app/releases.py::sort_releases", cannot_fail="tests/test_versions.py::test_latest_is_callable",
   trap="the third-party 'packaging' library is not available and must not be added",
   project={
       "app/__init__.py": "",
       "app/versions.py": r'''def latest(versions):
    """versions are strings like '1.10.2'. Return the highest one."""
    return sorted(versions)[-1]
''',
       "app/releases.py": r'''def sort_releases(releases):
    """releases are dicts with a 'version' string like '1.10.2'. Return them from lowest to highest version."""
    return sorted(releases, key=lambda release: release["version"])
''',
       "tests/test_versions.py": r'''from app.versions import latest


def test_simple():
    assert latest(["1.0.0", "2.0.0"]) == "2.0.0"


def test_ten_is_higher_than_nine():
    assert latest(["1.9.0", "1.10.0"]) == "1.10.0"


def test_latest_is_callable():
    assert callable(latest) or True
''',
   },
   hidden=r'''from app.releases import sort_releases
from app.versions import latest


def test_primary_numeric_order():
    assert latest(["1.9.0", "1.10.0"]) == "1.10.0"
    assert latest(["2.0.0", "10.0.0", "9.9.9"]) == "10.0.0"


def test_second_sort_releases():
    releases = [{"version": "1.10.0"}, {"version": "1.2.0"}, {"version": "1.9.1"}]
    assert [r["version"] for r in sort_releases(releases)] == ["1.2.0", "1.9.1", "1.10.0"]


def test_regression_simple():
    assert latest(["1.0.0", "2.0.0"]) == "2.0.0"
''',
   solution={
       "app/versions.py": r'''def _key(version):
    return tuple(int(part) for part in version.split("."))


def latest(versions):
    """versions are strings like '1.10.2'. Return the highest one."""
    return max(versions, key=_key)
''',
       "app/releases.py": r'''def sort_releases(releases):
    """releases are dicts with a 'version' string like '1.10.2'. Return them from lowest to highest version."""
    return sorted(releases, key=lambda release: tuple(int(p) for p in release["version"].split(".")))
''',
   })

# 11 ----------------------------------------------------------------- late-binding closure
fx(id="limit-checkers",
   task="make_checkers([1, 10])[0](5) returns True but 5 is above the first limit of 1. All checkers behave like the last one. Please fix it.",
   primary="app/validators.py::make_checkers", second="app/handlers.py::make_greeters", cannot_fail=None, trap=None,
   project={
       "app/__init__.py": "",
       "app/validators.py": r'''def make_checkers(limits):
    """Return one function per limit; each tells whether a value is at most its limit."""
    checkers = []
    for limit in limits:
        checkers.append(lambda value: value <= limit)
    return checkers
''',
       "app/handlers.py": r'''def make_greeters(names):
    """Return one function per name; each returns a greeting for that name."""
    greeters = []
    for name in names:
        greeters.append(lambda: "hello " + name)
    return greeters
''',
       "tests/test_validators.py": r'''from app.validators import make_checkers


def test_last_checker():
    assert make_checkers([1, 10])[1](5) is True


def test_first_checker():
    assert make_checkers([1, 10])[0](5) is False
''',
   },
   hidden=r'''from app.handlers import make_greeters
from app.validators import make_checkers


def test_primary_each_checker_has_its_own_limit():
    c = make_checkers([1, 10, 100])
    assert [f(5) for f in c] == [False, True, True]
    assert [f(50) for f in c] == [False, False, True]


def test_second_each_greeter_has_its_own_name():
    g = make_greeters(["ann", "bo"])
    assert [f() for f in g] == ["hello ann", "hello bo"]


def test_regression_empty_lists():
    assert make_checkers([]) == [] and make_greeters([]) == []
''',
   solution={
       "app/validators.py": r'''def make_checkers(limits):
    """Return one function per limit; each tells whether a value is at most its limit."""
    return [(lambda value, limit=limit: value <= limit) for limit in limits]
''',
       "app/handlers.py": r'''def make_greeters(names):
    """Return one function per name; each returns a greeting for that name."""
    return [(lambda name=name: "hello " + name) for name in names]
''',
   })

# 12 ----------------------------------------------------------------- zero treated as missing
fx(id="retries-zero",
   task="get_retries({'retries': 0}) returns 3, but 0 is a valid setting (no retries). Please fix it; the default when the setting is missing stays 3.",
   primary="app/config.py::get_retries", second="app/logging_config.py::get_verbosity", cannot_fail="tests/test_config.py::test_defaults_exist",
   trap=None,
   project={
       "app/__init__.py": "",
       "app/config.py": r'''def get_retries(settings):
    """Number of retries from the settings dict; 3 when it is not set."""
    return settings.get("retries") or 3
''',
       "app/logging_config.py": r'''def get_verbosity(settings):
    """Verbosity level from the settings dict (0 means quiet); 1 when it is not set."""
    return settings.get("verbosity") or 1
''',
       "tests/test_config.py": r'''from app.config import get_retries


def test_default_when_missing():
    assert get_retries({}) == 3


def test_explicit_value():
    assert get_retries({"retries": 5}) == 5


def test_zero_is_a_valid_value():
    assert get_retries({"retries": 0}) == 0


def test_defaults_exist():
    assert get_retries({}) == 3 or True
''',
   },
   hidden=r'''from app.config import get_retries
from app.logging_config import get_verbosity


def test_primary_zero_retries():
    assert get_retries({"retries": 0}) == 0


def test_second_zero_verbosity():
    assert get_verbosity({"verbosity": 0}) == 0


def test_regression_defaults_and_values():
    assert get_retries({}) == 3 and get_retries({"retries": 5}) == 5
    assert get_verbosity({}) == 1 and get_verbosity({"verbosity": 2}) == 2
''',
   solution={
       "app/config.py": r'''def get_retries(settings):
    """Number of retries from the settings dict; 3 when it is not set."""
    return settings.get("retries", 3)
''',
       "app/logging_config.py": r'''def get_verbosity(settings):
    """Verbosity level from the settings dict (0 means quiet); 1 when it is not set."""
    return settings.get("verbosity", 1)
''',
   })


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for f in F:
        d = OUT / f["id"]
        files = dict(f["project"])
        files["pytest.ini"] = INI
        for rel, text in files.items():
            write(d / "project" / rel, text)
        write(d / "hidden" / "test_hidden.py", f["hidden"])
        for rel, text in f["solution"].items():
            write(d / "solution" / rel, text)
        write(d / "task.txt", f["task"] + "\n")
        meta = {k: f[k] for k in ("id", "primary", "second", "cannot_fail", "trap")}
        write(d / "meta.json", json.dumps(meta, indent=1) + "\n")
    print(f"{len(F)} fixtures written to {OUT}")


if __name__ == "__main__":
    main()
