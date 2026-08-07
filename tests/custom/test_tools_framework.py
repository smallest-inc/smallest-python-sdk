"""smallestai.tools: registry + Exa tool (lazy third-party dep, crew-pluggable)."""
import asyncio

import pytest


def test_registry_lists_and_resolves_exa():
    from smallestai.tools import ExaSearchTool, get_tool, list_tools

    tools = list_tools()
    assert "exa_search" in tools
    assert get_tool("exa_search") is ExaSearchTool
    assert tools["exa_search"] is ExaSearchTool


def test_unknown_tool_raises_keyerror():
    from smallestai.tools import get_tool

    with pytest.raises(KeyError):
        get_tool("does-not-exist")


def test_tool_plugs_into_crew_registry():
    from smallestai.atoms.crew.tools import ToolRegistry
    from smallestai.tools import ExaSearchTool

    registry = ToolRegistry()
    ExaSearchTool(api_key="x").register(registry)
    names = {s["function"]["name"] for s in registry.get_schemas()}
    assert "web_search" in names


def test_importing_tools_does_not_require_exa_py():
    # importing the package + constructing the tool must not need exa-py
    import importlib

    importlib.import_module("smallestai.tools")
    importlib.import_module("smallestai.tools.exa")


def test_exa_run_without_exa_py_raises_clear_error():
    from smallestai.tools import ExaSearchTool

    try:
        import exa_py  # noqa: F401

        installed = True
    except ImportError:
        installed = False

    if installed:
        pytest.skip("exa-py is installed; the missing-dep path can't be exercised here")

    with pytest.raises(ImportError) as ei:
        asyncio.run(ExaSearchTool(api_key="x").run(query="hello"))
    assert 'smallestai[exa]' in str(ei.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
