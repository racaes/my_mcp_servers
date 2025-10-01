# Copilot Contribution Guide

Welcome, AI assistant! Please follow these guardrails when proposing changes:

1. **Respect the layout.** Keep MCP server logic inside `servers/<name>` and
   expose user-facing CLIs under `scripts/`.
2. **Keep configuration explicit.** Update `servers/<name>/config.toml` and, if
   needed, the central `config/mcp_servers.toml` whenever you add or rename a
   server.
3. **Ship with tests.** Add or update coverage under `tests/` when changing
   behavior. Smoke tests should confirm `/status` and CLI parsing work.
4. **Document the why.** Update `docs/` or `README.md` with rationale for
   significant changes so humans can track evolving architecture.
5. **Prefer incremental additions.** Avoid refactors that span multiple servers
   in a single change—submit focused pull requests.
