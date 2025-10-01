"""CLI for launching and managing the MarkItDown MCP server."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Confirm

from servers.markitdown.app import launch, load_config

app = typer.Typer(help="Launch the MarkItDown MCP server via stdio or HTTP.")
console = Console()

ProtocolOption = typer.Option(
    "stdio",
    "--protocol",
    "-p",
    help="Transport to use when launching the server (stdio or http).",
)


@app.command()
def main(
    protocol: str = ProtocolOption,
    config_path: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a TOML config file (defaults to servers/markitdown/config.toml)",
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Host binding when running in HTTP mode.",
    ),
    port: int = typer.Option(
        3001,
        "--port",
        help="Port binding when running in HTTP mode.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompts (non-interactive mode).",
    ),
) -> None:
    """Launch the MarkItDown MCP server using the requested transport."""

    if protocol not in {"stdio", "http"}:
        raise typer.BadParameter("Protocol must be 'stdio' or 'http'.")

    config = load_config(config_path)

    if protocol == "http":
        config.http.host = host
        config.http.port = port

    if not auto_confirm:
        console.print(
            f"[bold green]About to launch MarkItDown ({protocol.upper()})[/bold green]"
        )
        if not Confirm.ask("Continue?", default=True):
            console.print("[yellow]Cancelled by user.[/yellow]")
            raise typer.Exit(code=1)

    try:
        exit_code = launch(config, protocol)
    except KeyboardInterrupt:  # pragma: no cover - user interrupt
        console.print("[yellow]Interrupted[/yellow]")
        raise typer.Exit(code=1) from None

    if exit_code != 0:
        console.print(f"[red]MarkItDown exited with code {exit_code}[/red]")
        raise typer.Exit(code=exit_code)

    console.print("[green]MarkItDown finished successfully.[/green]")


if __name__ == "__main__":
    app()
