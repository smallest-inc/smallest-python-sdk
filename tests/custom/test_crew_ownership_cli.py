"""Crew config-ownership surfacing: ownership module, deprecation, doctor command."""

import warnings

from rich.console import Console


def test_ownership_module_has_data_and_renders():
    from smallestai.cli.lib import ownership

    assert ownership.CREW_OWNS
    assert ownership.PLATFORM_OWNS
    assert ownership.DASHBOARD_NO_OPS
    assert "LLM turn" in ownership.SUMMARY
    # any platform-owned field mentions redaction (the key gotcha)
    assert any("redaction" in field.lower() for _, field in ownership.PLATFORM_OWNS)
    ownership.render_ownership(Console())  # must not raise


def test_override_event_is_deprecated():
    from smallestai.atoms.crew.events import SDKSystemUpdateOutputAgentSettingsEvent

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        SDKSystemUpdateOutputAgentSettingsEvent(settings={})
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_agent_crew_app_exposes_doctor():
    from smallestai.cli.agent_crew import initialise_agent_crew_app
    from smallestai.cli.lib.atoms import AtomsAPIClient
    from smallestai.cli.lib.auth import AuthClient
    from smallestai.cli.lib.project_config import ProjectConfig

    app = initialise_agent_crew_app(ProjectConfig(), AuthClient(), AtomsAPIClient())
    names = {cmd.name or cmd.callback.__name__ for cmd in app.registered_commands}
    assert "doctor" in names


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
