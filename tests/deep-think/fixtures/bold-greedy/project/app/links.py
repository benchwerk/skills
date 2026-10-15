import re


def first_link(html):
    """Return the target of the first <a href="..."> in html, or None."""
    match = re.search(r'<a href="(.*)">', html)
    return match.group(1) if match else None
