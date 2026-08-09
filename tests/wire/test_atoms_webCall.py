from .conftest import get_client, verify_request_count


def test_atoms_webCall_start_web_chat_conversation() -> None:
    """Test startWebChatConversation endpoint with WireMock"""
    test_id = "atoms.web_call.start_web_chat_conversation.0"
    client = get_client(test_id)
    client.atoms.web_call.start_web_chat_conversation(
        agent_id="6a75935452c6e5eceaa16edf",
    )
    verify_request_count(test_id, "POST", "/conversation/chat", None, 1)


def test_atoms_webCall_start_web_call_conversation() -> None:
    """Test startWebCallConversation endpoint with WireMock"""
    test_id = "atoms.web_call.start_web_call_conversation.0"
    client = get_client(test_id)
    client.atoms.web_call.start_web_call_conversation(
        agent_id="6a75935452c6e5eceaa16edf",
    )
    verify_request_count(test_id, "POST", "/conversation/webcall", None, 1)
