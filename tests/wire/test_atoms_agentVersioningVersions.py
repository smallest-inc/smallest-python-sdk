import datetime

from .conftest import get_client, verify_request_count


def test_atoms_agentVersioningVersions_list_published_versions() -> None:
    """Test listPublishedVersions endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.list_published_versions.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.list_published_versions(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/versions", None, 1)


def test_atoms_agentVersioningVersions_diff_two_versions() -> None:
    """Test diffTwoVersions endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.diff_two_versions.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.diff_two_versions(
        id="60d0fe4f5311236168a109ca",
        version_a="versionA",
        version_b="versionB",
    )
    verify_request_count(
        test_id,
        "GET",
        "/agent/60d0fe4f5311236168a109ca/versions/diff",
        {"versionA": "versionA", "versionB": "versionB"},
        1,
    )


def test_atoms_agentVersioningVersions_compare_version_metrics() -> None:
    """Test compare_version_metrics endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.compare_version_metrics.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.compare_version_metrics(
        id="60d0fe4f5311236168a109ca",
        version_a="versionA",
        version_b="versionB",
        date_from=datetime.date.fromisoformat("2026-05-01"),
        date_to=datetime.date.fromisoformat("2026-05-31"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/agent/60d0fe4f5311236168a109ca/versions/compare-metrics",
        {"versionA": "versionA", "versionB": "versionB", "dateFrom": "2026-05-01", "dateTo": "2026-05-31"},
        1,
    )


def test_atoms_agentVersioningVersions_get_version_detail() -> None:
    """Test getVersionDetail endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.get_version_detail.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.get_version_detail(
        id="60d0fe4f5311236168a109ca",
        version_id="versionId",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/versions/versionId", None, 1)


def test_atoms_agentVersioningVersions_update_version_metadata() -> None:
    """Test update_version_metadata endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.update_version_metadata.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.update_version_metadata(
        id="60d0fe4f5311236168a109ca",
        version_id="versionId",
    )
    verify_request_count(test_id, "PATCH", "/agent/60d0fe4f5311236168a109ca/versions/versionId", None, 1)


def test_atoms_agentVersioningVersions_activate_version() -> None:
    """Test activate_version endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.activate_version.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.activate_version(
        id="60d0fe4f5311236168a109ca",
        version_id="versionId",
    )
    verify_request_count(test_id, "PATCH", "/agent/60d0fe4f5311236168a109ca/versions/versionId/activate", None, 1)


def test_atoms_agentVersioningVersions_test_call_with_version_config() -> None:
    """Test testCallWithVersionConfig endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.test_call_with_version_config.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_versions.test_call_with_version_config(
        id="60d0fe4f5311236168a109ca",
        version_id="versionId",
    )
    verify_request_count(test_id, "POST", "/agent/60d0fe4f5311236168a109ca/versions/versionId/test-call", None, 1)
