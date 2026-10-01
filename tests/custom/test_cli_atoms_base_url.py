"""AtomsAPIClient (agent-crew deploy / builds) honours SMALLEST_BASE_URL like make_client."""

from smallestai.cli.lib.atoms import AtomsAPIClient


def test_defaults_to_public_host(monkeypatch):
    monkeypatch.delenv("SMALLEST_BASE_URL", raising=False)
    assert AtomsAPIClient().base_url == "https://api.smallest.ai"


def test_uses_region_host_from_env(monkeypatch):
    monkeypatch.setenv("SMALLEST_BASE_URL", "https://api.us.smallest.ai/")
    assert AtomsAPIClient().base_url == "https://api.us.smallest.ai"
