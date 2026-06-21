from .conftest import get_client, verify_request_count


def test_atoms_agentVersioningDrafts_list_active_drafts() -> None:
    """Test listActiveDrafts endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.list_active_drafts.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.list_active_drafts(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/drafts", None, 1)


def test_atoms_agentVersioningDrafts_create_draft() -> None:
    """Test create_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.create_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.create_draft(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/agent/60d0fe4f5311236168a109ca/drafts", None, 1)


def test_atoms_agentVersioningDrafts_get_draft_detail() -> None:
    """Test getDraftDetail endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.get_draft_detail.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.get_draft_detail(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/drafts/draftId", None, 1)


def test_atoms_agentVersioningDrafts_discard_draft() -> None:
    """Test discard_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.discard_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.discard_draft(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "DELETE", "/agent/60d0fe4f5311236168a109ca/drafts/draftId", None, 1)


def test_atoms_agentVersioningDrafts_rename_draft() -> None:
    """Test rename_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.rename_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.rename_draft(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
        draft_name="draftName",
    )
    verify_request_count(test_id, "PATCH", "/agent/60d0fe4f5311236168a109ca/drafts/draftId", None, 1)


def test_atoms_agentVersioningDrafts_get_draft_diff() -> None:
    """Test getDraftDiff endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.get_draft_diff.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.get_draft_diff(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/drafts/draftId/diff", None, 1)


def test_atoms_agentVersioningDrafts_publish_draft() -> None:
    """Test publish_draft endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.publish_draft.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.publish_draft(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "POST", "/agent/60d0fe4f5311236168a109ca/drafts/draftId/publish", None, 1)


def test_atoms_agentVersioningDrafts_test_call_with_draft_config() -> None:
    """Test testCallWithDraftConfig endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.test_call_with_draft_config.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.test_call_with_draft_config(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "POST", "/agent/60d0fe4f5311236168a109ca/drafts/draftId/test-call", None, 1)


def test_atoms_agentVersioningDrafts_update_draft_config() -> None:
    """Test update_draft_config endpoint with WireMock"""
    test_id = "atoms.agent_versioning_drafts.update_draft_config.0"
    client = get_client(test_id)
    client.atoms.agent_versioning_drafts.update_draft_config(
        id="60d0fe4f5311236168a109ca",
        draft_id="draftId",
    )
    verify_request_count(test_id, "PATCH", "/agent/60d0fe4f5311236168a109ca/drafts/draftId/config", None, 1)
