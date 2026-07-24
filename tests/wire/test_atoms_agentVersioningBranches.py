from .conftest import get_client, verify_request_count


def test_atoms_agentVersioningBranches_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.list_.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.list(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches", None, 1)


def test_atoms_agentVersioningBranches_create_branch() -> None:
    """Test create_branch endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.create_branch.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.create_branch(
        id="id",
        source_branch_id="sourceBranchId",
        name="name",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches", None, 1)


def test_atoms_agentVersioningBranches_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.get.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.get(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches/branchId", None, 1)


def test_atoms_agentVersioningBranches_rename() -> None:
    """Test rename endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.rename.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.rename(
        id="id",
        branch_id="branchId",
        name="name",
    )
    verify_request_count(test_id, "PATCH", "/agent/id/branches/branchId", None, 1)


def test_atoms_agentVersioningBranches_archive() -> None:
    """Test archive endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.archive.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.archive(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/archive", None, 1)


def test_atoms_agentVersioningBranches_make_live() -> None:
    """Test make_live endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.make_live.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.make_live(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/live", None, 1)


def test_atoms_agentVersioningBranches_get_draft() -> None:
    """Test get_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.get_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.get_draft(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "GET", "/agent/id/branches/branchId/draft", None, 1)


def test_atoms_agentVersioningBranches_update_draft() -> None:
    """Test update_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.update_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.update_draft(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "PUT", "/agent/id/branches/branchId/draft", None, 1)


def test_atoms_agentVersioningBranches_discard_draft() -> None:
    """Test discard_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.discard_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.discard_draft(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "DELETE", "/agent/id/branches/branchId/draft", None, 1)


def test_atoms_agentVersioningBranches_publish_draft() -> None:
    """Test publish_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.publish_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.publish_draft(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/draft/publish", None, 1)


def test_atoms_agentVersioningBranches_cancel_publish() -> None:
    """Test cancel_publish endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.cancel_publish.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.cancel_publish(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/draft/publish/cancel", None, 1)


def test_atoms_agentVersioningBranches_test_call() -> None:
    """Test test_call endpoint with WireMock"""
    test_id = "atoms.agent_versioning_branches.test_call.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_branches.test_call(
        id="id",
        branch_id="branchId",
    )
    verify_request_count(test_id, "POST", "/agent/id/branches/branchId/test-call", None, 1)
