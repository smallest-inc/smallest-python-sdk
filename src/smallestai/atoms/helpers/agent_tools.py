"""
Configure agent tools (transfer_call, end_call, api_call, ...) from code.

How agent config works now
--------------------------
Atoms runs on the **branch/revision** versioning model. Serving reads the live
branch's head revision, so tool/prompt edits must go through the branch flow:

    PUT   /agent/{id}/branches/{branchId}/draft            (open/patch a draft)
    POST  /agent/{id}/branches/{branchId}/draft/publish    (commit; security scan)
    POST  /agent/{id}/branches/{branchId}/live             (make committed revision live)

Writing the legacy workflow document (``PATCH /workflow/{id}``) does **not** take
effect on live calls under this model - serving ignores it. The v1
drafts/versions endpoints are deprecated and return 409.

``AgentTools`` wraps the whole branch flow. You address agents by *agentId*; it
resolves the live branch, merges tools into a draft (config is section-based, so
your prompt is never touched), publishes, waits for the security scan, and makes
the revision live.

Usage
-----
    from smallestai.atoms.helpers import AgentTools

    tools = AgentTools(api_key="sk_...")           # or SMALLEST_API_KEY env var

    # add a transfer-to-human tool and make it live (merges, keeps prompt + other tools)
    tools.add_transfer_call(
        "AGENT_ID",
        number="+15551234567",
        transfer_type="cold_transfer",     # or "warm_transfer"
        on_hold_music="relaxing_sound",    # audio while bridging, so it isn't blank
    )

    # inspect / remove
    for t in tools.get_tools("AGENT_ID"):
        print(t.type, t.name)
    tools.remove_tool("AGENT_ID", "transfer_call")

    # stage without going live (leaves a published revision you activate later)
    tools.add_transfer_call("AGENT_ID", number="+1555...", make_live=False)
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional, Union

import requests

from smallestai.atoms.types.tool import Tool
from smallestai.atoms.types.tool_transfer_option import ToolTransferOption

logger = logging.getLogger("smallestai.atoms.agent_tools")

DEFAULT_BASE_URL = "https://api.smallest.ai/atoms/v1"

ToolInput = Union[Tool, Dict[str, Any]]


class AgentToolsError(Exception):
    """An agent could not be configured for tools (no branch, publish failed, ...)."""


class AgentTools:
    """Read-modify-write tool configuration for single-prompt agents, via the
    branch/revision versioning flow.

    Can be used standalone::

        tools = AgentTools(api_key="sk_...")

    or pointed at a non-prod host::

        tools = AgentTools(api_key="sk_...", base_url="https://api.dev.smallest.ai/atoms/v1")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        request_timeout: float = 30.0,
        publish_timeout: float = 120.0,
        poll_interval: float = 3.0,
    ):
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")
        self.base_url = (base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.request_timeout = request_timeout
        self.publish_timeout = publish_timeout
        self.poll_interval = poll_interval

    # ------------------------------------------------------------------ transport
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _raise_for_status(self, resp: "requests.Response", method: str, path: str) -> None:
        if resp.status_code < 400:
            return
        try:
            detail = resp.json()
        except ValueError:
            detail = (resp.text or "")[:300]
        raise AgentToolsError(f"{method} {path} -> HTTP {resp.status_code}: {detail}")

    def _unwrap(self, body: Any) -> Any:
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body

    def _get(self, path: str) -> Any:
        resp = requests.get(f"{self.base_url}/{path}", headers=self._headers(), timeout=self.request_timeout)
        self._raise_for_status(resp, "GET", path)
        return self._unwrap(resp.json())

    def _put(self, path: str, json_body: Dict[str, Any]) -> Any:
        resp = requests.put(
            f"{self.base_url}/{path}", headers=self._headers(), json=json_body, timeout=self.request_timeout
        )
        self._raise_for_status(resp, "PUT", path)
        return self._unwrap(resp.json())

    def _post(self, path: str, json_body: Dict[str, Any]) -> "requests.Response":
        resp = requests.post(
            f"{self.base_url}/{path}", headers=self._headers(), json=json_body, timeout=self.request_timeout
        )
        self._raise_for_status(resp, "POST", path)
        return resp

    # ------------------------------------------------------------- branch resolution
    def _live_branch(self, agent_id: str) -> Dict[str, Any]:
        data = self._get(f"agent/{agent_id}/branches")
        entries = (data or {}).get("branches") or []
        if not entries:
            raise AgentToolsError(f"agent {agent_id!r} has no branches; cannot configure tools")
        for entry in entries:
            if entry.get("isLive"):
                return entry["branch"]
        for entry in entries:
            if (entry.get("branch") or {}).get("isDefault"):
                return entry["branch"]
        return entries[0]["branch"]

    def _branch_by_id(self, agent_id: str, branch_id: str) -> Dict[str, Any]:
        data = self._get(f"agent/{agent_id}/branches")
        for entry in (data or {}).get("branches") or []:
            branch = entry.get("branch") or {}
            if branch.get("_id") == branch_id:
                return branch
        raise AgentToolsError(f"branch {branch_id!r} not found on agent {agent_id!r}")

    def _resolved_config(self, agent_id: str, branch: Dict[str, Any]) -> Dict[str, Any]:
        head = branch.get("headRevisionId")
        if not head:
            return {}
        rev = self._get(f"agent/{agent_id}/branches/{branch['_id']}/revisions/{head}")
        return (rev or {}).get("resolvedConfig", {}) or {}

    @staticmethod
    def _tools_from_config(resolved_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        return list((resolved_config.get("workflow_tools") or {}).get("tools") or [])

    # ------------------------------------------------------------------ serialization
    @staticmethod
    def _to_wire(tool: ToolInput) -> Dict[str, Any]:
        if isinstance(tool, Tool):
            wire = tool.dict(by_alias=True, exclude_none=True)
        elif isinstance(tool, dict):
            wire = dict(tool)
        else:
            raise AgentToolsError(f"tool must be a Tool or dict, got {type(tool).__name__}")
        # Fern's exclude_none does NOT drop fields explicitly set to None, and the
        # API rejects nulls on optional fields ("Expected boolean, received null").
        return {k: v for k, v in wire.items() if v is not None}

    @staticmethod
    def _tool_name(tool_dict: Dict[str, Any]) -> Optional[str]:
        return tool_dict.get("name")

    # ------------------------------------------------------------------ publish flow
    def _publish_and_wait(self, agent_id: str, branch_id: str, label: str) -> str:
        """Publish the open draft and wait for the security scan to commit a new
        revision. Returns the new head revision id."""
        source_head = self._branch_by_id(agent_id, branch_id).get("headRevisionId")
        resp = self._post(
            f"agent/{agent_id}/branches/{branch_id}/draft/publish", {"label": label}
        )
        body = resp.json() if resp.content else {}
        state = ((body or {}).get("data") or {}).get("state")
        # 200 {state: "committed"} = synchronous; 202 {state: "scanning"} = async scan.
        if resp.status_code == 200 and state == "committed":
            return self._branch_by_id(agent_id, branch_id).get("headRevisionId")

        deadline = time.time() + self.publish_timeout
        while time.time() < deadline:
            branch = self._branch_by_id(agent_id, branch_id)
            head = branch.get("headRevisionId")
            if head and head != source_head:
                rev = self._get(f"agent/{agent_id}/branches/{branch_id}/revisions/{head}")
                status = ((rev or {}).get("revision") or {}).get("status")
                if status in ("committed", "published"):
                    return head
            time.sleep(self.poll_interval)
        raise AgentToolsError(
            f"publish for agent {agent_id!r} did not commit within {self.publish_timeout:.0f}s "
            "(security scan may still be running or may have failed)"
        )

    # ------------------------------------------------------------------ public API
    def get_tools(self, agent_id: str) -> List[Tool]:
        """Return the agent's current live tools as typed :class:`Tool` models."""
        branch = self._live_branch(agent_id)
        raw = self._tools_from_config(self._resolved_config(agent_id, branch))
        out: List[Tool] = []
        for entry in raw:
            try:
                out.append(Tool(**entry))
            except Exception:
                out.append(entry)  # type: ignore[arg-type]
        return out

    def set_tools(
        self,
        agent_id: str,
        tools: List[ToolInput],
        *,
        replace: bool = False,
        make_live: bool = True,
        label: str = "SDK tool update",
    ) -> List[Dict[str, Any]]:
        """Write ``tools`` through the branch flow (draft -> publish -> make-live).

        Default merges by tool ``name`` (incoming overwrite same-named tools; other
        tools and the prompt are preserved - config is section-based). ``replace=True``
        overwrites the whole tool list. ``make_live=False`` publishes a revision but
        does not activate it.

        Returns the tool list (wire dicts) that was written.
        """
        branch = self._live_branch(agent_id)
        branch_id = branch["_id"]
        incoming = [self._to_wire(t) for t in tools]

        if replace:
            merged = incoming
        else:
            by_name: Dict[Optional[str], Dict[str, Any]] = {}
            for existing in self._tools_from_config(self._resolved_config(agent_id, branch)):
                by_name[self._tool_name(existing)] = existing
            for tool in incoming:
                by_name[self._tool_name(tool)] = tool
            merged = list(by_name.values())

        logger.info(
            "AgentTools.set_tools agent=%s branch=%s tools=%s replace=%s make_live=%s",
            agent_id, branch_id, [self._tool_name(t) for t in merged], replace, make_live,
        )
        self._put(
            f"agent/{agent_id}/branches/{branch_id}/draft",
            {"singlePromptConfig": {"tools": merged}},
        )
        self._publish_and_wait(agent_id, branch_id, label)
        logger.info("AgentTools.set_tools published agent=%s", agent_id)
        if make_live:
            self._post(f"agent/{agent_id}/branches/{branch_id}/live", {})
            logger.info("AgentTools.set_tools made live agent=%s (%d tool(s))", agent_id, len(merged))
        return merged

    def remove_tool(self, agent_id: str, name: str, *, make_live: bool = True) -> List[Dict[str, Any]]:
        """Remove the tool with the given ``name`` (no-op if absent)."""
        branch = self._live_branch(agent_id)
        kept = [
            t
            for t in self._tools_from_config(self._resolved_config(agent_id, branch))
            if self._tool_name(t) != name
        ]
        logger.info("AgentTools.remove_tool agent=%s name=%s", agent_id, name)
        return self.set_tools(agent_id, kept, replace=True, make_live=make_live, label=f"remove {name}")  # type: ignore[arg-type]

    def add_transfer_call(
        self,
        agent_id: str,
        *,
        number: str,
        transfer_type: str = "cold_transfer",
        name: str = "transfer_call",
        description: Optional[str] = None,
        on_hold_music: Optional[str] = None,
        transfer_only_if_human: Optional[bool] = None,
        enabled: bool = True,
        make_live: bool = True,
        **extra: Any,
    ) -> Tool:
        """Add a ``transfer_call`` tool that forwards the call to ``number``.

        Parameters
        ----------
        number : str
            E.164 destination, e.g. ``"+15551234567"``.
        transfer_type : str
            ``"cold_transfer"`` (blind) or ``"warm_transfer"``.
        on_hold_music : str, optional
            Audio played to the caller while the transfer bridges, so the line is
            not silent. One of ``"ringtone"``, ``"relaxing_sound"``,
            ``"uplifting_beats"``, ``"none"``.
        transfer_only_if_human : bool, optional
            Only transfer if a human (not voicemail) answers the destination.
        make_live : bool
            Publish and activate immediately (default). ``False`` stages it.

        The tool is merged into the agent's existing tools; the prompt and other
        tools are preserved. Returns the :class:`Tool` that was written.
        """
        kwargs: Dict[str, Any] = dict(
            type="transfer_call",
            name=name,
            description=description
            or "Transfer the call to a human agent or specialist when the caller asks.",
            enabled=enabled,
            transfer_number=number,
            transfer_option=ToolTransferOption(type=transfer_type),
        )
        if on_hold_music is not None:
            kwargs["on_hold_music"] = on_hold_music
        if transfer_only_if_human is not None:
            kwargs["transfer_only_if_human"] = transfer_only_if_human
        kwargs.update(extra)
        tool = Tool(**kwargs)
        self.set_tools(agent_id, [tool], make_live=make_live, label="add transfer_call")
        return tool
