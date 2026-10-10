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
    - Normalize Unicode with NFKD and remove combining marks
    - Lowercase all ASCII letters
    - Collapse spaces, underscores, and punctuation into single hyphens
    - Trim outer hyphens

    Args:
        label: The string to slugify

    Returns:
        The slugified string

    Raises:
        TypeError: If input is not a string
        ValueError: If the result is empty
    """
    if not isinstance(label, str):
        raise TypeError('label must be a string')

    label = unicodedata.normalize('NFKD', label).lower()
    result = []
    prev_was_separator = False

    for char in label:
        if unicodedata.category(char).startswith('M'):
            continue
        if 'a' <= char <= 'z' or '0' <= char <= '9':
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
        raise ValueError('label must contain letters or digits that normalize to ASCII')

    return slug
