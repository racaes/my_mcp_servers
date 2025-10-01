You are contributing to the **my_mcp_servers** toolkit.

- Prefer small, reviewable pull requests.
- Keep launch scripts idempotent and ensure they work from any project root.
- When adding a new MCP server, copy `servers/other_server_template` and update
  `config/mcp_servers.toml` plus VS Code snippets under `config/vscode/`.
- Update documentation (`docs/`, `README.md`, `MILESTONES.md`) alongside code
  changes so users always have accurate guidance.
- Run the relevant tests (or provide an explanation if they cannot run) before
  marking a change complete.
