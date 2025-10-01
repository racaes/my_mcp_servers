# Milestones

## ✅ v0.1.0 – MarkItDown foundation

- Scaffolded reusable repo layout for local MCP servers
- Added MarkItDown launcher with STDIO/HTTP support delegating to `markitdown-mcp`
- Documented setup flow, architecture, VS Code integration
- Shipped template package for future MCP servers
- Hardened environment setup script and packaging metadata for clean installs

## 🚧 Upcoming

- Add continuous integration workflow (lint + tests)
- Broaden coverage to include additional MCP servers compatible with VS Code / Copilot
- Package Windows-friendly executables / shortcuts for non-technical users
- Extend tests to exercise `markitdown-mcp` HTTP mode end-to-end
- Publish installation guide for pipx / shortcuts leveraging the setup script automation
- Add status dashboard documenting available MCP servers and their health checks

## 💡 Future ideas

- Add file-processing MCP server (e.g., PDF summarizer / data extraction)
- Provide Docker images for remote hosting of the MCP fleet
- Integrate OpenTelemetry / structured logging for richer observability
- Ship VS Code tasks for launching servers automatically per workspace
