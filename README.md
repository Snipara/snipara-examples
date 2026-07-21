# snipara-examples

**Reproducible examples and evidence for Snipara Project Intelligence.**

This repository keeps public integration examples, MCP discovery metadata, and
benchmark evidence in one place. It is intentionally small: no customer data,
private runbooks, internal ranking code, or credentials are included.

## Start here

- [`server.json`](./server.json) describes the Hosted MCP server for the
  official MCP Registry.
- [`io.github.Snipara/snipara`](https://registry.modelcontextprotocol.io/v0.1/servers?search=Snipara&limit=100)
  is the published official MCP Registry entry (`1.0.0`).
- [`examples/hosted-mcp`](./examples/hosted-mcp) shows the primary HTTP setup
  path without hard-coding a project or API key.
- [`benchmarks/hosted-context-2026-06`](./benchmarks/hosted-context-2026-06)
  contains the frozen June 19, 2026 context-selection evidence pack and its
  committed [`results.json`](./benchmarks/hosted-context-2026-06/results.json).
- [`proof/project-continuity-2026-07`](./proof/project-continuity-2026-07)
  mirrors the measured summary from the public Project Intelligence proof
  replay, with its owned-repository and negative-control limits kept explicit.

Verify the benchmark evidence with only Python's standard library:

```bash
python3 benchmarks/hosted-context-2026-06/verify_results.py
```

The verifier checks the case manifest hash, case coverage, reported means,
deltas, and token-reduction arithmetic. It does not claim that a live LLM run
will be byte-for-byte deterministic.

## Hosted MCP

Snipara is a Hosted MCP server for project intelligence and context
optimization across AI agents. Each user connects a project-specific endpoint:

```text
https://api.snipara.com/mcp/YOUR_PROJECT_SLUG
```

Authentication is supplied at runtime through `X-API-Key` or a bearer token.
Never commit an API key to this repository.

## What this benchmark does and does not prove

The frozen evidence pack compares focused Snipara context against the first
32,000 tokens of the same indexed documentation corpus on 12 project-context
questions. It preserves case-level scores so the published aggregates can be
independently recomputed.

It is one hosted run per task, not a universal model-quality guarantee. Model
behavior and the live hosted index can change, so future reruns should publish a
new dated evidence pack instead of rewriting the historical result.

## Additional controlled proof

The [Project Intelligence proof replay](https://www.snipara.com/proof) measures a
different question: whether continuity context changes what a coding agent finds
before implementation and whether continuity-heavy scenarios pass across local,
Codex CLI, and Claude runtimes. It is kept separate from the hosted-context
benchmark because it uses a Snipara-owned repository and does not yet include a
negative control where cold agents should already succeed.

## Related projects

- [`snipara-evals`](https://github.com/Snipara/snipara-evals) provides the
  deterministic Project Intelligence scoring library and CLI.
- [`snipara-companion`](https://github.com/Snipara/snipara-companion) provides
  local workflow continuity and code-impact gates.
- [`snipara-memory`](https://github.com/Snipara/snipara-memory) provides the
  standalone open-source memory engine.
- [Snipara documentation](https://www.snipara.com/docs) documents the Hosted
  MCP, Project Intelligence, integrations, and security boundaries.

## License

Apache-2.0. See [`LICENSE`](./LICENSE).
