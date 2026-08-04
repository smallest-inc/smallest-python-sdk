"""
Configure agent tools (transfer_call, end_call, api_call, ...) from code.

Why this helper exists
----------------------
Setting tools on a single-prompt agent from code is possible today, but the raw
surface has three footguns that make it feel impossible:

* The versioned drafts API (``POST /agent/{id}/drafts/...``) is not reachable on
  the public API host (it returns 404). The deployed write path is the legacy
  workflow document.
* That write path is ``PATCH /workflow/{workflowId}`` — it takes the *workflowId*
  (``agent.workflowId``), not the agentId, and it does not merge: a partial
  payload silently wipes the prompt and any tools you did not resend.
* The wire fields are camelCase aliases (``transferNumber``, ``onHoldMusic``, ...),
  easy to get wrong by hand.

``AgentTools`` wraps all of that. You address agents by *agentId*, it always
read-modify-writes (so the prompt and existing tools are never wiped), and you
pass typed :class:`~smallestai.atoms.types.tool.Tool` models.

Caveat: this writes the legacy workflow document directly. On an agent that is
actively using the versioning system, a later version activation can overwrite
the legacy doc. On the public API today versioning is not reachable, so the
legacy doc is authoritative — but if you adopt drafts/versioning later, move tool
edits into that flow.

Usage
-----
    from smallestai.atoms.helpers import AgentTools

    tools = AgentTools(api_key="sk_...")           # or SMALLEST_API_KEY env var

    # add a transfer-to-human tool (merges, keeps prompt + other tools)
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
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional, Union

import requests

from smallestai.atoms.types.tool import Tool
from smallestai.atoms.types.tool_transfer_option import ToolTransferOption

logger = logging.getLogger("smallestai.atoms.agent_tools")

DEFAULT_BASE_URL = "https://api.smallest.ai/atoms/v1"

ToolInput = Union[Tool, Dict[str, Any]]


class AgentToolsError(Exception):
    """An agent could not be configured for tools (missing workflowId, wrong type, ...)."""


class AgentTools:
    """Read-modify-write tool configuration for single-prompt agents.

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
    ):
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")
        self.base_url = (base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.request_timeout = request_timeout

    # ------------------------------------------------------------------ transport
    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _unwrap(self, body: Any) -> Any:
        # Atoms wraps successful reads as {"status": true, "data": {...}}.
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body

    def _raise_for_status(self, resp: "requests.Response", method: str, path: str) -> None:
        if resp.status_code < 400:
            return
        # Surface the API's error body — a bare HTTPError hides why the write failed.
        try:
            detail = resp.json()
        except ValueError:
            detail = (resp.text or "")[:300]
        raise AgentToolsError(f"{method} {path} -> HTTP {resp.status_code}: {detail}")

    def _get(self, path: str) -> Any:
        resp = requests.get(f"{self.base_url}/{path}", headers=self._headers(), timeout=self.request_timeout)
        self._raise_for_status(resp, "GET", path)
        return self._unwrap(resp.json())

    def _patch(self, path: str, json_body: Dict[str, Any]) -> Any:
        resp = requests.patch(
            f"{self.base_url}/{path}", headers=self._headers(), json=json_body, timeout=self.request_timeout
        )
        self._raise_for_status(resp, "PATCH", path)
        return resp.json()

    # ------------------------------------------------------------- config resolution
    def _agent_doc(self, agent_id: str) -> Dict[str, Any]:
        doc = self._get(f"agent/{agent_id}")
        if not isinstance(doc, dict):
            raise AgentToolsError(f"unexpected agent document for {agent_id!r}: {type(doc).__name__}")
        return doc

    def _workflow_id(self, agent_id: str) -> str:
        doc = self._agent_doc(agent_id)
        workflow_id = doc.get("workflowId") or doc.get("workflow_id")
        if not workflow_id:
            raise AgentToolsError(
                f"agent {agent_id!r} has no workflowId; cannot configure tools on it"
            )
        workflow_type = doc.get("workflowType") or doc.get("workflow_type") or "single_prompt"
        if workflow_type != "single_prompt":
            raise AgentToolsError(
                f"agent {agent_id!r} is workflow_type={workflow_type!r}; AgentTools only "
                "configures single_prompt agents. For workflow_graph agents, tools live on "
                "the graph's transfer_call / api_call nodes."
            )
        return workflow_id

    def _workflow_config(self, agent_id: str) -> Dict[str, Any]:
        cfg = self._get(f"agent/{agent_id}/workflow")
        return cfg if isinstance(cfg, dict) else {}

    # ------------------------------------------------------------------ serialization
    @staticmethod
    def _to_wire(tool: ToolInput) -> Dict[str, Any]:
        if isinstance(tool, Tool):
            wire = tool.dict(by_alias=True, exclude_none=True)
        elif isinstance(tool, dict):
            wire = dict(tool)
        else:
            raise AgentToolsError(f"tool must be a Tool or dict, got {type(tool).__name__}")
        # Fern's exclude_none does NOT drop fields that were explicitly set to None
        # (e.g. Tool(transfer_only_if_human=None)), and the API rejects nulls on
        # optional fields ("Expected boolean, received null"). Strip them here.
        return {k: v for k, v in wire.items() if v is not None}

    @staticmethod
    def _tool_name(tool_dict: Dict[str, Any]) -> Optional[str]:
        return tool_dict.get("name")

    # ------------------------------------------------------------------ public API
    def get_tools(self, agent_id: str) -> List[Tool]:
        """Return the agent's current tools as typed :class:`Tool` models.

        Unknown/forward-compat tool shapes are returned as raw dicts rather than
        dropped, so nothing is silently lost.
        """
        raw = self._workflow_config(agent_id).get("tools") or []
        out: List[Tool] = []
        for entry in raw:
            try:
                out.append(Tool(**entry))
            except Exception:  # tolerate shapes the current models don't know about
                out.append(entry)  # type: ignore[arg-type]
        return out

    def set_tools(
        self,
        agent_id: str,
        tools: List[ToolInput],
        *,
        replace: bool = False,
    ) -> List[Dict[str, Any]]:
        """Write ``tools`` to the agent.

        Default is a merge keyed by tool ``name`` (incoming tools overwrite an
        existing tool of the same name; other existing tools and the prompt are
        preserved). ``replace=True`` overwrites the whole tool list.

        Returns the tool list (wire dicts) that was written.
        """
        workflow_id = self._workflow_id(agent_id)
        cfg = self._workflow_config(agent_id)
        prompt = cfg.get("prompt") or ""
        incoming = [self._to_wire(t) for t in tools]

        if replace:
            merged = incoming
        else:
            by_name: Dict[Optional[str], Dict[str, Any]] = {}
            for existing in cfg.get("tools") or []:
                by_name[self._tool_name(existing)] = existing
            for tool in incoming:
                by_name[self._tool_name(tool)] = tool
            merged = list(by_name.values())

        logger.info(
            "AgentTools.set_tools agent=%s workflow=%s tools=%s replace=%s",
            agent_id,
            workflow_id,
            [self._tool_name(t) for t in merged],
            replace,
        )
        self._patch(
            f"workflow/{workflow_id}",
            {"type": "single_prompt", "singlePromptConfig": {"prompt": prompt, "tools": merged}},
        )
        logger.info("AgentTools.set_tools OK agent=%s wrote %d tool(s)", agent_id, len(merged))
        return merged

    def remove_tool(self, agent_id: str, name: str) -> List[Dict[str, Any]]:
        """Remove the tool with the given ``name`` (no-op if absent)."""
        kept = [t for t in (self._workflow_config(agent_id).get("tools") or []) if self._tool_name(t) != name]
        logger.info("AgentTools.remove_tool agent=%s name=%s", agent_id, name)
        return self.set_tools(agent_id, kept, replace=True)  # type: ignore[arg-type]

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
        **extra: Any,
    ) -> Tool:
        """Add a ``transfer_call`` tool that forwards the call to ``number``.

        Parameters
        ----------
        number : str
            E.164 destination, e.g. ``"+15551234567"``.
        transfer_type : str
            ``"cold_transfer"`` (hang up on connect) or ``"warm_transfer"``.
        on_hold_music : str, optional
            Audio played to the caller while the transfer bridges, so the line is
            not silent. One of ``"ringtone"``, ``"relaxing_sound"``,
            ``"uplifting_beats"``, ``"none"``.
        transfer_only_if_human : bool, optional
            Only transfer if a human (not voicemail) answers the destination.

        The tool is merged into the agent's existing tools; the prompt and other
        tools are preserved. Returns the :class:`Tool` that was written.
        """
        # Only pass optionals that have a value — the API rejects explicit nulls,
        # and tool descriptions are restricted to a limited charset (no '+', so the
        # default cannot embed the E.164 number).
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
        self.set_tools(agent_id, [tool])
        return tool
