Needs file `plugins/anythingllm_mcp_servers.json` following the [MCP Server Specification](https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#using-an-mcp-client):
```json
{
  "mcpServers": {
    "exoscale": {
      "command": "uv",
      "args": [
        "--directory",
        "/app/server/storage/exoscale-mcp-server",
        "run",
        "exoscale-mcp-server.py"
      ]
    "env": {
        "EXO_KEY_NAME": "EXO..."
        "EXO_KEY_SECRET": "Eya1...."
      }
    }
  }
}
```