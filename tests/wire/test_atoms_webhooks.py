from .conftest import get_client, verify_request_count

from smallestai.atoms.webhooks import PostWebhookRequestEventsItem


def test_atoms_webhooks_get_webhooks() -> None:
    """Test getWebhooks endpoint with WireMock"""
    test_id = "atoms.webhooks.get_webhooks.0"
    client = get_client(test_id)
    client.atoms.webhooks.get_webhooks()
    verify_request_count(test_id, "GET", "/webhook", None, 1)


def test_atoms_webhooks_create_a_webhook() -> None:
    """Test createAWebhook endpoint with WireMock"""
    test_id = "atoms.webhooks.create_a_webhook.0"
    client = get_client(test_id)
    client.atoms.webhooks.create_a_webhook(
        endpoint="https://example.com/webhook",
        description="Webhook for conversation events",
        events=[PostWebhookRequestEventsItem()],
    )
    verify_request_count(test_id, "POST", "/webhook", None, 1)


def test_atoms_webhooks_delete_a_webhook() -> None:
    """Test deleteAWebhook endpoint with WireMock"""
    test_id = "atoms.webhooks.delete_a_webhook.0"
    client = get_client(test_id)
    client.atoms.webhooks.delete_a_webhook(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/webhook/id", None, 1)


def test_atoms_webhooks_get_webhook_subscriptions_for_an_agent() -> None:
    """Test getWebhookSubscriptionsForAnAgent endpoint with WireMock"""
    test_id = "atoms.webhooks.get_webhook_subscriptions_for_an_agent.0"
    client = get_client(test_id)
    client.atoms.webhooks.get_webhook_subscriptions_for_an_agent(
        agent_id="agentId",
    )
    verify_request_count(test_id, "GET", "/agent/agentId/webhook-subscriptions", None, 1)


def test_atoms_webhooks_create_webhook_subscriptions_for_an_agent() -> None:
    """Test createWebhookSubscriptionsForAnAgent endpoint with WireMock"""
    test_id = "atoms.webhooks.create_webhook_subscriptions_for_an_agent.0"
    client = get_client(test_id)
    client.atoms.webhooks.create_webhook_subscriptions_for_an_agent(
        agent_id="agentId",
        event_types=["pre-conversation"],
        webhook_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/agent/agentId/webhook-subscriptions", None, 1)


def test_atoms_webhooks_delete_webhook_subscriptions_for_an_agent() -> None:
    """Test deleteWebhookSubscriptionsForAnAgent endpoint with WireMock"""
    test_id = "atoms.webhooks.delete_webhook_subscriptions_for_an_agent.0"
    client = get_client(test_id)
    client.atoms.webhooks.delete_webhook_subscriptions_for_an_agent(
        agent_id="agentId",
    )
    verify_request_count(test_id, "DELETE", "/agent/agentId/webhook-subscriptions", None, 1)
