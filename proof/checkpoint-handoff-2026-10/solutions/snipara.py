"""
Slugify function for converting labels to URL-friendly slugs.

Phases:
- ASCII (Claude): Lowercase ASCII, collapse separators, trim outer hyphens
- Unicode (Codex): Add NFKD normalization for Unicode characters
- Verification (Operator): Final validation
"""


import unicodedata

def slugify(label: str) -> str:
    """
    Convert a label into a URL-friendly slug.

    Implementation:
    - Normalize with NFKD and remove combining marks
    - Lowercase all ASCII letters
    - Collapse spaces, underscores, and punctuation into single hyphens
    - Trim outer hyphens

    Args:
        label: The string to slugify

    Returns:
        The slugified string

    Raises:
        TypeError: If input is not a string
        ValueError: If result is empty or contains only punctuation
    """
    if not isinstance(label, str):
        raise TypeError("label must be a string")

    normalized = unicodedata.normalize("NFKD", label)
    normalized = ''.join(
        char for char in normalized
        if not unicodedata.category(char).startswith("M")
    ).lower()

    result = []
    prev_was_separator = False

    for char in normalized:
        if "a" <= char <= "z":
            # Lowercase ASCII letters
            result.append(char.lower())
            prev_was_separator = False
        elif "0" <= char <= "9":
            # Keep digits
            result.append(char)
            prev_was_separator = False
        else:
            # Any other character (space, underscore, punctuation) becomes separator
            if not prev_was_separator and result:
                result.append('-')
                prev_was_separator = True

    # Trim outer hyphens
    slug = ''.join(result).strip('-')

    if not slug:
        raise ValueError("label must contain letters or digits after normalization")

    return slug
