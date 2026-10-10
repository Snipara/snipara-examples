# Decisions and Constraints

## Source: SPEC.md

1. **NFKD Normalization**: Unicode phase will use Unicode NFKD decomposition to transliterate accented Latin letters to ASCII and remove combining marks.

2. **Stdlib Only**: No external dependencies in slug.py. Implementation must use only Python standard library.

3. **Explicit Invalid-Input Errors**: 
   - TypeError for non-string input
   - ValueError for empty or punctuation-only results

4. **Saved-State Handoff**: 
   - Claude implements ASCII baseline only and exits
   - Codex continues Unicode/invalid-input work from Companion's saved state
   - Operator runs final validation and closes verification

5. **Public API Stability**: Keep the public API of `slugify(label: str) -> str` stable across all phases.

6. **ASCII Phase Requirements**:
   - Lowercase all ASCII letters
   - Collapse spaces, underscores, and punctuation into single hyphens
   - Trim outer hyphens from result

7. **No Network/External Resources**: No network calls or external data sources in slug.py.
