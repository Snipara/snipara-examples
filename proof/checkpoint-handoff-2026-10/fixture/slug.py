"""
Slugify function for converting labels to URL-friendly slugs.

Phases:
- ASCII (Claude): Lowercase ASCII, collapse separators, trim outer hyphens
- Unicode (Codex): Add NFKD normalization for Unicode characters
- Verification (Operator): Final validation
"""


def slugify(label: str) -> str:
    """
    Convert a label into a URL-friendly slug.

    ASCII Phase Implementation:
    - Lowercase all ASCII letters
    - Collapse spaces, underscores, and punctuation into single hyphens
    - Trim outer hyphens

    Args:
        label: The string to slugify

    Returns:
        The slugified string

    Raises:
        TypeError: If input is not a string (future phase)
        ValueError: If result is empty or contains only punctuation (future phase)
    """
    result = []
    prev_was_separator = False

    for char in label:
        if char.isalpha():
            # Lowercase ASCII letters
            result.append(char.lower())
            prev_was_separator = False
        elif char.isdigit():
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

    return slug
