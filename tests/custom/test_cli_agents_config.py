"""Unit tests for `smallestai agents create`/`update` config flags: SDK wiring
with a fake client. No network.

Asserts the field-to-call split from PRO-3554:
  - metadata (name, description, allow_inbound) -> agents.update_agent / create_agent
  - versioned config (prompt, first message, language, voice, model, redaction,
    interruptions, background sound) -> the branch draft (update_draft + publish)
"""

import types

import pytest
from typer.testing import CliRunner

from smallestai.cli.agents import initialise_agents_app

runner = CliRunner()


class _Resp:
    def __init__(self, data):
        self.data = data


def _obj(**kw):
    return types.SimpleNamespace(**kw)


class FakeAgents:
    def __init__(self):
        self.create_kwargs = None
        self.update_args = None
        self.update_kwargs = None

    def create_agent(self, **kw):
        self.create_kwargs = kw
        return _Resp("AGENT-NEW")

    def update_agent(self, agent_id, **kw):
        self.update_args = agent_id
        self.update_kwargs = kw
        return _Resp(_obj(id=agent_id))


class FakeBranches:
    """Returns one live branch so _resolve_write_branch_id picks it."""

    def list(self, id):
        branch = _obj(id="BRANCH-LIVE", is_default=True)
        summary = _obj(is_live=True, branch=branch)
        return _Resp(_obj(branches=[summary]))


class FakeClient:
    def __init__(self):
        self.agents = FakeAgents()
        self.agent_versioning_branches = FakeBranches()
        self.atoms = _obj(agents=self.agents, agent_versioning_branches=self.agent_versioning_branches)


class FakeVersioning:
    """Captures edit_and_publish calls instead of hitting draft/publish endpoints."""

    calls = []

    def __init__(self, client):
        self.client = client

    def edit_and_publish(self, agent_id, branch_id, **fields):
        FakeVersioning.calls.append((agent_id, branch_id, fields))
        return _obj(id="REV-1")


@pytest.fixture
def app(monkeypatch):
    client = FakeClient()
    FakeVersioning.calls = []
    monkeypatch.setattr("smallestai.cli.agents._client", lambda auth: client)
    monkeypatch.setattr("smallestai.atoms.helpers.Versioning", FakeVersioning)
    app = initialise_agents_app(auth_client=None)
    app._fake_client = client  # expose for assertions
    return app


def test_create_passes_config_fields(app):
    res = runner.invoke(
        app,
        [
            "create",
            "My Agent",
            "--description",
            "desc",
            "--allow-inbound",
            "--first-message",
            "Hi!",
            "--prompt",
            "You are helpful",
            "--language",
            "en",
            "--voice-id",
            "V123",
            "--model",
            "gpt-4o",
            "--redaction",
            "--allow-interruptions",
            "--background-sound",
            "office",
        ],
    )
    assert res.exit_code == 0, res.output
    assert "AGENT-NEW" in res.output
    kw = app._fake_client.agents.create_kwargs
    assert kw["name"] == "My Agent"
    assert kw["description"] == "desc"
    assert kw["allow_inbound_call"] is True
    assert kw["first_message"] == "Hi!"
    assert kw["global_prompt"] == "You are helpful"
    assert kw["language"] == {"default": "en", "supported": ["en"]}
    assert kw["synthesizer"] == {"voiceConfig": {"voiceId": "V123"}}
    assert kw["slm_model"] == "gpt-4o"
    assert kw["redaction_config"] == {"isEnabled": True}
    assert kw["allow_interruptions"] is True
    assert kw["background_sound"] == "office"


def test_create_minimal_only_name(app):
    res = runner.invoke(app, ["create", "Bare"])
    assert res.exit_code == 0, res.output
    assert app._fake_client.agents.create_kwargs == {"name": "Bare"}


def test_update_metadata_goes_through_update_agent(app):
    res = runner.invoke(app, ["update", "AG1", "--name", "Renamed", "--description", "new"])
    assert res.exit_code == 0, res.output
    assert app._fake_client.agents.update_args == "AG1"
    assert app._fake_client.agents.update_kwargs == {"name": "Renamed", "description": "new"}
    assert FakeVersioning.calls == []  # no config -> no draft write
    assert "name" in res.output and "description" in res.output


def test_update_config_goes_through_draft(app):
    res = runner.invoke(
        app,
        [
            "update",
            "AG1",
            "--prompt",
            "New prompt",
            "--voice-id",
            "V9",
            "--model",
            "gpt-4.1",
            "--no-redaction",
            "--no-allow-interruptions",
            "--background-sound",
            "cafe",
            "--language",
            "hi",
        ],
    )
    assert res.exit_code == 0, res.output
    # metadata call not made
    assert app._fake_client.agents.update_kwargs is None
    assert len(FakeVersioning.calls) == 1
    agent_id, branch_id, fields = FakeVersioning.calls[0]
    assert agent_id == "AG1"
    assert branch_id == "BRANCH-LIVE"
    assert fields["global_prompt"] == "New prompt"
    assert fields["synthesizer"] == {"voiceConfig": {"voiceId": "V9"}}
    assert fields["slm_model"] == "gpt-4.1"
    assert fields["redaction_config"] == {"isEnabled": False}
    assert fields["allow_interruptions"] is False
    assert fields["background_sound"] == "cafe"
    assert fields["language"] == {"default": "hi", "supported": ["hi"]}


def test_update_mixed_hits_both_paths(app):
    res = runner.invoke(app, ["update", "AG1", "--name", "N", "--prompt", "P"])
    assert res.exit_code == 0, res.output
    assert app._fake_client.agents.update_kwargs == {"name": "N"}
    assert len(FakeVersioning.calls) == 1
    assert FakeVersioning.calls[0][2] == {"global_prompt": "P"}


def test_update_no_flags_errors(app):
    res = runner.invoke(app, ["update", "AG1"])
    assert res.exit_code == 1
    assert "Nothing to update" in res.output
    assert FakeVersioning.calls == []
