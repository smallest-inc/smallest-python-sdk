"""Bare `smallestai` shows a banner (not an error), and `mcp` prints setup config."""
from typer.testing import CliRunner

from smallestai.cli.main import app

runner = CliRunner()


def test_bare_cli_shows_banner_and_commands_not_error():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Missing command" not in result.output
    # command list is present
    for name in ("agent-crew", "agents", "calls", "waves", "mcp"):
        assert name in result.output


def test_mcp_prints_setup_config():
    result = runner.invoke(app, ["mcp"])
    assert result.exit_code == 0
    assert "@smallest-ai/mcp-server" in result.output


def test_mcp_config_subcommand_emits_json():
    result = runner.invoke(app, ["mcp", "config"])
    assert result.exit_code == 0
    assert "mcpServers" in result.output


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
