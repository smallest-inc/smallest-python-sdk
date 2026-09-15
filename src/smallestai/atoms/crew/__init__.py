"""
Smallest AI Atoms Agent SDK.

A real-time WebSocket agent framework for building voice agents,
chatbots, and other interactive AI applications.

Usage:
    from smallestai.atoms.crew import AtomsCrewApp
    from smallestai.atoms.crew import CrewSession
    from smallestai.atoms.crew import OutputCrewNode, BackgroundCrewNode
    from smallestai.atoms.crew import OpenAIClient
    from smallestai.atoms.crew import function_tool, ToolRegistry

The submodule paths (e.g. ``smallestai.atoms.crew.server``) also work.
"""

from typing import TYPE_CHECKING

# Public API. Imported lazily via __getattr__ (PEP 562) so that importing this
# package does not eagerly pull in the crew runtime deps (fastapi, uvicorn, ...)
# that `server` and friends need. Access a name and it is imported on demand.
_LAZY_EXPORTS = {
    "AtomsCrewApp": "smallestai.atoms.crew.server",
    "CrewSession": "smallestai.atoms.crew.session",
    "OutputCrewNode": "smallestai.atoms.crew.nodes",
    "BackgroundCrewNode": "smallestai.atoms.crew.nodes",
    "OpenAIClient": "smallestai.atoms.crew.clients.openai",
    "function_tool": "smallestai.atoms.crew.tools",
    "ToolRegistry": "smallestai.atoms.crew.tools",
}

__all__ = list(_LAZY_EXPORTS.keys())

if TYPE_CHECKING:
    from smallestai.atoms.crew.clients.openai import OpenAIClient
    from smallestai.atoms.crew.nodes import BackgroundCrewNode, OutputCrewNode
    from smallestai.atoms.crew.server import AtomsCrewApp
    from smallestai.atoms.crew.session import CrewSession
    from smallestai.atoms.crew.tools import ToolRegistry, function_tool


def __getattr__(name: str):
    module_path = _LAZY_EXPORTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    return getattr(importlib.import_module(module_path), name)


def __dir__():
    return sorted(list(globals().keys()) + __all__)
