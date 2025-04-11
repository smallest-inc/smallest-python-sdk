from smallestai.atoms.models.create_knowledge_base_request import CreateKnowledgeBaseRequest
from smallestai.atoms.models.create_knowledge_base201_response import CreateKnowledgeBase201Response
from smallestai.atoms.models.get_knowledge_base_by_id200_response import GetKnowledgeBaseById200Response
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
from smallestai.atoms.models.api_response import ApiResponse
from smallestai.atoms.models.upload_text_to_knowledge_base_request import UploadTextToKnowledgeBaseRequest
from smallestai.atoms.models.get_knowledge_base_items200_response import GetKnowledgeBaseItems200Response
from smallestai.atoms.models.get_knowledge_bases200_response import GetKnowledgeBases200Response
from smallestai.atoms.models.knowledge_base_dto import KnowledgeBaseDTO
from smallestai.atoms.models.knowledge_base_item_dto import KnowledgeBaseItemDTO

def test_create_knowledge_base(atoms_client):
    request = CreateKnowledgeBaseRequest(
        name="Test Knowledge Base",
        description="Test knowledge base description"
    )
    response = atoms_client.create_knowledge_base(create_knowledge_base_request=request)
    assert isinstance(response, str)  # The response is the ID of the created knowledge base

def test_get_knowledge_base_by_id(atoms_client, global_state):
    response = atoms_client.get_knowledge_base_by_id(id=global_state["base_knowledge_base"]["id"])
    assert isinstance(response, KnowledgeBaseDTO)

def test_get_knowledge_bases(atoms_client):
    response = atoms_client.get_knowledge_bases()
    assert isinstance(response, list)
    for item in response:
        assert isinstance(item, KnowledgeBaseDTO)

def test_delete_knowledge_base(atoms_client, global_state):
    response = atoms_client.delete_knowledge_base(id=global_state["temp_knowledge_base"]["id"])
    assert response is True  # Delete response is just a boolean status

def test_get_knowledge_base_items(atoms_client, global_state):
    response = atoms_client.get_knowledge_base_items(
        id=global_state["base_knowledge_base"]["id"]
    )
    assert isinstance(response, list)
    for item in response:
        assert isinstance(item, KnowledgeBaseItemDTO)

def test_upload_text_to_knowledge_base(atoms_client, global_state):
    request = UploadTextToKnowledgeBaseRequest(
        title="Test Upload Item",
        content="This is a test text to upload to the knowledge base"
    )
    response = atoms_client.upload_text_to_knowledge_base(
        id=global_state["base_knowledge_base"]["id"],
        upload_text_to_knowledge_base_request=request
    )
    assert response is True  # Upload response is just a boolean status

def test_upload_media_to_knowledge_base(atoms_client, global_state):
    test_content = b"Test media content"
    
    response = atoms_client.upload_media_to_knowledge_base(
        id=global_state["base_knowledge_base"]["id"],
        media=test_content
    )
    assert response is True  # Upload response is just a boolean status

def test_delete_knowledge_base_item(atoms_client, global_state):
    response = atoms_client.delete_knowledge_base_item(
        knowledge_base_id=global_state["base_knowledge_base"]["id"],
        knowledge_base_item_id=global_state["temp_knowledge_base_item_id"]
    )
    assert response is True  # Delete response is just a boolean status 