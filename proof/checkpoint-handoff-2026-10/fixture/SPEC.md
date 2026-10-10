# Cross-agent checkpoint qualification
Build a dependency-free Python function `slugify(label: str) -> str` in slug.py.
Phase plan: create PLAN.json and DECISIONS.md, with four phase ids plan, ascii,
unicode, verification. Each phase contains one task with the same id, acceptance,
files, and verification commands. Preserve these ids throughout the workflow.
Phase ascii: lowercase ASCII; collapse spaces, underscores and punctuation into
hyphens; trim outer hyphens. Phase unicode: use Unicode NFKD to transliterate
accented Latin letters to ASCII; remove combining marks. After normalization,
any character outside [a-z0-9] becomes a separator (so Straße becomes stra-e). Reject non-string
input with TypeError; reject empty or punctuation-only results with ValueError.
No network or dependencies in slug.py. Keep the public API stable. DECISIONS.md
must record NFKD, stdlib only, explicit invalid-input errors, and saved-state
handoff as constraints. Claude implements only the ASCII baseline, then exits.
Codex continues the Unicode/invalid-input work from Companion's saved state.
The independent operator runs final validation and closes verification.
