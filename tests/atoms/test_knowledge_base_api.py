from smallestai.atoms.models.knowledgebase_post_request import KnowledgebasePostRequest
from smallestai.atoms.models.knowledgebase_post201_response import KnowledgebasePost201Response
from smallestai.atoms.models.knowledgebase_id_get200_response import KnowledgebaseIdGet200Response
from smallestai.atoms.models.agent_id_delete200_response import AgentIdDelete200Response
from smallestai.atoms.models.api_response import ApiResponse
from smallestai.atoms.models.knowledgebase_id_items_upload_text_post_request import KnowledgebaseIdItemsUploadTextPostRequest

def test_create_knowledge_base(atoms_client):
    request = KnowledgebasePostRequest(
        name="Test Knowledge Base",
        description="Test knowledge base description"
    )
    response = atoms_client.create_knowledge_base(knowledgebase_post_request=request)
    assert isinstance(response, KnowledgebasePost201Response)

def test_get_knowledge_base_by_id(atoms_client, global_state):
    response = atoms_client.get_knowledge_base_by_id(id=global_state["base_knowledge_base"]["id"])
    assert isinstance(response, KnowledgebaseIdGet200Response)

def test_get_knowledge_bases(atoms_client):
    response = atoms_client.get_knowledge_bases()
    assert isinstance(response, ApiResponse)

def test_delete_knowledge_base(atoms_client, global_state):
    response = atoms_client.delete_knowledge_base(id=global_state["temp_knowledge_base"]["id"])
    assert isinstance(response, AgentIdDelete200Response)

def test_get_knowledge_base_items(atoms_client, global_state):
    response = atoms_client.get_knowledge_base_items(
        id=global_state["base_knowledge_base"]["id"]
    )
    assert isinstance(response, ApiResponse)

def test_upload_text_to_knowledge_base(atoms_client, global_state):
    request = KnowledgebaseIdItemsUploadTextPostRequest(
        title="Test Upload Item",
        content="This is a test text to upload to the knowledge base"
    )
    response = atoms_client.upload_text_to_knowledge_base(
        id=global_state["base_knowledge_base"]["id"],
        knowledgebase_id_items_upload_text_post_request=request
    )
    assert isinstance(response, AgentIdDelete200Response)

def test_upload_media_to_knowledge_base(atoms_client, global_state):
    test_content = b"Test media content"
    
    response = atoms_client.upload_media_to_knowledge_base(
        id=global_state["base_knowledge_base"]["id"],
        media=test_content
    )
    assert isinstance(response, AgentIdDelete200Response)

def test_delete_knowledge_base_item(atoms_client, global_state):
   
    response = atoms_client.delete_knowledge_base_item(
        knowledge_base_id=global_state["base_knowledge_base"]["id"],
        knowledge_base_item_id=global_state["temp_knowledge_base_item_id"]
    )
    assert isinstance(response, AgentIdDelete200Response)