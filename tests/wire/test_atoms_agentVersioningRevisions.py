from .conftest import get_client, verify_request_count


def test_atoms_agentVersioningRevisions_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.agent_versioning_revisions.list_.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_revisions.list(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches/branchId/revisions", None, 1)


def test_atoms_agentVersioningRevisions_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "atoms.agent_versioning_revisions.get.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_revisions.get(
        id="id",
        branch_id="branchId",
        revision_id="revisionId",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches/branchId/revisions/revisionId", None, 1)


def test_atoms_agentVersioningRevisions_get_history() -> None:
    """Test get_history endpoint with WireMock"""
    test_id = "atoms.agent_versioning_revisions.get_history.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_revisions.get_history(
        id="id",
        branch_id="branchId",
        revision_id="revisionId",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches/branchId/revisions/revisionId/history", None, 1)


def test_atoms_agentVersioningRevisions_restore() -> None:
    """Test restore endpoint with WireMock"""
    test_id = "atoms.agent_versioning_revisions.restore.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_revisions.restore(
        id="id",
        branch_id="branchId",
        revision_id="revisionId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/revisions/revisionId/restore", None, 1)


def test_atoms_agentVersioningRevisions_diff() -> None:
    """Test diff endpoint with WireMock"""
    test_id = "atoms.agent_versioning_revisions.diff.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_revisions.diff(
        id="id",
        a="a",
        b="b",
    )
    verify_request_count(test_id, "GET", "/agent/id/diff", {"a": "a", "b": "b"}, 1)
