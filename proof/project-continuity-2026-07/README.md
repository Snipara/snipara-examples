# Project continuity proof replay — July 2026

This directory mirrors the measured summary published at
[`snipara.com/proof`](https://www.snipara.com/proof). It is useful evidence for
one narrow claim: project decisions, workflow state, impact context, and
verification evidence can change what a coding agent discovers before its first
edit and how it performs on continuity-dependent scenarios.

It is intentionally not mixed into the June hosted-context benchmark. The
source repository belongs to Snipara, the scenarios depend on project history,
and a negative-control class has not yet been published.

## Repository replay

The same engineering task was replayed from the commit before the work began:

- task: Complete Safe Parallel Coding MVP5/MVP6
- base: `499d63a3`
- answer-key final commit: `9785471a`
- answer key: 14 commits, 76 changed files, 5,475 insertions, 270 deletions,
  and 31 test/support files
- cold discovery: 16 searches, 1,722 unique search hits, 47 files opened,
  5 of the 76 final changed files found, and 3 of 7 surface categories found
- Snipara start package: 3 project-intelligence artifacts, 5 anchor files plus
  phase surfaces, and all 7 of 7 surface categories found

No time-to-plan claim is made because comparable raw timestamps were not
preserved.

## Continuity-dependent coding scenarios

The public proof page reports six controlled scenarios with ten paired
repetitions per model. Provider/runtime groups stay separate:

| Runtime group | Cold passes | With Snipara |
| --- | ---: | ---: |
| Local models | 0 / 180 | 170 / 180 |
| Codex CLI | 25 / 180 | 179 / 180 |
| Claude | 7 / 120 | 120 / 120 |

See [`results.json`](./results.json) for the model-level values and deterministic
quality/continuity scores copied from the public proof page.

## Limits

- These are six continuity-heavy coding scenarios, not a general coding suite.
- The public comparison is cold repository context versus Hosted Snipara
  retrieval; the continuity-local condition is an oracle ceiling control and is
  not included here.
- The proof uses Snipara-owned work, so external comparative pilots remain the
  stronger next validation.
- A negative control where cold agents already succeed has not yet been
  published. No broad coding uplift is claimed until that control exists.
- Local, Codex CLI, and Claude results use different runtimes and must not be
  presented as a global model ranking.

`results.json` is a machine-readable copy of the published summary, not a raw
trace bundle. The canonical methodology and caveats remain the public proof page.
