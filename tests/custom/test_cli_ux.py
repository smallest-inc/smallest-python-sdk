"""CLI UX additions: version, grouped help, docs/open URL fallback."""

import re

from typer.testing import CliRunner

from smallestai import __version__
from smallestai.cli.main import app

runner = CliRunner()

_ANSI = re.compile(r"\x1b\[[0-9;]*m")
# Render help wide so Rich doesn't wrap/truncate option names at 80 cols (CI).
_WIDE = {"COLUMNS": "200", "TERM": "dumb"}


def _plain_help(args):
    res = runner.invoke(app, args, env=_WIDE)
    return res, _ANSI.sub("", res.output)


def test_version_command_and_flag():
    for args in (["version"], ["--version"]):
        res = runner.invoke(app, args)
        assert res.exit_code == 0
        assert __version__ in res.output


def test_welcome_shows_grouped_commands():
    res = runner.invoke(app, [])
    assert res.exit_code == 0
    for group in ("BUILD & DEPLOY", "VOICE AGENTS", "TELEPHONY", "SPEECH", "SETUP"):
        assert group in res.output
    for cmd in ("agent-crew", "agents", "calls", "models", "mcp", "status"):
        assert cmd in res.output


def test_docs_prints_url_when_not_a_tty():
    # CliRunner stdout is not a TTY, so docs/open print the URL instead of launching.
    res = runner.invoke(app, ["docs"])
    assert res.exit_code == 0
    assert "docs.smallest.ai" in res.output
    res = runner.invoke(app, ["open"])
    assert res.exit_code == 0
    assert "app.smallest.ai" in res.output


def test_agent_crew_commands_have_agent_id_and_json():
    for args in (
        ["agent-crew", "builds", "--help"],
        ["agent-crew", "deploy", "--help"],
        ["agent-crew", "logs", "--help"],
    ):
        res, plain = _plain_help(args)
        assert res.exit_code == 0
        assert "--agent-id" in plain
    _, plain = _plain_help(["agent-crew", "builds", "--help"])
    assert "--json" in plain


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
