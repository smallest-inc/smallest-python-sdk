from .conftest import get_client, verify_request_count


def test_atoms_knowledgeBase_get_all_knowledge_bases() -> None:
    """Test getAllKnowledgeBases endpoint with WireMock"""
    test_id = "atoms.knowledge_base.get_all_knowledge_bases.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.get_all_knowledge_bases()
    verify_request_count(test_id, "GET", "/knowledgebase", None, 1)


def test_atoms_knowledgeBase_create_a_knowledge_base() -> None:
    """Test createAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.create_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.create_a_knowledge_base(
        name="name",
    )
    verify_request_count(test_id, "POST", "/knowledgebase", None, 1)


def test_atoms_knowledgeBase_get_a_knowledge_base() -> None:
    """Test getAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.get_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.get_a_knowledge_base(
        id="id",
    )
    verify_request_count(test_id, "GET", "/knowledgebase/id", None, 1)


def test_atoms_knowledgeBase_delete_a_knowledge_base() -> None:
    """Test deleteAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.delete_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.delete_a_knowledge_base(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/knowledgebase/id", None, 1)


def test_atoms_knowledgeBase_get_all_knowledge_base_items() -> None:
    """Test getAllKnowledgeBaseItems endpoint with WireMock"""
    test_id = "atoms.knowledge_base.get_all_knowledge_base_items.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.get_all_knowledge_base_items(
        id="id",
    )
    verify_request_count(test_id, "GET", "/knowledgebase/id/items", None, 1)


def test_atoms_knowledgeBase_delete_a_knowledge_base_item() -> None:
    """Test deleteAKnowledgeBaseItem endpoint with WireMock"""
    test_id = "atoms.knowledge_base.delete_a_knowledge_base_item.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.delete_a_knowledge_base_item(
        knowledge_base_id="knowledgeBaseId",
        knowledge_base_item_id="knowledgeBaseItemId",
    )
    verify_request_count(test_id, "DELETE", "/knowledgebase/knowledgeBaseId/items/knowledgeBaseItemId", None, 1)


def test_atoms_knowledgeBase_upload_a_pdf_file_to_a_knowledge_base() -> None:
    """Test uploadAPdfFileToAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.upload_a_pdf_file_to_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.upload_a_pdf_file_to_a_knowledge_base(
        id="id",
        media="example_media",
    )
    verify_request_count(test_id, "POST", "/knowledgebase/id/items/upload-media", None, 1)
