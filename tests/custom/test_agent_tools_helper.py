"""Unit tests for the AgentTools helper (branch/revision versioning flow).

Exercised with a fake transport (no network):
- merge vs replace semantics keyed by tool name, over the live resolved config
- the write goes through the branch flow: PUT draft -> publish -> make-live
- the draft body carries singlePromptConfig.tools with camelCase wire fields
- add_transfer_call builds a correct transfer_call Tool (incl. on_hold_music)
- None optionals are stripped; API error bodies are surfaced
"""

import json

import pytest

from smallestai.agents.helpers import (
    AgentTools,
    AgentToolsError,
    SinglePromptConfig,
    Tool,
    ToolTransferOption,
)

BRANCH_ID = "BR1"
HEAD = "REV1"


def test_exported_tool_models_construct_and_serialize():
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
        self.content = self.text.encode()

    def json(self):
        return self._payload


class FakeBranchTransport:
    """Serves the branch endpoints and records draft/publish/live calls."""

    def __init__(self, tools):
        self.resolved_tools = list(tools)  # current live tools
        self.puts = []       # (url, body)
        self.published = 0
        self.made_live = 0

    # GET /agent/{id}/branches  and  /branches/{bid}/revisions/{head}
    def get(self, url, headers=None, timeout=None):
        if url.endswith("/branches"):
            return FakeResponse({"data": {"branches": [{
                "isLive": True,
                "branch": {"_id": BRANCH_ID, "name": "main", "isDefault": True,
                           "status": "active", "headRevisionId": HEAD},
            }]}})
        if "/revisions/" in url:
            return FakeResponse({"data": {
                "revision": {"status": "published"},
                "resolvedConfig": {"workflow_tools": {"tools": self.resolved_tools}},
            }})
        return FakeResponse({"data": {}})

    def put(self, url, headers=None, json=None, timeout=None):
        self.puts.append((url, json))
        # reflect the draft tools into the "live" config so publish->live is visible
        self.resolved_tools = json["singlePromptConfig"]["tools"]
        return FakeResponse({"data": {"draftId": "D1"}})

    def post(self, url, headers=None, json=None, timeout=None):
        if url.endswith("/draft/publish"):
            self.published += 1
            return FakeResponse({"data": {"state": "committed"}})  # sync commit, no poll
        if url.endswith("/live"):
            self.made_live += 1
            return FakeResponse({"data": {"branch": {"_id": BRANCH_ID}}})
        return FakeResponse({"data": {}})


@pytest.fixture
def wired(monkeypatch):
    def _make(tools):
        t = FakeBranchTransport(tools)
        monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.get", t.get)
        monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.put", t.put)
        monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.post", t.post)
        return AgentTools(api_key="sk_test", base_url="https://api.example/atoms/v1"), t

    return _make


def test_add_transfer_call_runs_full_branch_flow(wired):
    helper, t = wired([])
    tool = helper.add_transfer_call(
        "AG1", number="+15551234567", transfer_type="cold_transfer", on_hold_music="relaxing_sound"
    )
    assert isinstance(tool, Tool)
    # draft -> publish -> make-live all happened, once
    assert len(t.puts) == 1
    assert t.published == 1
    assert t.made_live == 1
    url, body = t.puts[0]
    assert url.endswith(f"/branches/{BRANCH_ID}/draft")
    wire = body["singlePromptConfig"]["tools"][0]
    assert wire["type"] == "transfer_call"
    assert wire["transferNumber"] == "+15551234567"
    assert wire["transferOption"] == {"type": "cold_transfer"}
    assert wire["onHoldMusic"] == "relaxing_sound"


def test_merge_preserves_existing_live_tools(wired):
    helper, t = wired([{"type": "end_call", "name": "end_call", "description": "bye"}])
    helper.add_transfer_call("AG1", number="+1")
    _, body = t.puts[0]
    names = [x["name"] for x in body["singlePromptConfig"]["tools"]]
    assert names == ["end_call", "transfer_call"]


def test_same_name_overwrites(wired):
    helper, t = wired([{"type": "transfer_call", "name": "transfer_call", "transferNumber": "+1old"}])
    helper.add_transfer_call("AG1", number="+1new")
    _, body = t.puts[0]
    tools = body["singlePromptConfig"]["tools"]
    assert len(tools) == 1 and tools[0]["transferNumber"] == "+1new"


def test_replace_overwrites_all(wired):
    helper, t = wired([{"type": "end_call", "name": "end_call"}])
    helper.set_tools("AG1", [Tool(type="transfer_call", name="x", description="d", transfer_number="+1")], replace=True)
    _, body = t.puts[0]
    assert [x["name"] for x in body["singlePromptConfig"]["tools"]] == ["x"]


def test_remove_tool(wired):
    helper, t = wired([
        {"type": "transfer_call", "name": "transfer_call"},
        {"type": "end_call", "name": "end_call"},
    ])
    helper.remove_tool("AG1", "transfer_call")
    _, body = t.puts[0]
    assert [x["name"] for x in body["singlePromptConfig"]["tools"]] == ["end_call"]


def test_make_live_false_publishes_but_does_not_activate(wired):
    helper, t = wired([])
    helper.add_transfer_call("AG1", number="+1", make_live=False)
    assert t.published == 1
    assert t.made_live == 0


def test_get_tools_reads_live_resolved_config(wired):
    helper, _ = wired([{"type": "transfer_call", "name": "transfer_call", "description": "d", "transferNumber": "+1"}])
    got = helper.get_tools("AG1")
    assert len(got) == 1 and isinstance(got[0], Tool)
    assert got[0].transfer_number == "+1"


def test_none_optionals_stripped_from_wire(wired):
    helper, t = wired([])
    helper.add_transfer_call("AG1", number="+15551234567")
    wire = t.puts[0][1]["singlePromptConfig"]["tools"][0]
    assert "transferOnlyIfHuman" not in wire
    assert "onHoldMusic" not in wire
    assert "+" not in wire["description"]


def test_no_branches_raises(monkeypatch):
    def empty_get(url, headers=None, timeout=None):
        return FakeResponse({"data": {"branches": []}})

    monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.get", empty_get)
    helper = AgentTools(api_key="sk_test", base_url="https://api.example/atoms/v1")
    with pytest.raises(AgentToolsError, match="no branches"):
        helper.add_transfer_call("AG1", number="+1")


def test_api_error_body_is_surfaced(monkeypatch):
    def get(url, headers=None, timeout=None):
        return FakeResponse({"data": {"branches": [{"isLive": True, "branch": {"_id": BRANCH_ID, "headRevisionId": HEAD, "isDefault": True}}]}})

    def bad_put(url, headers=None, json=None, timeout=None):
        return FakeResponse({"status": False, "errors": ["invalid tool"]}, status_code=400)

    monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.get", get)
    monkeypatch.setattr("smallestai.agents.helpers.agent_tools.requests.put", bad_put)
    helper = AgentTools(api_key="sk_test", base_url="https://api.example/atoms/v1")
    with pytest.raises(AgentToolsError, match="HTTP 400.*invalid tool"):
        helper.add_transfer_call("AG1", number="+1")
