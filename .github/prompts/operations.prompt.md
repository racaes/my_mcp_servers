Operational reminders for maintaining the MCP servers toolkit:

- Keep virtual environments project-local (`.venv`) to avoid polluting global Python installs.
- Capture manual launch commands and troubleshooting tips in `docs/` or this prompt file.
- When releasing new servers, document required environment variables and health checks.
- Rotate log files under `logs/` regularly; prefer structured logging when scaling up.
- Update VS Code snippets after changing script names or entrypoints to avoid stale configs.
