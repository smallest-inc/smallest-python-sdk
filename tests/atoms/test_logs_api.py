import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.get_conversation_logs200_response_data import GetConversationLogs200ResponseData

def test_get_conversation_logs(atoms_client, global_state):
    
    call_id = global_state["base_call"]["id"]
    
    response = atoms_client.get_conversation_logs(id=call_id)
    print(response)
    
    assert isinstance(response, GetConversationLogs200ResponseData) 