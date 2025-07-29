from smallestai.atoms.models.conversation_id_get200_response import ConversationIdGet200Response

def test_get_conversation_logs(atoms_client, global_state):
    
    call_id = global_state["base_call"]["id"]
    
    response = atoms_client.get_conversation_logs(id=call_id)
    print(response)
    
    assert isinstance(response, ConversationIdGet200Response) 