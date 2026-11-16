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

    headers = BaseClientWrapper(api_key="k", environment=SmallestAIEnvironment.PRODUCTION).get_headers()
    assert headers["X-Source"] == "smallest-python-sdk"


@pytest.mark.parametrize("entry", ["smallestai.client", "smallestai"])
def test_fresh_process_client_imports(entry):
    # Root imports used to patch the classes globally and hide direct-import bugs.
    import subprocess

    code = f"""
from {entry} import SmallestAI, AsyncSmallestAI
for cls in (SmallestAI, AsyncSmallestAI):
    client = cls(api_key="test-key")
    assert client.atoms is client.agents
    assert client.waves is client.speech
    streaming = client.waves.streaming_tts
    assert streaming is client.speech.streaming_tts
    assert streaming._raw_client._client_wrapper is client.speech._client_wrapper
"""
    subprocess.run([sys.executable, "-W", "ignore::DeprecationWarning", "-c", code], check=True)


@pytest.mark.parametrize("old,new", [("Atoms", "Agents"), ("Waves", "Speech")])
def test_legacy_class_imports(old, new):
    import importlib

    import smallestai

    for prefix in ("", "Async"):
        with pytest.warns(DeprecationWarning):
            legacy = getattr(smallestai, prefix + old + "Client")
        assert legacy is getattr(smallestai, prefix + new + "Client")
        legacy_module = importlib.import_module(f"smallestai.{old.lower()}.client")
        assert getattr(legacy_module, prefix + old + "Client") is legacy
        raw_module = importlib.import_module(f"smallestai.{old.lower()}.raw_client")
        assert getattr(raw_module, prefix + "Raw" + old + "Client") is getattr(
            raw_module, prefix + "Raw" + new + "Client"
        )


def test_verification_script_uses_renamed_paths(monkeypatch):
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[2] / "scripts/verify.py"
    spec = importlib.util.spec_from_file_location("sdk_verify", path)
    verify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verify)
    verify.check_wire_coverage()
    verify.check_helper_coverage()
    assert not verify.failures
    monkeypatch.setenv("SMALLEST_API_KEY", "test-key")
    monkeypatch.setenv("SMALLEST_BASE_URL", "http://localhost:9999")
    client = verify.live_client()
    assert client._client_wrapper.get_environment().atoms == "http://localhost:9999/atoms/v1"
    assert list(verify.read_methods(client))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
