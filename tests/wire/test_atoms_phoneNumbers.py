from .conftest import get_client, verify_request_count


def test_atoms_phoneNumbers_get_acquired_phone_numbers() -> None:
    """Test getAcquiredPhoneNumbers endpoint with WireMock"""
    test_id = "atoms.phone_numbers.get_acquired_phone_numbers.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.get_acquired_phone_numbers()
    verify_request_count(test_id, "GET", "/product/phone-numbers", None, 1)


def test_atoms_phoneNumbers_import_a_sip_phone_number() -> None:
    """Test importASipPhoneNumber endpoint with WireMock"""
    test_id = "atoms.phone_numbers.import_a_sip_phone_number.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.import_a_sip_phone_number(
        phone_number="+14155551234",
        sip_termination_url="sip:trunk.your-provider.com",
        name="Main Support Line",
        sip_username="",
        sip_password="",
    )
    verify_request_count(test_id, "POST", "/product/import-phone-number", None, 1)
