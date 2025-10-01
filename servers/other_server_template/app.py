"""Template module for building additional MCP servers.

Duplicate this directory, rename it, and implement your server-specific
logic inside the `bootstrap` and configuration helpers below.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

try:  # Optional import – only required if you expose HTTP endpoints
    from fastapi import FastAPI  # type: ignore
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore


class TemplateServerConfig(BaseModel):
    name: str = "other-server"
    entrypoint: str = "python -m your_package.server"
    working_directory: Path = Field(default=Path.cwd())


def load_config(_: Optional[Path] = None) -> TemplateServerConfig:
    """Return default configuration for the template server."""

    # Replace this with TOML loading logic mirroring markitdown/app.py when ready.
    return TemplateServerConfig()


async def run_stdio(config: TemplateServerConfig) -> int:
    """Example coroutine that would spawn the upstream MCP server via stdio."""

    logging.info("Pretending to launch %s via stdio", config.name)
    await asyncio.sleep(0.1)
    return 0


def create_http_app(_: TemplateServerConfig):  # pragma: no cover - placeholder
    """Return a FastAPI app for new MCP servers.

    Replace the body of this function with HTTP endpoints to surface your
    server capabilities. You can follow the MarkItDown implementation for
    reference.
    """

    if FastAPI is None:
        raise RuntimeError("FastAPI is required to expose HTTP endpoints.")

    app = FastAPI(title="Other MCP Server")

    @app.get("/status")
    async def status():  # noqa: WPS430 - FastAPI signature requirement
        return {"status": "ok", "server": "other-server"}

    return app
