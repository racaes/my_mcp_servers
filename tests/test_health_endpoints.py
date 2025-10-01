from __future__ import annotations

from pathlib import Path

import pytest  # type: ignore[import]

from servers.markitdown import load_config


def test_load_config_defaults(tmp_path: Path) -> None:
    config = load_config(tmp_path / "missing.toml")
    assert config.server.name == "markitdown"
    assert config.server.protocol == "stdio"


def test_build_launch_command_http() -> None:
    from servers.markitdown.app import ConfigBundle

    bundle = ConfigBundle()
    cmd = bundle.server.command + ["--http", "--host", bundle.http.host, "--port", str(bundle.http.port)]

    from servers.markitdown.app import build_launch_command

    assert build_launch_command(bundle, "http") == cmd


def test_launch_handles_missing_binary() -> None:
    from servers.markitdown.app import ConfigBundle, MarkItDownServerConfig, launch

    bundle = ConfigBundle(server=MarkItDownServerConfig(command=["nonexistent-binary"]))

    with pytest.raises(FileNotFoundError):
        launch(bundle, "stdio")
