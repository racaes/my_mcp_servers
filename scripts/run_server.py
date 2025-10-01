"""Generic launcher for any MCP server registered in config/mcp_servers.toml."""

from __future__ import annotations

import asyncio
from importlib import import_module
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

try:  # Python 3.11+ provides tomllib in stdlib
    import tomllib  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for older interpreters
    import tomli as tomllib  # type: ignore


app = typer.Typer(help="Launch any MCP server defined in config/mcp_servers.toml")
console = Console()


def _load_registry(path: Path) -> dict[str, dict[str, str]]:
    data = tomllib.loads(path.read_text("utf-8"))
    return {key: value for key, value in data.items() if isinstance(value, dict)}


def _resolve_entrypoint(script: str):
    module_name, _, attr = script.partition(":")
    module = import_module(module_name)
    if not attr:
        raise ValueError(f"Script entrypoint must include attribute: {script}")
    return getattr(module, attr)


@app.command()
def main(
    name: Optional[str] = typer.Argument(None, help="Name of the server in mcp_servers.toml"),
    registry: Path = typer.Option(
        Path("config/mcp_servers.toml"),
        "--registry",
        "-r",
        help="Path to the MCP server registry file.",
    ),
) -> None:
    """Launch a server registered in the shared configuration."""

    if not registry.exists():
        raise typer.BadParameter(f"Registry file not found: {registry}")

    servers = _load_registry(registry)

    if name is None:
        table = Table(title="Available MCP servers")
        table.add_column("Key", style="cyan")
        table.add_column("Label", style="green")
        table.add_column("Protocol", justify="center")
        for key, payload in servers.items():
            table.add_row(key, payload.get("label", ""), payload.get("protocol", ""))
        console.print(table)
        raise typer.Exit()

    if name not in servers:
        raise typer.BadParameter(f"Server '{name}' not found in {registry}")

    entry = servers[name]
    script = entry.get("script")
    if not script:
        raise typer.BadParameter(f"Server '{name}' is missing a script entry")

    func = _resolve_entrypoint(script)

    config_path = entry.get("config")
    host = entry.get("http_host")
    port = entry.get("http_port")
    protocol = entry.get("protocol", "stdio")

    kwargs = {}
    if config_path:
        kwargs["config_path"] = Path(config_path)
    if host:
        kwargs["host"] = host
    if port:
        kwargs["port"] = int(port)
    if protocol:
        kwargs["protocol"] = protocol

    # Ensure non-interactive execution by default when using Typer-powered launchers.
    kwargs.setdefault("auto_confirm", True)

    console.print(f"Launching {name} via {script} with protocol {protocol}")

    try:
        result = func(**kwargs)
    except typer.Exit as exc:  # pragma: no cover - Typer handles exits via exceptions
        if exc.exit_code not in (0, None):
            raise
        return

    if asyncio.iscoroutine(result):
        asyncio.run(result)


if __name__ == "__main__":
    app()
