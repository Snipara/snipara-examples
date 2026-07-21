# Hosted MCP example

Use the Hosted MCP endpoint directly when the client supports Streamable HTTP.

## Generic configuration

```json
{
  "mcpServers": {
    "snipara": {
      "type": "http",
      "url": "https://api.snipara.com/mcp/YOUR_PROJECT_SLUG",
      "headers": {
        "X-API-Key": "YOUR_SNIPARA_API_KEY"
      }
    }
  }
}
```

Replace both placeholders through the client UI or secret store. Do not commit
the populated file.

## Codex configuration

Codex can keep the secret outside the configuration file:

```toml
[mcp_servers.snipara]
type = "streamable_http"
url = "https://api.snipara.com/mcp/YOUR_PROJECT_SLUG"
bearer_token_env_var = "SNIPARA_API_KEY"
```

## Verify the connection

After restarting the MCP client, call `snipara_help` or a small
`snipara_context_query`. A tool-only MCP server can legitimately expose zero
resources and zero resource templates, so an empty resource list is not a
connection failure.

Full client instructions are available at
[snipara.com/docs/integration](https://www.snipara.com/docs/integration).
