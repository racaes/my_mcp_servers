from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:  # Python 3.11+
    import tomllib  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for <3.11
    import tomli as tomllib  # type: ignore

from pydantic import BaseModel, Field


class MarkItDownServerConfig(BaseModel):
    """Configuration describing how to invoke the upstream markitdown-mcp package."""

    name: str = Field(default="markitdown", description="Logical server identifier")
    protocol: str = Field(default="stdio", description="Transport protocol: stdio or http")
    command: List[str] = Field(
        default_factory=lambda: [sys.executable, "-m", "markitdown_mcp"],
        description="Base command used to launch markitdown-mcp",
    )
    working_directory: Path = Field(
        default=Path.cwd(), description="Directory passed as cwd when spawning the server"
    )
    env: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment variables merged into the subprocess when launching",
    )


class HTTPConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 3001


class ConfigBundle(BaseModel):
    server: MarkItDownServerConfig = MarkItDownServerConfig()
    http: HTTPConfig = HTTPConfig()


def load_config(config_path: Path | None) -> ConfigBundle:
    """Load TOML configuration for markitdown-mcp launch options."""

    resolved = config_path or Path(__file__).with_name("config.toml")
    if not resolved.exists():
        logging.getLogger(__name__).debug("Config %s missing; using defaults", resolved)
        return ConfigBundle()

    with resolved.open("rb") as stream:
        data = tomllib.load(stream)

    return ConfigBundle.model_validate(data)


def build_launch_command(bundle: ConfigBundle, protocol: str) -> List[str]:
    """Return the command line for invoking markitdown-mcp with the desired protocol."""

    cmd = list(bundle.server.command)

    if protocol == "stdio":
        return cmd

    if protocol == "http":
        return cmd + ["--http", "--host", bundle.http.host, "--port", str(bundle.http.port)]

    raise ValueError(f"Unsupported protocol: {protocol}")


def launch(bundle: ConfigBundle, protocol: str) -> int:
    """Run markitdown-mcp with the requested transport and return the exit code."""

    cmd = build_launch_command(bundle, protocol)
    env = os.environ.copy()
    env.update(bundle.server.env)

    process = subprocess.run(cmd, cwd=bundle.server.working_directory, env=env, check=False)
    return process.returncode
