"""Unit tests for the MultiAgent (Playbooks) config writer — no network.

These mock the generated client and assert:
  - the correct workflowType + playbooks body is written through the draft pipeline
    for a representative router + 2-specialist definition,
  - client-side validation mirrors the platform publish refines (error paths),
  - round-trip serialization (to_api -> config_from_api) is lossless,
  - the 403 allowlist denial maps to MultiAgentNotEntitledError.

Live coverage (real create -> write -> read-back -> archive) is in the same file
behind the `integration` marker, gated on SMALLEST_API_KEY.
"""

from __future__ import annotations

import os
from types import SimpleNamespace as NS

import pytest

from smallestai.atoms.errors.forbidden_error import ForbiddenError
from smallestai.atoms.helpers import (
    IntentRouter,
    MultiAgent,
    MultiAgentError,
    MultiAgentNotEntitledError,
    Playbook,
    PlaybookAuth,
    PlaybooksConfig,
    Verification,
    config_from_api,
)
from smallestai.atoms.helpers.multi_agent import WORKFLOW_TYPE_MULTI_AGENTS

# ── fixtures ──────────────────────────────────────────────────────────────────────


def _representative_config() -> PlaybooksConfig:
    return PlaybooksConfig(
        router=IntentRouter(
            fallback_playbook_id="general",
            classifier_model="gpt-4o-mini",
            allow_mid_call_reroute=True,
        ),
        conversation_guide="You are Aria, a warm, concise support agent.",
        global_tool_refs=["tool_lookup_account"],
        verifications=[
            Verification(id="v_identity", name="Identity check", tool_refs=["tool_verify_dob"], max_retries=2),
        ],
        playbooks=[
            Playbook(
                id="card_fraud",
                name="Card fraud",
                intent_name="card_fraud",
                intent_description="Caller reports a lost/stolen card or fraud.",
                prompt="You handle card-fraud reports.",
                tool_refs=["tool_freeze_card"],
                verification_ids=["v_identity"],
            ),
            Playbook(
                id="general",
                name="General",
                intent_name="general",
                intent_description="Anything else.",
                prompt="General support.",
            ),
        ],
    )


class _RecordingClient:
    """A minimal stand-in for SmallestAI that records the calls the writer makes."""

    def __init__(self, *, default_branch_id: str = "branch_main", publish_fails: bool = False, create_raises=None):
        self.created_kwargs = None
        self.update_draft_calls = []
        self.publish_calls = []
        self._create_raises = create_raises

        parent = self

        class _Agents:
            def create_agent(self, **kwargs):
                parent.created_kwargs = kwargs
                if parent._create_raises is not None:
                    raise parent._create_raises
                return NS(status=True, data="agent_new")

        class _Branches:
            def list(self, *, id):
                inner = NS(id=default_branch_id, is_default=True)
                other = NS(id="branch_fork", is_default=False)
                return NS(data=NS(branches=[NS(branch=other), NS(branch=inner)]))

            def update_draft(self, *, id, branch_id, **fields):
                parent.update_draft_calls.append({"id": id, "branch_id": branch_id, **fields})
                return NS(data=NS(id="rev_draft", draft_revision=2, workflow_type=WORKFLOW_TYPE_MULTI_AGENTS))

            def publish_draft(self, *, id, branch_id, label=None):
                parent.publish_calls.append({"id": id, "branch_id": branch_id, "label": label})
                return NS(data=NS(state="committed", revision=NS(id="rev_pub", status="published")))

        class _Revisions:
            def list(self, *, id, branch_id, limit):
                return NS(data=NS(revisions=[NS(id="rev_pub")]))

            def get(self, *, id, branch_id, revision_id):
                cfg = _representative_config().to_api()
                return NS(data=NS(resolved_config={"playbooks": {"playbooks": cfg}}))

        class _Atoms:
            agents = _Agents()
            agent_versioning_branches = _Branches()
            agent_versioning_revisions = _Revisions()

        self.atoms = _Atoms()


# ── write-path body shape ───────────────────────────────────────────────────────


def test_create_agent_sets_multi_agents_workflow_type_and_writes_playbooks():
    client = _RecordingClient()
    ma = MultiAgent(client)
    cfg = _representative_config()

    agent_id = ma.create_agent(name="Support bot", config=cfg)

    assert agent_id == "agent_new"
    # workflowType must be flipped at create (it cannot be set on the draft body).
    assert client.created_kwargs["workflow_type"] == "multi_agents"
    assert client.created_kwargs["name"] == "Support bot"

    # The playbooks config goes through the draft body via additional_body_parameters.
    assert len(client.update_draft_calls) == 1
    call = client.update_draft_calls[0]
    assert call["branch_id"] == "branch_main"  # resolved to the default branch
    body = call["request_options"]["additional_body_parameters"]["playbooks"]

    assert body["router"] == {
        "fallbackPlaybookId": "general",
        "allowMidCallReroute": True,
        "classifierModel": "gpt-4o-mini",
    }
    assert body["conversationGuide"] == "You are Aria, a warm, concise support agent."
    assert body["globalToolRefs"] == ["tool_lookup_account"]
    assert [p["id"] for p in body["playbooks"]] == ["card_fraud", "general"]
    assert body["playbooks"][0]["intentName"] == "card_fraud"
    assert body["playbooks"][0]["toolRefs"] == ["tool_freeze_card"]
    assert body["playbooks"][0]["verificationIds"] == ["v_identity"]
    assert body["verifications"][0]["id"] == "v_identity"

    # And it publishes (via edit_and_publish -> publish_draft).
    assert client.publish_calls and client.publish_calls[0]["id"] == "agent_new"


def test_publish_config_resolves_default_branch_and_publishes():
    client = _RecordingClient(default_branch_id="branch_live")
    ma = MultiAgent(client)

    rev = ma.publish_config("agent_x", _representative_config(), label="v1")

    assert rev.id == "rev_pub"
    assert client.update_draft_calls[0]["branch_id"] == "branch_live"
    assert client.publish_calls[0]["label"] == "v1"


def test_write_draft_does_not_publish():
    client = _RecordingClient()
    ma = MultiAgent(client)

    ma.write_draft("agent_x", _representative_config(), branch_id="branch_explicit")

    assert client.update_draft_calls[0]["branch_id"] == "branch_explicit"
    assert client.publish_calls == []  # write_draft must not publish


def test_expected_revision_is_forwarded_for_optimistic_concurrency():
    client = _RecordingClient()
    ma = MultiAgent(client)

    ma.write_draft("agent_x", _representative_config(), expected_revision=7)

    assert client.update_draft_calls[0]["expected_revision"] == 7


# ── read-back ──────────────────────────────────────────────────────────────────


def test_read_config_unwraps_double_wrapped_section():
    client = _RecordingClient()
    ma = MultiAgent(client)

    cfg = ma.read_config("agent_x")

    assert cfg is not None
    assert cfg.router.fallback_playbook_id == "general"
    assert [p.id for p in cfg.playbooks] == ["card_fraud", "general"]
    assert cfg.verifications[0].id == "v_identity"


def test_read_config_returns_none_on_empty_section():
    client = _RecordingClient()

    # Override revisions.get to return an empty playbooks section (non-multi-agent / draft).
    def _empty_get(*, id, branch_id, revision_id):
        return NS(data=NS(resolved_config={"playbooks": {}}))

    client.atoms.agent_versioning_revisions.get = _empty_get
    ma = MultiAgent(client)

    assert ma.read_config("agent_x") is None


# ── validation / error paths (mirror platform refines) ─────────────────────────


def test_validate_requires_at_least_one_playbook():
    cfg = PlaybooksConfig(router=IntentRouter(fallback_playbook_id="x"), playbooks=[])
    with pytest.raises(MultiAgentError, match="At least one playbook"):
        cfg.validate()


def test_validate_fallback_must_reference_existing_playbook():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="missing"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p"),
        ],
    )
    with pytest.raises(MultiAgentError, match="must reference an existing playbook"):
        cfg.validate()


def test_validate_fallback_must_be_enabled():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p", enabled=False),
            Playbook(id="b", name="B", intent_name="b", intent_description="d", prompt="p"),
        ],
    )
    with pytest.raises(MultiAgentError, match="must reference an enabled playbook"):
        cfg.validate()


def test_validate_rejects_duplicate_ids():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p"),
            Playbook(id="a", name="B", intent_name="b", intent_description="d", prompt="p"),
        ],
    )
    with pytest.raises(MultiAgentError, match="ids must be unique"):
        cfg.validate()


def test_validate_rejects_duplicate_intent_names_case_insensitive():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="Billing", intent_description="d", prompt="p"),
            Playbook(id="b", name="B", intent_name="billing", intent_description="d", prompt="p"),
        ],
    )
    with pytest.raises(MultiAgentError, match="intent names must be unique"):
        cfg.validate()


def test_validate_rejects_structured_type():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p", type="structured"),
        ],
    )
    with pytest.raises(MultiAgentError, match="structured.*reserved"):
        cfg.validate()


def test_validate_requires_weak_tools_when_auth_level_set():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p", auth_level="weak"),
        ],
    )
    with pytest.raises(MultiAgentError, match="weak_tools is empty"):
        cfg.validate()


def test_validate_strong_auth_satisfied_with_tools():
    cfg = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="a"),
        auth=PlaybookAuth(weak_tools=[{"name": "id_phone"}], strong_tools=[{"name": "verify_dob"}]),
        playbooks=[
            Playbook(id="a", name="A", intent_name="a", intent_description="d", prompt="p", auth_level="strong"),
        ],
    )
    cfg.validate()  # should not raise


def test_write_draft_validates_before_network():
    client = _RecordingClient()
    ma = MultiAgent(client)
    bad = PlaybooksConfig(router=IntentRouter(fallback_playbook_id="x"), playbooks=[])

    with pytest.raises(MultiAgentError):
        ma.write_draft("agent_x", bad)

    assert client.update_draft_calls == []  # no network on invalid config


# ── entitlement mapping ─────────────────────────────────────────────────────────


def test_create_maps_403_allowlist_denial_to_not_entitled():
    denial = ForbiddenError(
        body={"status": False, "errors": ["Multi-Agent agents are not available for your account."]}
    )
    client = _RecordingClient(create_raises=denial)
    ma = MultiAgent(client)

    with pytest.raises(MultiAgentNotEntitledError):
        ma.create_agent(name="x", config=_representative_config())


def test_create_reraises_unrelated_403():
    other = ForbiddenError(body={"status": False, "errors": ["Some other forbidden reason"]})
    client = _RecordingClient(create_raises=other)
    ma = MultiAgent(client)

    with pytest.raises(ForbiddenError):
        ma.create_agent(name="x", config=_representative_config())


# ── round-trip serialization ────────────────────────────────────────────────────


def test_to_api_then_config_from_api_is_lossless():
    cfg = _representative_config()
    back = config_from_api(cfg.to_api())

    assert back.router.fallback_playbook_id == cfg.router.fallback_playbook_id
    assert back.router.classifier_model == cfg.router.classifier_model
    assert back.conversation_guide == cfg.conversation_guide
    assert back.global_tool_refs == cfg.global_tool_refs
    assert [p.id for p in back.playbooks] == [p.id for p in cfg.playbooks]
    assert back.playbooks[0].tool_refs == cfg.playbooks[0].tool_refs
    assert back.playbooks[0].verification_ids == cfg.playbooks[0].verification_ids
    assert back.verifications[0].id == cfg.verifications[0].id
    back.validate()  # the parsed config is itself valid


# ── live round-trip (gated) ──────────────────────────────────────────────────────


@pytest.mark.integration
def test_live_round_trip_create_write_read_archive():
    """Real create -> write playbooks -> publish -> read-back -> archive.

    Uses a THROWAWAY agent and archives it in a finally. Requires SMALLEST_API_KEY on
    an account on the multi-agent allowlist (e.g. an @smallest.ai account).
    """
    api_key = os.environ.get("SMALLEST_API_KEY")
    if not api_key:
        pytest.skip("SMALLEST_API_KEY not set")

    from smallestai import SmallestAI

    client = SmallestAI(api_key=api_key)
    ma = MultiAgent(client)
    cfg = _representative_config()

    agent_id = None
    try:
        try:
            agent_id = ma.create_agent(name="zzz-sdk-ma-test-DELETE", config=cfg)
        except MultiAgentNotEntitledError:
            pytest.skip("account is not on the multi-agent allowlist")

        back = ma.read_config(agent_id)
        assert back is not None
        assert back.router.fallback_playbook_id == "general"
        assert [p.id for p in back.playbooks] == ["card_fraud", "general"]
        assert back.playbooks[0].prompt == "You handle card-fraud reports."
        assert back.verifications[0].id == "v_identity"
    finally:
        if agent_id:
            client.atoms.agents.archive_agent(id=agent_id)
