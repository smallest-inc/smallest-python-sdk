"""6.0 rename (atoms->agents, waves->speech): new names work, old names still
work as deprecated aliases (client attribute + deep imports), and the observability
header is intact.
"""
import sys
import warnings

import pytest

from smallestai import SmallestAI


def _client():
    return SmallestAI(api_key="test-key")


def test_new_namespaces():
    c = _client()
    assert type(c.agents).__name__ == "AgentsClient"
    assert type(c.speech).__name__ == "SpeechClient"


def test_client_atoms_waves_aliases_are_deprecated():
    c = _client()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert c.atoms is c.agents
        assert c.waves is c.speech
    cats = [x.category for x in w]
    assert DeprecationWarning in cats


def test_deep_import_backcompat_same_objects():
    from smallestai.agents.crew.nodes import OutputCrewNode as New
    from smallestai.speech.helpers import synthesize_to_file as new_helper

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from smallestai.atoms.crew.nodes import OutputCrewNode as Old  # type: ignore[import-not-found]
        from smallestai.waves.helpers import synthesize_to_file as old_helper  # type: ignore[import-not-found]

    assert Old is New
    assert old_helper is new_helper


def test_deep_import_emits_deprecation_warning():
    # The finder warns once per top-level name; reset so this test sees it
    # regardless of what earlier tests imported.
    import smallestai._compat as compat

    compat._warned.clear()
    sys.modules.pop("smallestai.atoms.calls", None)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        import smallestai.atoms.calls  # type: ignore[import-not-found]  # noqa: F401
    assert any(issubclass(x.category, DeprecationWarning) for x in w)


def test_plan_not_entitled_error_still_exported():
    from smallestai import PlanNotEntitledError
    from smallestai.errors import PlanNotEntitledError as FromErrors

    assert PlanNotEntitledError is FromErrors


def test_observability_header_survives_rename():
    from smallestai.core.client_wrapper import BaseClientWrapper
    from smallestai.environment import SmallestAIEnvironment

    headers = BaseClientWrapper(
        api_key="k", environment=SmallestAIEnvironment.PRODUCTION
    ).get_headers()
    assert headers["X-Source"] == "smallest-python-sdk"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
