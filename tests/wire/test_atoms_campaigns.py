from .conftest import get_client, verify_request_count


def test_atoms_campaigns_retrieve_all_campaigns() -> None:
    """Test retrieveAllCampaigns endpoint with WireMock"""
    test_id = "atoms.campaigns.retrieve_all_campaigns.0"
    client = get_client(test_id)
    client.atoms.campaigns.retrieve_all_campaigns()
    verify_request_count(test_id, "GET", "/campaign", None, 1)


def test_atoms_campaigns_create_a_campaign() -> None:
    """Test createACampaign endpoint with WireMock"""
    test_id = "atoms.campaigns.create_a_campaign.0"
    client = get_client(test_id)
    client.atoms.campaigns.create_a_campaign(
        name="My Campaign",
        audience_id="60d0fe4f5311236168a109ca",
        agent_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/campaign", None, 1)


def test_atoms_campaigns_get_a_campaign() -> None:
    """Test getACampaign endpoint with WireMock"""
    test_id = "atoms.campaigns.get_a_campaign.0"
    client = get_client(test_id)
    client.atoms.campaigns.get_a_campaign(
        id="id",
    )
    verify_request_count(test_id, "GET", "/campaign/id", None, 1)


def test_atoms_campaigns_delete_a_campaign() -> None:
    """Test deleteACampaign endpoint with WireMock"""
    test_id = "atoms.campaigns.delete_a_campaign.0"
    client = get_client(test_id)
    client.atoms.campaigns.delete_a_campaign(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/campaign/id", None, 1)


def test_atoms_campaigns_start_or_resume_a_campaign() -> None:
    """Test startOrResumeACampaign endpoint with WireMock"""
    test_id = "atoms.campaigns.start_or_resume_a_campaign.0"
    client = get_client(test_id)
    client.atoms.campaigns.start_or_resume_a_campaign(
        id="id",
    )
    verify_request_count(test_id, "POST", "/campaign/id/start", None, 1)


def test_atoms_campaigns_pause_a_campaign() -> None:
    """Test pauseACampaign endpoint with WireMock"""
    test_id = "atoms.campaigns.pause_a_campaign.0"
    client = get_client(test_id)
    client.atoms.campaigns.pause_a_campaign(
        id="id",
    )
    verify_request_count(test_id, "POST", "/campaign/id/pause", None, 1)
