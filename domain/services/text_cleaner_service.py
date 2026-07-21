"""Domain logic for text sanitization and input cleaning.

Pure functions — no framework or infrastructure dependencies.
"""

import re


def sanitize_text(text: str) -> str:
    """Remove excessive whitespace and simple HTML/XML tags."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"<.*?>", "", text)
    return text


def validate_text_length(text: str, max_length: int = 1000) -> tuple[bool, str]:
    """Check that *text* is non-empty and does not exceed *max_length*."""
    if not text or text.strip() == "":
        return False, "Input cannot be empty."
    if len(text) > max_length:
        return False, "Input is too long."
    return True, text
