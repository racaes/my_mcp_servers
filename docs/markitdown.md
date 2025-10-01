# MarkItDown MCP Server

This document captures implementation details for the bundled MarkItDown server wrapper.

## Purpose

- Provide a convenient entrypoint (`scripts/run_markitdown.py`) that supports
  both STDIO (for Copilot agent integrations) and HTTP (for custom tooling).
- Offer reusable configuration via `servers/markitdown/config.toml` and
  fleet-wide overrides under `config/mcp_servers.toml`.

## Dependencies

| Package           | Reason                                                   |
|-------------------|----------------------------------------------------------|
| `markitdown-mcp`  | Official Microsoft launcher for the MarkItDown MCP      |
| `markitdown`      | Underlying conversion logic (transitive via the MCP CLI) |
| `mcp`             | Core Model Context Protocol types and utilities          |
| `typer`           | User-friendly CLI definition for launch scripts          |
| `rich`            | Console UX upgrades (tables, prompts)                    |
| `pydantic`        | Structured configuration loading                         |

## STDIO Transport

The launcher spawns the upstream MarkItDown MCP executable defined in the
configuration file. By default it runs:

```bash
python -m markitdown_mcp
```

The wrapper simply forwards stdio to the parent process so the MCP transport
is identical to running the upstream package directly.

## HTTP Transport

When HTTP is requested, the launcher appends `--http`, `--host`, and `--port`
flags before delegating to `markitdown-mcp`. This leverages the FastMCP-based
HTTP/SSE support already included with the upstream package.

## Configuration Layers

1. `servers/markitdown/config.toml` – Source of truth for server-local defaults
2. `config/mcp_servers.toml` – Registry consumed by the generic launcher and VS Code
3. CLI options – Final override when invoking scripts manually or through tasks

Use `tomli-w` or standard `tomllib` to edit these files programmatically.

## Operational Tips

- Prefer overriding the `command` array in `config.toml` if you pin
  `markitdown-mcp` to a custom virtual environment.
- Use the shared registry (`config/mcp_servers.toml`) to keep VS Code and
  launch scripts aligned on host/port choices.
