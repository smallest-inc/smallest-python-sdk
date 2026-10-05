"""Typed writer for the platform multi-agent **Playbooks** config (PRO-3272).

A multi-agent agent (``workflowType = multi_agents``) is an **intent router + a set
of specialist playbooks**. The router classifies each user turn and routes to the
matching playbook (falling back to ``router.fallback_playbook_id``), and may re-route
mid-call. The platform runs the LLM turn; the customer authors the prompts + tool
references. See ``atoms-platform`` ``packages/atoms-types/src/workflow/playbooks.ts``.

This helper is the SDK-side *source of truth* writer: you define the config in Python,
it writes the versioned ``playbooks`` config section onto an agent's branch through the
same draft -> publish pipeline the dashboard uses, so the dashboard renders it (the
model is one-directional: the SDK writes, the UI reflects).

Why this is built on top of the generated client rather than regenerated into it:
the generated ``update_draft`` does not model a ``playbooks`` body field and the
generated ``WorkflowType`` does not list ``multi_agents`` yet. Rather than hand-edit
generated files (which a regen would clobber), this sends ``playbooks`` through Fern's
``RequestOptions.additional_body_parameters`` escape hatch and reuses
``Versioning.edit_and_publish``. The typed models below are hand-maintained to mirror
the platform zod schema; this module lives under ``helpers/`` which ``.fernignore``
protects from regeneration. If/when the API spec grows a typed ``playbooks`` draft
body, this writer can switch to the generated field without changing its public API.

Usage::

    from smallestai import SmallestAI
    from smallestai.atoms.helpers import (
        MultiAgent, PlaybooksConfig, IntentRouter, Playbook,
    )

    client = SmallestAI(api_key="...")
    ma = MultiAgent(client)

    config = PlaybooksConfig(
        router=IntentRouter(fallback_playbook_id="general", classifier_model="gpt-4o-mini"),
        conversation_guide="You are Aria, a warm, concise support agent.",
        playbooks=[
            Playbook(
                id="card_fraud", name="Card fraud", intent_name="card_fraud",
                intent_description="Caller reports a lost/stolen card or fraud.",
                prompt="You handle card-fraud reports...",
                tool_refs=["tool_freeze_card"],
            ),
            Playbook(
                id="general", name="General", intent_name="general",
                intent_description="Anything else.", prompt="General support...",
            ),
        ],
    )

    # One call: create a brand-new multi-agent agent carrying this config, published + live.
    agent_id = ma.create_agent(name="Support bot", config=config)

    # Or write onto an existing multi-agent agent's live branch and publish:
    ma.publish_config(agent_id, config)

    # Round-trip: read the published config back.
    config_back = ma.read_config(agent_id)
"""

from __future__ import annotations

import dataclasses
import re
import typing
import warnings

from ..errors.forbidden_error import ForbiddenError
from .versioning import Versioning

# ── Limits + constraints mirrored from the platform schema (playbooks.ts) ─────────
# These are enforced at publish by the platform; we mirror them as fail-fast client
# checks so a malformed config is rejected before a network round-trip. The platform
# publish validator remains the source of truth.
MAX_PLAYBOOKS = 128
MAX_PLAYBOOK_PROMPT_CHARS = 30_000

# intentName structural guard — the full allowlist (letters/marks/digits/spaces +
# . , ' ’ _ ( ) & / -, >=1 alphanumeric, no consecutive slashes, <=64 chars) is
# enforced at publish; here we block control chars / angle brackets and require an
# alphanumeric so an obviously-bad label fails fast.
_INTENT_NAME_ALLOWED = re.compile(r"^[^\x00-\x1f<>]*$")

PlaybookAuthLevel = typing.Literal["none", "weak", "strong"]
PlaybookType = typing.Literal["free_form", "structured"]
VerificationOnFail = typing.Literal["downgrade", "handoff", "end"]

#: The platform ``WorkflowType`` value for a multi-agent (Playbooks) agent. The
#: generated ``WorkflowType`` literal does not list this yet (see module docstring).
WORKFLOW_TYPE_MULTI_AGENTS = "multi_agents"


class MultiAgentError(Exception):
    """A multi-agent Playbooks config failed client-side validation.

    Raised before any network call when the config violates a rule the platform
    would reject at publish (missing fallback, duplicate ids, etc.). Catching this
    lets callers distinguish "my config is wrong" from transport/API errors.
    """


class MultiAgentNotEntitledError(MultiAgentError):
    """The org/account is not on the multi-agent (Playbooks) allowlist.

    The platform gates ``workflowType = multi_agents`` behind a rollout allowlist and
    returns HTTP 403 ("Multi-Agent agents are not available for your account.") on
    create. This maps that 403 so callers can catch it distinctly. Note it is a 403,
    not the 400 plan-gate that ``PlanNotEntitledError`` covers, so it needs its own type.
    """


# ── Typed config models (mirror playbooks.ts) ────────────────────────────────────


@dataclasses.dataclass
class IntentRouter:
    """The intent router that classifies each turn and routes to a playbook.

    Args:
        fallback_playbook_id: Playbook id used when no intent matches. Required, and
            must reference an existing, enabled playbook in the same config.
        classifier_model: Model alias for the intent-classification call. Empty uses
            the orchestrator default.
        allow_mid_call_reroute: When True (default), the router may switch playbooks
            mid-call on an intent change.
    """

    fallback_playbook_id: str
    classifier_model: typing.Optional[str] = None
    allow_mid_call_reroute: bool = True

    def to_api(self) -> typing.Dict[str, typing.Any]:
        out: typing.Dict[str, typing.Any] = {
            "fallbackPlaybookId": self.fallback_playbook_id,
            "allowMidCallReroute": self.allow_mid_call_reroute,
        }
        if self.classifier_model is not None:
            out["classifierModel"] = self.classifier_model
        return out


@dataclasses.dataclass
class PlaybookAuth:
    """Shared authentication tools injected into playbooks by their ``auth_level``.

    Args:
        weak_tools: Tools that satisfy WEAK auth (caller recognition), e.g.
            ``identify_by_phone``. Each is an inline tool dict (same shape as a
            single-prompt tool / ``smallestai.atoms.helpers.Tool``).
        strong_tools: Tools that satisfy STRONG auth (full identity proof), e.g.
            ``verify_dob``.
    """

    weak_tools: typing.List[typing.Dict[str, typing.Any]] = dataclasses.field(default_factory=list)
    strong_tools: typing.List[typing.Dict[str, typing.Any]] = dataclasses.field(default_factory=list)

    def to_api(self) -> typing.Dict[str, typing.Any]:
        return {"weakTools": list(self.weak_tools), "strongTools": list(self.strong_tools)}


@dataclasses.dataclass
class Verification:
    """A named, reusable identity check imported into playbooks by reference.

    A playbook lists verification ids in ``Playbook.verification_ids``; the check is
    satisfied once every tool in ``tool_refs`` has succeeded on the call.

    Args:
        id: Stable id, referenced by ``Playbook.verification_ids``.
        name: Human label.
        instructions: Natural-language instructions for how the agent runs the check.
        tool_refs: Proof tools (ALL must succeed), referenced from the Tools tab by id/name.
        trigger_tool_refs: Trigger/helper tools (e.g. ``send_otp``) — never proofs.
        binds_principal: Passing this check resolves + locks which principal is on the line.
        max_retries: Wrong-value retries allowed before the check locks (1-10).
        on_fail: What happens when retries are exhausted.
    """

    id: str
    name: str = ""
    instructions: str = ""
    tool_refs: typing.List[str] = dataclasses.field(default_factory=list)
    trigger_tool_refs: typing.List[str] = dataclasses.field(default_factory=list)
    binds_principal: bool = True
    max_retries: int = 2
    on_fail: VerificationOnFail = "downgrade"

    def to_api(self) -> typing.Dict[str, typing.Any]:
        return {
            "id": self.id,
            "name": self.name,
            "instructions": self.instructions,
            "toolRefs": list(self.tool_refs),
            "triggerToolRefs": list(self.trigger_tool_refs),
            "bindsPrincipal": self.binds_principal,
            "maxRetries": self.max_retries,
            "onFail": self.on_fail,
        }


@dataclasses.dataclass
class Playbook:
    """A specialist: a focused prompt + a scoped subset of tools.

    Args:
        id: Stable id, referenced by the router and by call-path events.
        name: Customer-facing label (unique, case-insensitive, within a config).
        intent_name: Short intent label the classifier uses, e.g. ``card_fraud``
            (unique, case-insensitive, within a config).
        intent_description: Natural-language description of what routes a caller here —
            read by the classifier.
        prompt: The specialist system prompt.
        enabled: Whether this playbook participates in routing.
        tool_refs: Preferred tool wiring — ``tool_...`` registry ids from the agent's
            Tools tab that this playbook imports.
        tools: Inline tool dicts (legacy). Prefer ``tool_refs``.
        verification_ids: Verifications this playbook requires (ALL must pass).
        auth_level: Legacy identity-proof gate (``none``/``weak``/``strong``). The new
            runtime uses ``verification_ids``; ``auth_level`` is the legacy mechanism.
        domain: Optional grouping label (the "Category" in the Procedures UI).
        knowledge_base_id: Optional per-playbook knowledge base id.
        type: Execution style. ``free_form`` is the only supported mode; ``structured``
            is reserved and rejected by this writer (the platform runtime stubs it).
    """

    id: str
    name: str
    intent_name: str
    intent_description: str
    prompt: str
    enabled: bool = True
    tool_refs: typing.List[str] = dataclasses.field(default_factory=list)
    tools: typing.List[typing.Dict[str, typing.Any]] = dataclasses.field(default_factory=list)
    verification_ids: typing.List[str] = dataclasses.field(default_factory=list)
    auth_level: PlaybookAuthLevel = "none"
    domain: typing.Optional[str] = None
    knowledge_base_id: typing.Optional[str] = None
    type: PlaybookType = "free_form"

    def to_api(self) -> typing.Dict[str, typing.Any]:
        out: typing.Dict[str, typing.Any] = {
            "id": self.id,
            "name": self.name,
            "intentName": self.intent_name,
            "intentDescription": self.intent_description,
            "enabled": self.enabled,
            "type": self.type,
            "authLevel": self.auth_level,
            "prompt": self.prompt,
            "tools": list(self.tools),
            "toolRefs": list(self.tool_refs),
            "verificationIds": list(self.verification_ids),
        }
        if self.domain is not None:
            out["domain"] = self.domain
        if self.knowledge_base_id is not None:
            out["knowledgeBaseId"] = self.knowledge_base_id
        return out


@dataclasses.dataclass
class PlaybooksConfig:
    """The full multi-agent Playbooks config for one agent.

    Args:
        router: The intent router (required).
        playbooks: The specialist playbooks (at least one required; at least one enabled).
        auth: Shared auth tools injected by ``auth_level``.
        conversation_guide: Persona/style/global behaviour injected into EVERY
            specialist prompt (defined once instead of repeated per playbook).
        verifications: Named, reusable identity checks referenced via
            ``Playbook.verification_ids``.
        global_tool_refs: Tools visible every turn regardless of the active playbook.
        entity_list_tool / entity_detail_tool / entity_id_arg / principal_id_arg:
            Optional entity-resolution wiring.
    """

    router: IntentRouter
    playbooks: typing.List[Playbook]
    auth: typing.Optional[PlaybookAuth] = None
    conversation_guide: typing.Optional[str] = None
    verifications: typing.List[Verification] = dataclasses.field(default_factory=list)
    global_tool_refs: typing.List[str] = dataclasses.field(default_factory=list)
    entity_list_tool: typing.Optional[str] = None
    entity_detail_tool: typing.Optional[str] = None
    entity_id_arg: typing.Optional[str] = None
    principal_id_arg: typing.Optional[str] = None

    def to_api(self) -> typing.Dict[str, typing.Any]:
        """Serialize to the camelCase ``playbooks`` config body the platform stores."""
        out: typing.Dict[str, typing.Any] = {
            "router": self.router.to_api(),
            "playbooks": [p.to_api() for p in self.playbooks],
            "verifications": [v.to_api() for v in self.verifications],
            "globalToolRefs": list(self.global_tool_refs),
        }
        if self.auth is not None:
            out["auth"] = self.auth.to_api()
        if self.conversation_guide is not None:
            out["conversationGuide"] = self.conversation_guide
        for key, value in (
            ("entityListTool", self.entity_list_tool),
            ("entityDetailTool", self.entity_detail_tool),
            ("entityIdArg", self.entity_id_arg),
            ("principalIdArg", self.principal_id_arg),
        ):
            if value is not None:
                out[key] = value
        return out

    def validate(self) -> None:
        """Fail-fast client-side validation, mirroring the platform's publish refines.

        Raises ``MultiAgentError`` on the first violation. The platform re-validates
        at publish (``validateMultiAgentPlaybooks``) and is the source of truth; this
        just avoids a round-trip for obvious mistakes.
        """
        _validate_config(self)


# ── Validation (mirrors the zod .refine()s in playbooksConfigSchema) ──────────────


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise MultiAgentError(message)


def _validate_config(cfg: PlaybooksConfig) -> None:
    _require(len(cfg.playbooks) >= 1, "At least one playbook is required")
    _require(
        len(cfg.playbooks) <= MAX_PLAYBOOKS,
        f"Too many playbooks: {len(cfg.playbooks)} (max {MAX_PLAYBOOKS})",
    )

    defined_verification_ids = {v.id for v in cfg.verifications}

    for pb in cfg.playbooks:
        _require(bool(pb.id.strip()), "Every playbook needs a non-empty id")
        _require(bool(pb.name.strip()), f"Playbook '{pb.id}': name is required")
        _require(bool(pb.intent_name.strip()), f"Playbook '{pb.id}': intent_name is required")
        _require(len(pb.intent_name) <= 64, f"Playbook '{pb.id}': intent_name must be 64 characters or fewer")
        _require(
            bool(_INTENT_NAME_ALLOWED.match(pb.intent_name)) and bool(re.search(r"[^\W_]", pb.intent_name, re.UNICODE)),
            f"Playbook '{pb.id}': intent_name has invalid characters "
            "(letters/numbers/spaces and . , ' _ ( ) & / - only)",
        )
        _require("//" not in pb.intent_name, f"Playbook '{pb.id}': intent_name cannot contain consecutive slashes")
        _require(bool(pb.intent_description.strip()), f"Playbook '{pb.id}': intent_description is required")
        _require(bool(pb.prompt.strip()), f"Playbook '{pb.id}': prompt is required")
        _require(
            len(pb.prompt) <= MAX_PLAYBOOK_PROMPT_CHARS,
            f"Playbook '{pb.id}': prompt exceeds {MAX_PLAYBOOK_PROMPT_CHARS} characters",
        )
        # structured is reserved + not implemented in the runtime (UI offers it disabled).
        _require(
            pb.type == "free_form",
            f"Playbook '{pb.id}': type='structured' is reserved and not yet supported; use 'free_form'",
        )
        _require(
            pb.auth_level in ("none", "weak", "strong"),
            f"Playbook '{pb.id}': auth_level must be none/weak/strong",
        )
        for vid in pb.verification_ids:
            _require(
                vid in defined_verification_ids,
                f"Playbook '{pb.id}': verification_id '{vid}' does not match any defined verification",
            )

    # Unique ids / names / intent names (case-insensitive for name + intent_name).
    ids = [p.id for p in cfg.playbooks]
    _require(len(set(ids)) == len(ids), "Playbook ids must be unique")
    names = [p.name.strip().lower() for p in cfg.playbooks]
    _require(len(set(names)) == len(names), "Playbook names must be unique")
    intents = [p.intent_name.strip().lower() for p in cfg.playbooks]
    _require(len(set(intents)) == len(intents), "Playbook intent names must be unique")

    enabled = [p for p in cfg.playbooks if p.enabled]
    _require(len(enabled) >= 1, "At least one playbook must be enabled")

    # Fallback must reference an existing + enabled playbook.
    _require(bool(cfg.router.fallback_playbook_id), "router.fallback_playbook_id is required")
    fallback = next((p for p in cfg.playbooks if p.id == cfg.router.fallback_playbook_id), None)
    _require(
        fallback is not None,
        f"router.fallback_playbook_id '{cfg.router.fallback_playbook_id}' must reference an existing playbook",
    )
    _require(
        fallback is None or fallback.enabled,
        f"router.fallback_playbook_id '{cfg.router.fallback_playbook_id}' must reference an enabled playbook",
    )

    # An auth_level is meaningless without the shared tools that satisfy it.
    weak_tools = cfg.auth.weak_tools if cfg.auth else []
    strong_tools = cfg.auth.strong_tools if cfg.auth else []
    needs_weak = any(p.enabled and p.auth_level in ("weak", "strong") for p in cfg.playbooks)
    needs_strong = any(p.enabled and p.auth_level == "strong" for p in cfg.playbooks)
    _require(
        not needs_weak or len(weak_tools) > 0,
        "A playbook requires weak/strong auth but auth.weak_tools is empty — add a caller-recognition tool",
    )
    _require(
        not needs_strong or len(strong_tools) > 0,
        "A playbook requires strong auth but auth.strong_tools is empty — add an identity-proof tool",
    )


# ── The facade ────────────────────────────────────────────────────────────────────


class MultiAgent:
    """Typed reader/writer for the platform multi-agent Playbooks config.

    Wraps the generated agent + versioning clients and the ``Versioning`` helper.
    Rides future regens unchanged (it holds a reference to ``client``, not to any
    generated internals).

    Usage::

        from smallestai import SmallestAI
        from smallestai.atoms.helpers import MultiAgent

        ma = MultiAgent(SmallestAI(api_key="..."))
    """

    def __init__(self, client: typing.Any):
        self._client = client
        self._agents = client.atoms.agents
        self._branches = client.atoms.agent_versioning_branches
        self._revisions = client.atoms.agent_versioning_revisions
        self._versioning = Versioning(client)

    # -- branch resolution ---------------------------------------------------------

    def _default_branch_id(self, agent_id: str) -> str:
        """Return the agent's live/default (Main) branch id."""
        branches = self._branches.list(id=agent_id).data.branches
        if not branches:
            raise MultiAgentError(f"agent {agent_id} has no branches")
        for item in branches:
            inner = getattr(item, "branch", item)
            if getattr(inner, "is_default", False):
                return inner.id
        # Fall back to the first branch if none is flagged default.
        first = getattr(branches[0], "branch", branches[0])
        return first.id

    # -- create --------------------------------------------------------------------

    def create_agent(
        self,
        *,
        name: str,
        config: PlaybooksConfig,
        description: typing.Optional[str] = None,
        label: typing.Optional[str] = None,
        **create_kwargs: typing.Any,
    ) -> str:
        """Create a brand-new multi-agent agent carrying ``config``, published + live.

        Creates the agent with ``workflow_type = multi_agents`` (so every revision
        inherits it — the workflow type can only be set at create), writes the
        ``playbooks`` config onto its live branch, and publishes. Returns the new
        agent id.

        Extra ``create_kwargs`` are forwarded to ``agents.create_agent`` (e.g.
        ``synthesizer=``, ``language=``).

        Raises:
            MultiAgentError: the config failed client-side validation.
            MultiAgentNotEntitledError: the account is not on the multi-agent allowlist.
        """
        config.validate()
        # A global_prompt is required by create; multi-agent uses playbook prompts, so
        # a short placeholder is fine (the runtime reads the playbooks section).
        kwargs: typing.Dict[str, typing.Any] = {
            "name": name,
            "workflow_type": WORKFLOW_TYPE_MULTI_AGENTS,
        }
        if description is not None:
            kwargs["description"] = description
        kwargs.setdefault("global_prompt", create_kwargs.pop("global_prompt", name))
        kwargs.update(create_kwargs)
        try:
            created = self._agents.create_agent(**kwargs)
        except ForbiddenError as exc:
            raise self._as_entitlement_error(exc) from exc
        agent_id = self._extract_agent_id(created)
        self.publish_config(agent_id, config, label=label)
        return agent_id

    # -- write ---------------------------------------------------------------------

    def write_draft(
        self,
        agent_id: str,
        config: PlaybooksConfig,
        *,
        branch_id: typing.Optional[str] = None,
        expected_revision: typing.Optional[int] = None,
    ) -> typing.Any:
        """Write ``config`` to the branch's open draft without publishing.

        Structural validation runs client-side; the agent must already be a
        multi-agent agent (``workflow_type`` is set at create, not here). Returns the
        updated draft revision. Use ``publish_config`` for the common write+publish path.
        """
        config.validate()
        self._warn_unknown_tool_refs(config)
        branch_id = branch_id or self._default_branch_id(agent_id)
        # Omit expected_revision when None so we don't send a stray null — matches
        # edit_and_publish (publish_config), which only forwards it when set.
        kwargs: typing.Dict[str, typing.Any] = {"request_options": self._playbooks_body(config)}
        if expected_revision is not None:
            kwargs["expected_revision"] = expected_revision
        return self._versioning.update_draft(agent_id, branch_id, **kwargs)

    def publish_config(
        self,
        agent_id: str,
        config: PlaybooksConfig,
        *,
        branch_id: typing.Optional[str] = None,
        label: typing.Optional[str] = None,
        expected_revision: typing.Optional[int] = None,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> typing.Any:
        """Write ``config`` to the branch draft and publish it (the common path).

        Reuses ``Versioning.edit_and_publish`` — the same draft -> publish pipeline the
        dashboard uses — so the published config renders in the dashboard. Returns the
        published revision. Raises ``DraftConflictError`` if ``expected_revision`` is stale.
        """
        config.validate()
        self._warn_unknown_tool_refs(config)
        branch_id = branch_id or self._default_branch_id(agent_id)
        return self._versioning.edit_and_publish(
            agent_id,
            branch_id,
            label=label,
            expected_revision=expected_revision,
            timeout=timeout,
            poll_interval=poll_interval,
            request_options=self._playbooks_body(config),
        )

    # -- read ----------------------------------------------------------------------

    def read_config(
        self,
        agent_id: str,
        *,
        branch_id: typing.Optional[str] = None,
        revision_id: typing.Optional[str] = None,
    ) -> typing.Optional[PlaybooksConfig]:
        """Read the published Playbooks config back as a typed ``PlaybooksConfig``.

        Resolves the newest published revision on the branch (or ``revision_id`` if
        given) and parses its ``playbooks`` config section. Returns ``None`` when the
        agent has no playbooks config. Note: only *committed* (published) revisions
        carry a resolved config — a never-published draft reads back as ``None``.
        """
        raw = self.read_config_dict(agent_id, branch_id=branch_id, revision_id=revision_id)
        return config_from_api(raw) if raw else None

    def read_config_dict(
        self,
        agent_id: str,
        *,
        branch_id: typing.Optional[str] = None,
        revision_id: typing.Optional[str] = None,
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """Read the raw ``playbooks`` config section (camelCase dict), or ``None``.

        Resolves the newest *published* revision on the branch (or ``revision_id`` if
        given); in-flight draft / scanning / archived revisions are skipped. The
        escape hatch when you want the exact stored shape rather than the typed model
        (e.g. to inspect fields this SDK version does not model yet).
        """
        branch_id = branch_id or self._default_branch_id(agent_id)
        if revision_id is None:
            revisions = self._revisions.list(id=agent_id, branch_id=branch_id, limit=20).data.revisions or []
            # Only committed (published) revisions carry a resolved config; skip any
            # in-flight draft / archived rows so we return the newest *published* one
            # (a publish still scanning would otherwise read back as None).
            published = [r for r in revisions if getattr(r, "status", None) == "published"]
            if not published:
                return None
            revision_id = published[0].id
        got = self._revisions.get(id=agent_id, branch_id=branch_id, revision_id=revision_id)
        resolved = getattr(got.data, "resolved_config", None) or {}
        # The section is stored double-wrapped: resolved_config["playbooks"]["playbooks"]
        # is the config object (section name -> field name -> value). An empty section
        # or a non-multi-agent revision yields {} -> None.
        section = resolved.get("playbooks") if isinstance(resolved, dict) else None
        if not isinstance(section, dict):
            return None
        inner = section.get("playbooks")
        if not isinstance(inner, dict):
            return None
        return inner

    # -- internals -----------------------------------------------------------------

    @staticmethod
    def _playbooks_body(config: PlaybooksConfig) -> typing.Dict[str, typing.Any]:
        """The ``RequestOptions`` carrying the playbooks config in the draft body.

        The generated ``update_draft`` does not model a ``playbooks`` field, so it is
        sent through Fern's ``additional_body_parameters`` escape hatch (spread into
        the request body by the core http client). See module docstring.
        """
        return {"additional_body_parameters": {"playbooks": config.to_api()}}

    def _known_tool_ids(self) -> typing.Optional[typing.Set[str]]:
        """Best-effort set of the org's tool ids/names, or ``None`` if the lookup can't run.

        Queries the Tools library (``GET /tool``) on the same host/key as this client.
        Returns ``None`` on any error so a tools-lookup hiccup never blocks a publish.
        """
        try:
            from .tools import Tools

            wrapper = getattr(self._client, "_client_wrapper", None)
            api_key = wrapper._get_api_key() if wrapper is not None and hasattr(wrapper, "_get_api_key") else None
            env = wrapper.get_environment() if wrapper is not None and hasattr(wrapper, "get_environment") else None
            base_url = getattr(env, "atoms", None)
            if not api_key or not base_url:
                return None
            resp = Tools(base_url=base_url, api_key=api_key).list()
            if isinstance(resp, dict):
                items = resp.get("data") or resp.get("tools") or []
            elif isinstance(resp, list):
                items = resp
            else:
                items = []
            known: typing.Set[str] = set()
            for item in items:
                if isinstance(item, dict):
                    for key in ("toolId", "tool_id", "id", "_id", "name", "key"):
                        val = item.get(key)
                        if isinstance(val, str) and val:
                            known.add(val)
            return known
        except Exception:
            return None

    def check_tool_refs(self, config: PlaybooksConfig) -> typing.List[str]:
        """Return the config's ``tool_refs`` that match no tool in the org Tools library.

        Playbook / verification / global ``tool_refs`` are *references* to tools that must
        already exist in the library (matched by id or name). A ref to a tool that does not
        exist is dropped by the platform and shows as empty in the dashboard. This surfaces
        those at author time. Returns ``[]`` if everything resolves or if the lookup can't
        run (offline, no key) — it never raises.
        """
        known = self._known_tool_ids()
        if known is None:
            return []
        refs: typing.Set[str] = set(config.global_tool_refs)
        for pb in config.playbooks:
            refs.update(pb.tool_refs)
        for ver in config.verifications:
            refs.update(ver.tool_refs)
            refs.update(ver.trigger_tool_refs)
        for ref in (config.entity_list_tool, config.entity_detail_tool):
            if ref:
                refs.add(ref)
        return sorted(r for r in refs if r not in known)

    def _warn_unknown_tool_refs(self, config: PlaybooksConfig) -> None:
        """Emit a warning (never raise) for tool_refs that don't resolve to a real tool."""
        unknown = self.check_tool_refs(config)
        if unknown:
            warnings.warn(
                "These tool_refs do not match any tool in your org Tools library and will "
                f"show as empty in the dashboard: {unknown}. Create the tools first "
                "(e.g. Tools().create(...)) and reference their id/name, or remove the refs.",
                stacklevel=3,
            )

    @staticmethod
    def _extract_agent_id(created: typing.Any) -> str:
        """Pull the agent id from a create response.

        ``create_agent`` returns ``{status, data}`` where ``data`` is the id string.
        """
        data = getattr(created, "data", created)
        if isinstance(data, str):
            return data
        # Defensive: some shapes nest the id.
        for attr in ("id", "agent_id", "_id"):
            value = getattr(data, attr, None)
            if isinstance(value, str):
                return value
        raise MultiAgentError(f"could not determine agent id from create response: {created!r}")

    @staticmethod
    def _as_entitlement_error(exc: ForbiddenError) -> Exception:
        """Map a 403 to ``MultiAgentNotEntitledError`` when it's the allowlist denial."""
        body = getattr(exc, "body", None)
        if isinstance(body, dict):
            errors = body.get("errors")
            text = " ".join(errors) if isinstance(errors, list) else str(body.get("message") or body)
        else:
            text = str(body or "")
        if "multi-agent" in text.lower() or "not available for your account" in text.lower():
            return MultiAgentNotEntitledError(
                "This account is not on the multi-agent (Playbooks) allowlist. "
                "Contact Smallest to enable multi-agent agents."
            )
        return exc


# ── Deserialization (camelCase API dict -> typed model) ───────────────────────────


def _playbook_from_api(raw: typing.Dict[str, typing.Any]) -> Playbook:
    return Playbook(
        id=raw.get("id", ""),
        name=raw.get("name", ""),
        intent_name=raw.get("intentName", ""),
        intent_description=raw.get("intentDescription", ""),
        prompt=raw.get("prompt", ""),
        enabled=raw.get("enabled", True),
        tool_refs=list(raw.get("toolRefs", []) or []),
        tools=list(raw.get("tools", []) or []),
        verification_ids=list(raw.get("verificationIds", []) or []),
        auth_level=raw.get("authLevel", "none"),
        domain=raw.get("domain"),
        knowledge_base_id=raw.get("knowledgeBaseId"),
        type=raw.get("type", "free_form"),
    )


def _verification_from_api(raw: typing.Dict[str, typing.Any]) -> Verification:
    return Verification(
        id=raw.get("id", ""),
        name=raw.get("name", ""),
        instructions=raw.get("instructions", ""),
        tool_refs=list(raw.get("toolRefs", []) or []),
        trigger_tool_refs=list(raw.get("triggerToolRefs", []) or []),
        binds_principal=raw.get("bindsPrincipal", True),
        max_retries=raw.get("maxRetries", 2),
        on_fail=raw.get("onFail", "downgrade"),
    )


def config_from_api(raw: typing.Dict[str, typing.Any]) -> PlaybooksConfig:
    """Parse a stored ``playbooks`` config dict (camelCase) into a ``PlaybooksConfig``.

    The inverse of ``PlaybooksConfig.to_api``. Unknown fields are ignored.
    """
    router_raw = raw.get("router") or {}
    router = IntentRouter(
        fallback_playbook_id=router_raw.get("fallbackPlaybookId", ""),
        classifier_model=router_raw.get("classifierModel"),
        allow_mid_call_reroute=router_raw.get("allowMidCallReroute", True),
    )
    auth_raw = raw.get("auth")
    auth = None
    if isinstance(auth_raw, dict):
        auth = PlaybookAuth(
            weak_tools=list(auth_raw.get("weakTools", []) or []),
            strong_tools=list(auth_raw.get("strongTools", []) or []),
        )
    return PlaybooksConfig(
        router=router,
        playbooks=[_playbook_from_api(p) for p in (raw.get("playbooks") or [])],
        auth=auth,
        conversation_guide=raw.get("conversationGuide"),
        verifications=[_verification_from_api(v) for v in (raw.get("verifications") or [])],
        global_tool_refs=list(raw.get("globalToolRefs", []) or []),
        entity_list_tool=raw.get("entityListTool"),
        entity_detail_tool=raw.get("entityDetailTool"),
        entity_id_arg=raw.get("entityIdArg"),
        principal_id_arg=raw.get("principalIdArg"),
    )
