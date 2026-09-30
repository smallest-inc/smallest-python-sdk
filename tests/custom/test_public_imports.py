"""Guards the documented public import surface of `smallestai.atoms.crew`.

A customer hit `ImportError` on `from smallestai.atoms.crew import AtomsCrewApp`
because `crew/__init__` exported nothing (the imports there lived only in the
docstring). Both the module docstring and the docs advertise this short path, so
lock it here: if the package stops exporting a public symbol, this test fails in
CI rather than in a customer's notebook.
"""

import importlib

CREW_PUBLIC = [
    "AtomsCrewApp",
    "CrewSession",
    "OutputCrewNode",
    "BackgroundCrewNode",
    "OpenAIClient",
    "function_tool",
    "ToolRegistry",
]


def test_crew_all_advertises_public_api():
    mod = importlib.import_module("smallestai.atoms.crew")
    assert set(CREW_PUBLIC) <= set(mod.__all__)


def test_crew_public_symbols_resolve_from_short_path():
    from smallestai.atoms.crew import (  # noqa: F401
        AtomsCrewApp,
        BackgroundCrewNode,
        CrewSession,
        OpenAIClient,
        OutputCrewNode,
        ToolRegistry,
        function_tool,
    )

    for sym in (
        AtomsCrewApp,
        CrewSession,
        OutputCrewNode,
        BackgroundCrewNode,
        OpenAIClient,
        ToolRegistry,
        function_tool,
    ):
        assert sym is not None


def test_unknown_attr_raises_attributeerror():
    mod = importlib.import_module("smallestai.atoms.crew")
    try:
        mod.DefinitelyNotAThing
    except AttributeError:
        return
    raise AssertionError("expected AttributeError for an unknown attribute")
