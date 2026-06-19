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


def test_atoms_knowledgeBase_update_a_knowledge_base_name_description() -> None:
    """Test updateAKnowledgeBaseNameDescription endpoint with WireMock"""
    test_id = "atoms.knowledge_base.update_a_knowledge_base_name_description.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.update_a_knowledge_base_name_description(
        id="id",
        name="Q4 Pricing Updates",
    )
    verify_request_count(test_id, "POST", "/knowledgebase/id", None, 1)


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


def test_atoms_knowledgeBase_get_a_presigned_s3url_for_direct_file_upload() -> None:
    """Test getAPresignedS3UrlForDirectFileUpload endpoint with WireMock"""
    test_id = "atoms.knowledge_base.get_a_presigned_s3url_for_direct_file_upload.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.get_a_presigned_s3url_for_direct_file_upload(
        file_name="company-handbook.pdf",
        file_size=2457600,
        content_type="application/pdf",
        knowledge_base_id="6867ca76d0f8f2e0f4201281",
    )
    verify_request_count(test_id, "POST", "/knowledgebase/get-presigned-url", None, 1)


def test_atoms_knowledgeBase_complete_a_presigned_url_upload_and_start_processing() -> None:
    """Test completeAPresignedUrlUploadAndStartProcessing endpoint with WireMock"""
    test_id = "atoms.knowledge_base.complete_a_presigned_url_upload_and_start_processing.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.complete_a_presigned_url_upload_and_start_processing(
        file_name="company-handbook.pdf",
        content_type="application/pdf",
        knowledge_base_id="6867ca76d0f8f2e0f4201281",
        key="key",
        file_size=1,
    )
    verify_request_count(test_id, "POST", "/knowledgebase/compelete-file-upload", None, 1)


def test_atoms_knowledgeBase_extract_ur_ls_from_a_sitemap_xml() -> None:
    """Test extractUrLsFromASitemapXml endpoint with WireMock"""
    test_id = "atoms.knowledge_base.extract_ur_ls_from_a_sitemap_xml.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.extract_ur_ls_from_a_sitemap_xml(
        site_url="https://example.com/sitemap.xml",
        knowledge_base_id="6867ca76d0f8f2e0f4201281",
    )
    verify_request_count(test_id, "POST", "/knowledgebase/get-sitemap-urls", None, 1)


def test_atoms_knowledgeBase_scrape_a_list_of_ur_ls_into_a_knowledge_base() -> None:
    """Test scrapeAListOfUrLsIntoAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.scrape_a_list_of_ur_ls_into_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.scrape_a_list_of_ur_ls_into_a_knowledge_base(
        id="id",
        urls=["https://example.com/pricing", "https://example.com/faq"],
    )
    verify_request_count(test_id, "POST", "/knowledgebase/id/scrape-urls", None, 1)


def test_atoms_knowledgeBase_list_scraped_ur_ls_in_a_knowledge_base_their_status() -> None:
    """Test listScrapedUrLsInAKnowledgeBaseTheirStatus endpoint with WireMock"""
    test_id = "atoms.knowledge_base.list_scraped_ur_ls_in_a_knowledge_base_their_status.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.list_scraped_ur_ls_in_a_knowledge_base_their_status(
        id="id",
    )
    verify_request_count(test_id, "GET", "/knowledgebase/id/scraped-urls", None, 1)


def test_atoms_knowledgeBase_delete_a_scraped_url_from_a_knowledge_base() -> None:
    """Test deleteAScrapedUrlFromAKnowledgeBase endpoint with WireMock"""
    test_id = "atoms.knowledge_base.delete_a_scraped_url_from_a_knowledge_base.0"
    client = get_client(test_id)
    client.atoms.knowledge_base.delete_a_scraped_url_from_a_knowledge_base(
        knowledge_base_id="knowledgeBaseId",
        knowledge_base_scraped_urls_id="knowledgeBaseScrapedUrlsId",
    )
    verify_request_count(
        test_id, "DELETE", "/knowledgebase/knowledgeBaseId/scraped-urls/knowledgeBaseScrapedUrlsId", None, 1
    )
