from .conftest import get_client, verify_request_count


def test_atoms_campaigns_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.campaigns.list_.0"
    client = get_client(test_id)
    client.atoms.campaigns.list()
    verify_request_count(test_id, "GET", "/campaign", None, 1)


def test_atoms_campaigns_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "atoms.campaigns.create.0"
    client = get_client(test_id)
    client.atoms.campaigns.create(
        name="My Campaign",
        audience_id="60d0fe4f5311236168a109ca",
        agent_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/campaign", None, 1)


def test_atoms_campaigns_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "atoms.campaigns.get.0"
    client = get_client(test_id)
    client.atoms.campaigns.get(
        id="id",
    )
    verify_request_count(test_id, "GET", "/campaign/id", None, 1)


def test_atoms_campaigns_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "atoms.campaigns.delete.0"
    client = get_client(test_id)
    client.atoms.campaigns.delete(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/campaign/id", None, 1)


def test_atoms_campaigns_start_or_resume() -> None:
    """Test start_or_resume endpoint with WireMock"""
    test_id = "atoms.campaigns.start_or_resume.0"
    client = get_client(test_id)
    client.atoms.campaigns.start_or_resume(
        id="id",
    )
    verify_request_count(test_id, "POST", "/campaign/id/start", None, 1)


def test_atoms_campaigns_pause() -> None:
    """Test pause endpoint with WireMock"""
    test_id = "atoms.campaigns.pause.0"
    client = get_client(test_id)
    client.atoms.campaigns.pause(
        id="id",
    )
    verify_request_count(test_id, "POST", "/campaign/id/pause", None, 1)


def test_atoms_campaigns_export_campaign_results_by_audience_member() -> None:
    """Test exportCampaignResultsByAudienceMember endpoint with WireMock"""
    test_id = "atoms.campaigns.export_campaign_results_by_audience_member.0"
    client = get_client(test_id)
    client.atoms.campaigns.export_campaign_results_by_audience_member(
        id="6a75935452c6e5eceaa16edf",
    )
    verify_request_count(test_id, "GET", "/campaign/6a75935452c6e5eceaa16edf/export/by-audience-member", None, 1)


def test_atoms_campaigns_export_campaign_logs() -> None:
    """Test exportCampaignLogs endpoint with WireMock"""
    test_id = "atoms.campaigns.export_campaign_logs.0"
    client = get_client(test_id)
    for _ in client.atoms.campaigns.export_campaign_logs(
        id="id",
    ):
        pass
    verify_request_count(test_id, "GET", "/campaign/id/logs/export", None, 1)
