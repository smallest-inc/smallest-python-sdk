"""Exa web-search tool for crew agents.

    from smallestai.tools import ExaSearchTool
    search = ExaSearchTool()                 # reads EXA_API_KEY
    search.register(self.tool_registry)      # inside a crew node

Requires the exa extra:  pip install "smallestai[exa]"
"""

from __future__ import annotations

import asyncio
import os
import typing

from smallestai.atoms.crew.tools import function_tool
from smallestai.tools.base import Tool

_INSTALL_HINT = 'pip install "smallestai[exa]"'


class ExaSearchTool(Tool):
    name = "exa_search"
    description = "Search the web for current information using Exa."

    def __init__(self, api_key: typing.Optional[str] = None) -> None:
        self._api_key = api_key or os.getenv("EXA_API_KEY")
        self._client: typing.Any = None

    def _get_client(self) -> typing.Any:
        if self._client is not None:
            return self._client
        try:
            from exa_py import Exa  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ImportError(
                "ExaSearchTool requires the exa-py package. Install it with:\n    " + _INSTALL_HINT
            ) from exc
        if not self._api_key:
            raise ValueError("No Exa API key. Pass api_key=... or set the EXA_API_KEY env var.")
        self._client = Exa(self._api_key)
        return self._client

    @function_tool(name="web_search")
    async def run(self, query: str, num_results: int = 3) -> str:
        """Search the web for up-to-date information and return the top results.

        Args:
            query: What to search the web for.
            num_results: How many results to return (default 3).
        """
        client = self._get_client()
        # exa-py is synchronous; run it off the event loop so we don't block the call.
        response = await asyncio.to_thread(client.search_and_contents, query, num_results=num_results, text=True)
        results = getattr(response, "results", None) or []
        if not results:
            return f"No results found for {query!r}."
        lines = []
        for r in results:
            title = getattr(r, "title", "") or ""
            url = getattr(r, "url", "") or ""
            text = (getattr(r, "text", "") or "")[:500].strip()
            lines.append("\n".join(part for part in (f"- {title}", f"  {url}", f"  {text}") if part.strip()))
        return "\n".join(lines)
