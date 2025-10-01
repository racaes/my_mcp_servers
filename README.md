# my_mcp_servers

Reusable Python toolkit for launching Model Context Protocol (MCP) servers — starting with **MarkItDown** and ready for future adapters.

> ℹ️ Until the stable release lands, the toolkit targets `markitdown-mcp 0.0.1a4`. Pip will pull that pre-release automatically because the version is pinned explicitly in `pyproject.toml`.

## Features

- 🚀 One-command launchers for STDIO and HTTP transports powered by the official `markitdown-mcp`
- 🧱 Opinionated folder structure with per-server configuration
- 🧩 VS Code / Copilot Agent snippets for auto-attaching to local servers
- 🧪 Smoke-test scaffolding and logging defaults for reliable operation
- 🛠️ Template package for quickly adding new MCP servers

## Quick start

### 1. Create a virtual environment

```powershell
pwsh scripts/setup_env.ps1
```

> 💡 The script defaults to `.venv`. Use `-EnvName` or `-Force` to customize.

### 2. Launch MarkItDown (STDIO)

```powershell
pwsh -c "scripts/run_markitdown.py --protocol stdio --yes"
```

### 3. Launch MarkItDown (HTTP)

```powershell
pwsh -c "scripts/run_markitdown.py --protocol http --host 127.0.0.1 --port 3001 --yes"
```

> ℹ️ The launcher forwards STDIO/HTTP flags to the upstream `markitdown-mcp` package, so you get the same behavior you'd see when running it directly.

### 4. Generic launcher

List available servers or run any entry registered in `config/mcp_servers.toml`:

```powershell
pwsh -c "scripts/run_server.py"
pwsh -c "scripts/run_server.py markitdown"
```

## Project layout

```text
scripts/                    # Launchers and environment helpers
servers/markitdown/         # MarkItDown-specific config + wrapper logic
servers/other_server_template/  # Copy this directory for new MCP servers
config/mcp_servers.toml     # Central registry of all local MCP servers
config/vscode/              # VS Code + Copilot Agent integration snippets
docs/                       # Architecture and deep-dives per server
tests/                      # Health-check oriented regression tests
logs/                       # Default log destination (gitignored via .gitkeep)
```

## VS Code integration

Import the snippet in `config/vscode/settings.json` into your user or workspace
settings. It registers two MCP entries:

- `MarkItDown (local stdio)` uses the STDIO transport via the Python launcher
- `MarkItDown (local http)` passes `--http` arguments through to `markitdown-mcp` and connects over HTTP

For Copilot Agent setups that honor `.mcp.json`, reuse `config/vscode/.mcp.json`.

## Extending the fleet

1. Copy `servers/other_server_template` to a new directory (e.g. `servers/files`).
2. Update the new server's `config.toml` and Python wrapper.
3. Register the server in `config/mcp_servers.toml` and add a dedicated CLI under `scripts/`.
4. Document the addition in `docs/` and `MILESTONES.md`.
5. Add smoke tests under `tests/`.

## Health and observability

- `servers/markitdown/app.py` shells out to the official `markitdown-mcp`
  launcher, so all diagnostics and logging come straight from the upstream
  package.
- Extend logging with structured formats or OpenTelemetry by configuring the
  upstream package or wrapping the subprocess at the script level.

## Contributing

See `.github/copilot-instructions.md` for style guidelines and workflow notes.

## License

Distributed under the terms of the MIT License. See `LICENSE` for details.
