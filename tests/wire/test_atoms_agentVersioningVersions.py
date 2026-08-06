from .conftest import get_client, verify_request_count


def test_atoms_agentVersioningVersions_list_published_versions() -> None:
    """Test listPublishedVersions endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.list_published_versions.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.list_published_versions(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/versions", None, 1)


def test_atoms_agentVersioningVersions_diff_two_versions() -> None:
    """Test diffTwoVersions endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.diff_two_versions.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.diff_two_versions(
        id="id",
        version_a="versionA",
        version_b="versionB",
    )
    verify_request_count(test_id, "GET", "/agent/id/versions/diff", {"versionA": "versionA", "versionB": "versionB"}, 1)


def test_atoms_agentVersioningVersions_get_version_detail() -> None:
    """Test getVersionDetail endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.get_version_detail.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.get_version_detail(
        id="id",
        version_id="versionId",
    )
    verify_request_count(test_id, "GET", "/agent/id/versions/versionId", None, 1)


def test_atoms_agentVersioningVersions_update_version_metadata() -> None:
    """Test update_version_metadata endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.update_version_metadata.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.update_version_metadata(
        id="id",
        version_id="versionId",
    )
    verify_request_count(test_id, "PATCH", "/agent/id/versions/versionId", None, 1)


def test_atoms_agentVersioningVersions_activate_version() -> None:
    """Test activate_version endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.activate_version.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.activate_version(
        id="id",
        version_id="versionId",
    )
    verify_request_count(test_id, "PATCH", "/agent/id/versions/versionId/activate", None, 1)


def test_atoms_agentVersioningVersions_test_call_with_version_config() -> None:
    """Test testCallWithVersionConfig endpoint with WireMock"""
    test_id = "atoms.agent_versioning_versions.test_call_with_version_config.0"
    client = get_client(test_id)
    client.agents.agent_versioning_versions.test_call_with_version_config(
        id="id",
        version_id="versionId",
    )
    verify_request_count(test_id, "POST", "/agent/id/versions/versionId/test-call", None, 1)
