# Hosted context benchmark — June 19, 2026

This evidence pack freezes the public summary of a 12-case hosted run comparing:

1. focused context returned by Snipara; and
2. the first 32,000 tokens of the same indexed documentation corpus without
   retrieval.

The generation model was OpenAI GPT-4.1. Each task was run once with natural
assistant prompts. The committed result is therefore a historical observation,
not a universal guarantee or a statistically powered model leaderboard.

## Files

- [`cases.json`](./cases.json) contains the frozen prompts and claim-level
  evaluation targets.
- [`results.json`](./results.json) contains metadata, context statistics,
  reported aggregates, and case-level scores.
- [`verify_results.py`](./verify_results.py) independently recomputes the
  published aggregates and token-reduction arithmetic.

## Reproduce the evidence check

```bash
python3 verify_results.py
```

Expected output:

```text
verified 12 cases: quality +0.854, window tokens -80.26%
```

This command is deterministic and requires no network access or API key.

## Reproduce a live run

The historical run used:

- provider: `openai`
- model: `gpt-4.1`
- generation mode: `natural`
- baseline mode: `window`
- baseline budget: `32000` tokens
- Snipara project: `snipara`
- Snipara context source: Hosted MCP/API
- source checkout: `d19d4756ec1cc9fb1c77f10fa06833bdfcc1e967`

A live rerun requires your own OpenAI and Snipara credentials. Because the model
and hosted index evolve, publish live reruns as a new dated directory with their
own corpus fingerprint and `results.json`; do not overwrite this evidence pack.

## Limits

- One run per task means the result is directional.
- LLM judging is not byte-for-byte deterministic.
- The raw corpus and response transcripts are not published because they came
  from a private product repository; the public pack exposes the prompts,
  claim targets, case-level metrics, aggregate math, and exact run metadata.
- The baseline is a fixed first-window truncation, not a full long-context dump.
- Public claims must remain scoped to this benchmark.
