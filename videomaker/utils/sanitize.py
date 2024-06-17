import re
from cleantext import clean


def sanitize_text(text: str) -> str:

    result = text.replace("+", "plus").replace("&", "and")
    result = clean(result, no_emoji=True, no_urls=True, lower=False)

    link_pattern = r"\[([^\]]+)\]\(<[^>]+>\)"
    result = re.sub(link_pattern, r"\1", result)

    return " ".join(result.split())
