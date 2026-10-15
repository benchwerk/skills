import re


def bold_text(html):
    """Return the text of the first <b>...</b> in html, or None."""
    match = re.search(r"<b>(.*?)</b>", html)
    return match.group(1) if match else None
