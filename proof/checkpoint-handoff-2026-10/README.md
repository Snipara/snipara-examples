# Claude Code → saved checkpoint → fresh Codex

The agent can change. The work continues.

This public fixture retains the inputs, commands, validator and results of one
controlled Companion handoff. It also contains one matched continuation with and
without Snipara. It is a development demonstration, not a reliability study.

## What actually ran

On October 10, 2026, native Claude Code (Haiku 4.5) created `PLAN.json`, recorded
`DECISIONS.md`, implemented the ASCII baseline and completed the first two phases
with published Companion 3.7.0. A fresh native Codex session resumed the saved
`unicode` phase. A separate operator checked the candidate and protected files,
then closed the verification phase. See [`original-result.json`](original-result.json).

The paired test reuses that frozen Claude-produced input. It does **not** rerun
Claude for each arm. Both fresh Codex sessions receive identical ordinary source,
plan, decisions and six-case ASCII evidence. The Snipara arm additionally receives
the saved workflow and access to the project's Hosted MCP. The baseline has no
Snipara credentials or state, but can infer progress from all the ordinary files.
Neither session receives the earlier agent's conversation.

The checkpoint fixture preserves completed phases, tasks, attempts and receipts.
Only absolute paths are rebased and private coordination telemetry and memory
identifiers are removed/redacted. `manifest.json` seals these public inputs.

## Measured paired result

Same gpt-6.1-sol model, low reasoning effort, common prompt, eight-call requested
budget, 210-second process timeout. Baseline ran first; one pair only.

| Observation                                  | Ordinary files | Files + Snipara checkpoint/MCP |
| -------------------------------------------- | -------------: | -----------------------------: |
| Independent validation                       |          21/21 |                          21/21 |
| Full agent session                           |       30.936 s |                       55.630 s |
| Successful `workflow resume` command         | Not applicable |                        2.380 s |
| Separate successful Hosted MCP probe         | Not applicable |                        1.063 s |
| Client-reported input tokens (cumulative)    |         84,640 |                        152,376 |
| Cached input tokens (included above)         |         73,728 |                        134,784 |
| Output tokens                                |          1,163 |                          1,572 |
| Shell commands completed/failed              |          2 / 0 |                          4 / 1 |
| Plan, decisions, original evidence unchanged |            Yes |                            Yes |

Both candidates passed. The baseline inferred progress; Companion explicitly
restored `unicode` and two completed tasks. **This pair shows no speed or token
saving.** The Snipara session includes one failed hosted probe in its restricted
sandbox and a retry through the native automatic approval reviewer. Successful
probe/resume timings exclude the failed attempt; its separate duration was not
recorded. We retain the retry instead of rerunning until a favorable result.

The command time includes hosted session-context retrieval. It is not time to
first useful progress or total harness overhead. Session duration includes code
implementation, tool calls and the permission retry. Tokens are client-reported
and cumulative across calls, not unique prompt size. Billing is unavailable.
Snapshots prove original files/records were preserved; they do not measure how
many tasks the model avoided redoing. Those metrics remain `null` in
[`paired-result.json`](paired-result.json), rather than invented zeros.

## Verify the published candidates (no account or model call)

```bash
git clone https://github.com/Snipara/snipara-examples.git
cd snipara-examples/proof/checkpoint-handoff-2026-10
python3 verify_results.py
```

This recomputes input and solution hashes and runs the same external 21-case
validator against both committed candidates. It cannot independently reproduce
historical durations, billing or token counts.

## Run a new paired continuation

Requires Python 3.11+, Node.js, a logged-in native Codex CLI distribution that
supports `exec --approve-for-me` (the automatic approval review/workspace-write
mode used here), and an environment-backed key for **your own** Snipara project.
Check `codex exec --help` first. The runner refuses incompatible clients; never
replace approval review with a sandbox bypass.

```bash
npm install --prefix /tmp/checkpoint-companion snipara-companion@3.7.0
export COMPANION_BIN=/tmp/checkpoint-companion/node_modules/.bin/snipara-companion
export CODEX_BIN=codex
export SNIPARA_PROJECT_ID=YOUR_PROJECT_SLUG
# Export SNIPARA_API_KEY from your secret manager; never commit or print it.
python3 run.py --model YOUR_CODEX_MODEL --output /tmp/checkpoint-pair-NEW
```

Use a fresh output directory every time. `--order snipara-first` is available for
future order controls, but do not rewrite this historical baseline-first pair.
Native session logs, stderr and full resume context stay under `control/` locally
and can contain private hosted context: **do not publish them without review**.
The generated aggregate `result.json` has no keys, private context or transcripts.
Inspect failures and publish their sanitized outcomes, not just successful reruns.

`driver.py resume` performs a real HTTPS `tools/list` probe against
`https://api.snipara.com/mcp/$SNIPARA_PROJECT_ID` and calls the real installed
`workflow resume --include-session-context --json`. It prints the available
context to the producing agent, rather than synthesizing a successful resume.
The controller runs `validator.py` only after each producing session exits and
checks that protected files and validation source were unchanged. The producing
agent is instructed to edit only `slug.py` and `artifacts/HANDOFF.json`.

This rerun stops after validating the paired continuations. It deliberately leaves
workflow phase completion to the operator; it does not claim to reproduce the
original four-phase final-commit lifecycle. The original bounded four-phase
handoff and this paired continuation are separate records.

## Scope

Resume requires the project folder, saved `.snipara` state, referenced workflow
artifacts **and** the project's Snipara MCP. This does not qualify live-process
migration, restoration from MCP alone, Orchestrator controller transfer,
authenticated human acceptance, broad reliability, or universal performance gains.
These capabilities were not exercised; untested does not mean unsupported.
