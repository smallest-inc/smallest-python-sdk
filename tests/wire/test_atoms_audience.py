from .conftest import get_client, verify_request_count


def test_atoms_audience_get_all_audiences() -> None:
    """Test getAllAudiences endpoint with WireMock"""
    test_id = "atoms.audience.get_all_audiences.0"
    client = get_client(test_id)
    client.atoms.audience.get_all_audiences()
    verify_request_count(test_id, "GET", "/audience", None, 1)


def test_atoms_audience_create_audience_with_csv_upload() -> None:
    """Test createAudienceWithCsvUpload endpoint with WireMock"""
    test_id = "atoms.audience.create_audience_with_csv_upload.0"
    client = get_client(test_id)
    client.atoms.audience.create_audience_with_csv_upload(
        file="example_file",
        name="name",
        phone_number_column_name="phoneNumberColumnName",
    )
    verify_request_count(test_id, "POST", "/audience", None, 1)


def test_atoms_audience_get_audience_by_id() -> None:
    """Test getAudienceById endpoint with WireMock"""
    test_id = "atoms.audience.get_audience_by_id.0"
    client = get_client(test_id)
    client.atoms.audience.get_audience_by_id(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "GET", "/audience/60d0fe4f5311236168a109ca", None, 1)


def test_atoms_audience_delete_audience() -> None:
    """Test deleteAudience endpoint with WireMock"""
    test_id = "atoms.audience.delete_audience.0"
    client = get_client(test_id)
    client.atoms.audience.delete_audience(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "DELETE", "/audience/60d0fe4f5311236168a109ca", None, 1)


def test_atoms_audience_get_audience_members() -> None:
    """Test getAudienceMembers endpoint with WireMock"""
    test_id = "atoms.audience.get_audience_members.0"
    client = get_client(test_id)
    client.atoms.audience.get_audience_members(
        id="60d0fe4f5311236168a109ca",
        page=1,
        offset=10,
    )
    verify_request_count(test_id, "GET", "/audience/60d0fe4f5311236168a109ca/members", {"page": "1", "offset": "10"}, 1)


def test_atoms_audience_add_audience_members() -> None:
    """Test addAudienceMembers endpoint with WireMock"""
    test_id = "atoms.audience.add_audience_members.0"
    client = get_client(test_id)
    client.atoms.audience.add_audience_members(
        id="60d0fe4f5311236168a109ca",
        members=[{"phoneNumber": "+1234567890", "name": "John Doe", "email": "john@example.com"}],
    )
    verify_request_count(test_id, "POST", "/audience/60d0fe4f5311236168a109ca/members", None, 1)


def test_atoms_audience_delete_audience_members() -> None:
    """Test deleteAudienceMembers endpoint with WireMock"""
    test_id = "atoms.audience.delete_audience_members.0"
    client = get_client(test_id)
    client.atoms.audience.delete_audience_members(
        id="60d0fe4f5311236168a109ca",
        member_ids=["60d0fe4f5311236168a109cd"],
    )
    verify_request_count(test_id, "DELETE", "/audience/60d0fe4f5311236168a109ca/members", None, 1)


def test_atoms_audience_search_audience_members() -> None:
    """Test searchAudienceMembers endpoint with WireMock"""
    test_id = "atoms.audience.search_audience_members.0"
    client = get_client(test_id)
    client.atoms.audience.search_audience_members(
        id="60d0fe4f5311236168a109ca",
        query="john",
    )
    verify_request_count(test_id, "GET", "/audience/60d0fe4f5311236168a109ca/members/search", {"query": "john"}, 1)
