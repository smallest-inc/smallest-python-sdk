from .conftest import get_client, verify_request_count


def test_atoms_widget_get_agent_widget_config() -> None:
    """Test getAgentWidgetConfig endpoint with WireMock"""
    test_id = "atoms.widget.get_agent_widget_config.0"
    client = get_client(test_id)
    client.atoms.widget.get_agent_widget_config(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/widget-config", None, 1)


def test_atoms_widget_update_agent_widget_config() -> None:
    """Test updateAgentWidgetConfig endpoint with WireMock"""
    test_id = "atoms.widget.update_agent_widget_config.0"
    client = get_client(test_id)
    client.atoms.widget.update_agent_widget_config(
        id="id",
    )
    verify_request_count(test_id, "PATCH", "/agent/id/widget-config", None, 1)


def test_atoms_widget_get_agent_avatar_presigned_url() -> None:
    """Test getAgentAvatarPresignedUrl endpoint with WireMock"""
    test_id = "atoms.widget.get_agent_avatar_presigned_url.0"
    client = get_client(test_id)
    client.atoms.widget.get_agent_avatar_presigned_url(
        id="id",
        file_name="fileName",
        content_type="contentType",
        file_size=1.1,
    )
    verify_request_count(test_id, "POST", "/agent/id/avatar/presigned-url", None, 1)
