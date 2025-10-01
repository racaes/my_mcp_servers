# Architecture Overview

## Goals

- Centralize reusable Model Context Protocol (MCP) servers in a single Python toolset
- Support both STDIO and HTTP transports so the same server can be consumed by
  editors (VS Code / Copilot Agent) or other local tools
- Provide clear configuration boundaries for server-specific and fleet-wide concerns
- Make future MCP server additions predictable through templates and documentation

## High-Level Layout

```text
my_mcp_servers
├── config              # Shared registry + editor integration snippets
├── docs                # Architectural references and deep-dives
├── servers             # One package per MCP server (MarkItDown, etc.)
├── scripts             # Human-friendly launchers and environment tools
├── tests               # Regression coverage for health checks and config loaders
└── logs                # Centralized logging output (ignored from VCS)
```

## Control Flow

1. **Launch** via `scripts/run_markitdown.py` (or the generic `run_server.py`).
2. The launcher reads server defaults from `servers/<name>/config.toml` and optional
   overrides from `config/mcp_servers.toml`.
3. Depending on the requested protocol, the launcher builds the appropriate
  command line (e.g., `--http`, host, port flags) and delegates to the upstream
  server package.
4. Output is streamed directly from the subprocess to the console so VS Code and
  other clients see the same transport as the upstream server provides.
5. VS Code connects through entries defined in `config/vscode/settings.json` or
   `.mcp.json`, allowing Agent/Copilot to auto-launch or attach to the server.

## Extensibility

- Copy `servers/other_server_template/` to bootstrap new MCP integrations.
- Register the new server inside `config/mcp_servers.toml` so launch scripts and
  VS Code snippets discover it automatically.
- Add CLI wrappers under `scripts/` when custom argument handling is required.
- Document behaviors and data contracts inside `docs/` to keep onboarding friction low.

## Observability and Health

- Smoke tests under `tests/` consume the same configuration to guard against
  regressions in launch scripts.
- Future enhancements can layer on structured logging (JSON) or integration with
  observability stacks such as OpenTelemetry.
