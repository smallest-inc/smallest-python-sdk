"""Prebuilt, pluggable tools for crew agents.

Each tool is a small class wrapping a third-party capability (web search, etc.) with a
``@function_tool``-decorated ``run`` method, so it drops straight into a crew's
``ToolRegistry`` and can also be called directly. Third-party libraries are optional
extras, lazy-imported on first use with a clear "install the extra" error.

    from smallestai.tools import ExaSearchTool

    search = ExaSearchTool()          # reads EXA_API_KEY
    # inside a crew node:
    search.register(self.tool_registry)
    # or standalone:
    results = await search.run(query="latest news on voice AI")

Discover what's available:

    from smallestai.tools import list_tools, get_tool
    list_tools()                      # {"exa_search": ExaSearchTool, ...}
"""
from __future__ import annotations

import importlib
from typing import Dict, Type

from smallestai.tools.base import Tool

# name -> "module:ClassName". Lazy so importing this package never pulls a third-party lib.
_REGISTRY: Dict[str, str] = {
    "exa_search": "smallestai.tools.exa:ExaSearchTool",
}


def list_tools() -> Dict[str, Type[Tool]]:
    """Return every available tool as ``{name: class}`` (imports each tool module)."""
    out: Dict[str, Type[Tool]] = {}
    for name in _REGISTRY:
        out[name] = get_tool(name)
    return out


def get_tool(name: str) -> Type[Tool]:
    """Return a tool class by registry name (e.g. ``"exa_search"``)."""
    try:
        path = _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(f"Unknown tool {name!r}. Available: {sorted(_REGISTRY)}") from exc
    module_path, _, class_name = path.partition(":")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def __getattr__(name: str):  # PEP 562: expose tool classes lazily at package level
    for reg_name, path in _REGISTRY.items():
        if path.endswith(":" + name):
            return get_tool(reg_name)
    raise AttributeError(f"module 'smallestai.tools' has no attribute {name!r}")


__all__ = ["Tool", "list_tools", "get_tool", "ExaSearchTool"]
