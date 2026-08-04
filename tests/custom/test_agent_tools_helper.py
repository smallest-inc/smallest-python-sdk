"""Unit tests for the AgentTools helper.

These exercise the read-modify-write logic with a fake transport (no network):
- merge vs replace semantics keyed by tool name
- prompt + other tools are preserved (never wiped)
- the write targets PATCH /workflow/{workflowId} with camelCase wire fields
- add_transfer_call builds a correct transfer_call Tool (incl. on_hold_music)
- guardrails: missing workflowId and non-single_prompt agents raise
"""

import json

import pytest

from smallestai.atoms.helpers import (
    AgentTools,
    AgentToolsError,
    SinglePromptConfig,
    Tool,
    ToolTransferOption,
)


def test_exported_tool_models_construct_and_serialize():
    """The models re-exported from atoms.helpers build and serialize by alias."""
    option = ToolTransferOption(type="warm_transfer")
    tool = Tool(
        type="transfer_call",
        name="transfer_call",
        description="Transfer to a specialist.",
        transfer_number="+15551234567",
        transfer_option=option,
    )
    config = SinglePromptConfig(prompt="You are helpful.", tools=[tool])
    wire = config.dict(by_alias=True, exclude_none=True)
    assert wire["prompt"] == "You are helpful."
    assert wire["tools"][0]["transferNumber"] == "+15551234567"
    assert wire["tools"][0]["transferOption"]["type"] == "warm_transfer"


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


class FakeTransport:
    """Records GET/PATCH calls and serves canned agent + workflow docs."""

    def __init__(self, agent_doc, workflow_cfg):
        self.agent_doc = agent_doc
        self.workflow_cfg = workflow_cfg
        self.patches = []  # (path, body)
        self.gets = []

    def get(self, url, headers=None, timeout=None):
        self.gets.append(url)
        if url.endswith("/workflow"):
            return FakeResponse({"status": True, "data": self.workflow_cfg})
        return FakeResponse({"status": True, "data": self.agent_doc})

    def patch(self, url, headers=None, json=None, timeout=None):
        self.patches.append((url, json))
        # reflect the write into the stored config so a subsequent read sees it
        self.workflow_cfg = dict(self.workflow_cfg)
        self.workflow_cfg["tools"] = json["singlePromptConfig"]["tools"]
        return FakeResponse({"status": True, "data": self.workflow_cfg})


@pytest.fixture
def wired(monkeypatch):
    def _make(agent_doc, workflow_cfg):
        transport = FakeTransport(agent_doc, workflow_cfg)
        monkeypatch.setattr("smallestai.atoms.helpers.agent_tools.requests.get", transport.get)
        monkeypatch.setattr("smallestai.atoms.helpers.agent_tools.requests.patch", transport.patch)
        helper = AgentTools(api_key="sk_test", base_url="https://api.example/atoms/v1")
        return helper, transport

    return _make


AGENT_DOC = {"_id": "AG1", "workflowId": "WF1", "workflowType": "single_prompt"}


def test_add_transfer_call_builds_correct_tool_and_targets_workflow(wired):
    helper, t = wired(AGENT_DOC, {"prompt": "You are helpful.", "tools": []})
    tool = helper.add_transfer_call(
        "AG1", number="+15551234567", transfer_type="cold_transfer", on_hold_music="relaxing_sound"
    )
    assert isinstance(tool, Tool)
    assert tool.transfer_number == "+15551234567"

    # one PATCH, to the workflowId (not the agentId), single_prompt shape
    assert len(t.patches) == 1
    url, body = t.patches[0]
    assert url.endswith("/workflow/WF1")
    assert body["type"] == "single_prompt"
    written = body["singlePromptConfig"]["tools"]
    assert len(written) == 1
    wire = written[0]
    # camelCase aliases on the wire
    assert wire["type"] == "transfer_call"
    assert wire["transferNumber"] == "+15551234567"
    assert wire["transferOption"] == {"type": "cold_transfer"}
    assert wire["onHoldMusic"] == "relaxing_sound"
    # prompt preserved
    assert body["singlePromptConfig"]["prompt"] == "You are helpful."


def test_none_optionals_are_stripped_from_wire(wired):
    """Explicit-None optionals must not reach the API (it rejects nulls)."""
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": []})
    # transfer_only_if_human omitted -> must be absent, not null
    helper.add_transfer_call("AG1", number="+15551234567")
    _, body = t.patches[0]
    wire = body["singlePromptConfig"]["tools"][0]
    assert "transferOnlyIfHuman" not in wire
    assert "onHoldMusic" not in wire
    # default description must be within the allowed charset (no '+')
    assert "+" not in wire["description"]


def test_user_tool_with_explicit_none_is_stripped(wired):
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": []})
    tool = Tool(type="transfer_call", name="x", description="d", transfer_number="+1", transfer_only_if_human=None)
    helper.set_tools("AG1", [tool])
    _, body = t.patches[0]
    assert "transferOnlyIfHuman" not in body["singlePromptConfig"]["tools"][0]


def test_set_tools_merges_by_name_and_preserves_existing(wired):
    existing = {"type": "end_call", "name": "end_call", "description": "bye", "enabled": True}
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": [existing]})
    new_tool = Tool(type="transfer_call", name="transfer_call", description="d", transfer_number="+1")
    helper.set_tools("AG1", [new_tool])

    _, body = t.patches[0]
    names = [tool["name"] for tool in body["singlePromptConfig"]["tools"]]
    assert names == ["end_call", "transfer_call"]  # existing kept, new appended


def test_set_tools_same_name_overwrites_not_duplicates(wired):
    existing = {"type": "transfer_call", "name": "transfer_call", "transferNumber": "+1old"}
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": [existing]})
    helper.add_transfer_call("AG1", number="+1new")

    _, body = t.patches[0]
    tools = body["singlePromptConfig"]["tools"]
    assert len(tools) == 1
    assert tools[0]["transferNumber"] == "+1new"


def test_set_tools_replace_overwrites_all(wired):
    existing = {"type": "end_call", "name": "end_call"}
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": [existing]})
    helper.set_tools("AG1", [Tool(type="transfer_call", name="x", description="d", transfer_number="+1")], replace=True)

    _, body = t.patches[0]
    names = [tool["name"] for tool in body["singlePromptConfig"]["tools"]]
    assert names == ["x"]  # end_call dropped


def test_remove_tool(wired):
    tools = [
        {"type": "transfer_call", "name": "transfer_call"},
        {"type": "end_call", "name": "end_call"},
    ]
    helper, t = wired(AGENT_DOC, {"prompt": "P", "tools": tools})
    helper.remove_tool("AG1", "transfer_call")

    _, body = t.patches[0]
    names = [tool["name"] for tool in body["singlePromptConfig"]["tools"]]
    assert names == ["end_call"]


def test_get_tools_returns_typed(wired):
    tools = [{"type": "transfer_call", "name": "transfer_call", "description": "d", "transferNumber": "+1"}]
    helper, _ = wired(AGENT_DOC, {"prompt": "P", "tools": tools})
    got = helper.get_tools("AG1")
    assert len(got) == 1
    assert isinstance(got[0], Tool)
    assert got[0].transfer_number == "+1"


def test_missing_workflow_id_raises(wired):
    helper, _ = wired({"_id": "AG1", "workflowType": "single_prompt"}, {"prompt": "P", "tools": []})
    with pytest.raises(AgentToolsError, match="no workflowId"):
        helper.set_tools("AG1", [Tool(type="end_call", name="end_call", description="d")])


def test_non_single_prompt_agent_raises(wired):
    helper, _ = wired(
        {"_id": "AG1", "workflowId": "WF1", "workflowType": "workflow_graph"}, {"prompt": "P", "tools": []}
    )
    with pytest.raises(AgentToolsError, match="workflow_graph"):
        helper.add_transfer_call("AG1", number="+1")


def test_api_error_body_is_surfaced(monkeypatch):
    """A non-2xx write raises AgentToolsError carrying the API's error body."""

    def bad_patch(url, headers=None, json=None, timeout=None):
        return FakeResponse({"status": False, "error": "prompt is required"}, status_code=400)

    def ok_get(url, headers=None, timeout=None):
        if url.endswith("/workflow"):
            return FakeResponse({"data": {"prompt": "P", "tools": []}})
        return FakeResponse({"data": AGENT_DOC})

    monkeypatch.setattr("smallestai.atoms.helpers.agent_tools.requests.get", ok_get)
    monkeypatch.setattr("smallestai.atoms.helpers.agent_tools.requests.patch", bad_patch)
    helper = AgentTools(api_key="sk_test", base_url="https://api.example/atoms/v1")
    with pytest.raises(AgentToolsError, match="HTTP 400.*prompt is required"):
        helper.add_transfer_call("AG1", number="+1")
