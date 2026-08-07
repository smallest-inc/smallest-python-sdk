"""Base class for prebuilt crew tools."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from smallestai.atoms.crew.tools import ToolRegistry


class Tool:
    """A prebuilt tool wrapping a third-party capability.

    Subclasses implement an async ``run`` method decorated with ``@function_tool`` (so the
    crew can auto-extract its schema and the LLM can call it), and set ``name`` /
    ``description``. ``run`` stays directly callable for standalone use.
    """

    name: str = ""
    description: str = ""

    def register(self, registry: "ToolRegistry") -> None:
        """Add this tool's ``run`` to a crew ``ToolRegistry`` so the agent's LLM can call it.

            search = ExaSearchTool()
            search.register(self.tool_registry)
        """
        run = getattr(self, "run", None)
        if run is None or not hasattr(run, "__tool_info__"):
            raise TypeError(
                f"{type(self).__name__}.run must be decorated with @function_tool to be "
                "registered with a crew ToolRegistry."
            )
        registry.register(run)
