# Security

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository. Do not
open a public issue containing credentials, private project data, or an
unpatched security finding.

## Example safety rules

- Use placeholders for project slugs and API keys.
- Load secrets from environment variables or the MCP client's secret store.
- Never commit `.env` files, access tokens, raw production logs, or customer
  benchmark data.
- Treat benchmark outputs as public before adding them to an evidence pack.

