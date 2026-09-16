"""
Reusable Tools library.

The org-level Tools registry: create a tool once and reference it from any number
of agents by its ``toolId``. Two types are registry tools — ``api_call`` and
``client_tool``. System tools (transfer, end-call, knowledge-base search) are
configured per-agent, not here.

Usage:
    from smallestai.atoms.helpers import Tools

    tools = Tools()
    created = tools.create({
        "type": "api_call",
        "name": "get_order_status",
        "description": "Look up an order by id.",
        "method": "GET",
        "url": "https://api.example.com/orders/{{order_id}}",
        "llmParameters": [
            {"name": "order_id", "type": "text", "description": "The order id", "required": True}
        ],
    })
    tool_id = created["data"]["toolId"]
    tools.list()
    tools.update(tool_id, {...})
    tools.duplicate(tool_id)
    tools.delete(tool_id)
"""

import os
from typing import Any, Dict, Optional

import requests

DEFAULT_BASE_URL = "https://api.smallest.ai/atoms/v1"


class Tools:
    """Manager for the org Tools library (``/tool``).

    Standalone:
        tools = Tools()
        tools.list()
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Args:
            base_url: API base URL (default: api.smallest.ai/atoms/v1)
            api_key: API key (default: SMALLEST_API_KEY env var)
        """
        self.base_url = base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list(self) -> Dict[str, Any]:
        """List the org's tools."""
        url = f"{self.base_url}/tool"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def create(self, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tool.

        Args:
            definition: the tool body (``type`` ``api_call`` or ``client_tool``,
                plus ``name``, ``description``, and the fields for that type).
        """
        url = f"{self.base_url}/tool"
        response = requests.post(url, headers=self._get_headers(), json={"definition": definition})
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def update(self, tool_id: str, definition: Dict[str, Any]) -> Dict[str, Any]:
        """Update a tool. Propagates to every agent that references it."""
        url = f"{self.base_url}/tool/{tool_id}"
        response = requests.patch(url, headers=self._get_headers(), json={"definition": definition})
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def duplicate(self, tool_id: str) -> Dict[str, Any]:
        """Duplicate a tool into a new library tool with a new ``toolId``."""
        url = f"{self.base_url}/tool/{tool_id}/duplicate"
        response = requests.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def delete(self, tool_id: str) -> Dict[str, Any]:
        """Delete a tool. Blocked (400) while any agent still references it."""
        url = f"{self.base_url}/tool/{tool_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]
