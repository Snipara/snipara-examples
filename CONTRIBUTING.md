# Contributing

Contributions should keep examples reproducible, safe, and narrowly scoped.

Good contributions include:

- sanitized Hosted MCP configuration examples;
- benchmark cases based on public source material;
- deterministic result-verification improvements;
- adapters for additional MCP clients;
- corrections to claims, links, or methodology.

Do not contribute credentials, customer data, private repository content,
production logs, internal runbooks, or unverifiable marketing claims.

Before opening a pull request, run:

```bash
python3 benchmarks/hosted-context-2026-06/verify_results.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

When publishing a new benchmark run, add a new dated directory. Historical
evidence packs are immutable except for clearly documented corrections.

