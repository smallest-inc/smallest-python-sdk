import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.conversation_outbound_post_request import ConversationOutboundPostRequest
from smallestai.atoms.models.conversation_outbound_post200_response import ConversationOutboundPost200Response

def test_start_outbound_call(atoms_client, global_state):
    request = ConversationOutboundPostRequest(
        agentId=global_state["base_agent"]["id"],
        phoneNumber="+919789384444"
    )
    response = atoms_client.start_outbound_call(conversation_outbound_post_request=request)
    assert isinstance(response, ConversationOutboundPost200Response) 