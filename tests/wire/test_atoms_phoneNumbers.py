from .conftest import get_client, verify_request_count


def test_atoms_phoneNumbers_get_acquired_phone_numbers() -> None:
    """Test getAcquiredPhoneNumbers endpoint with WireMock"""
    test_id = "atoms.phone_numbers.get_acquired_phone_numbers.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.get_acquired_phone_numbers()
    verify_request_count(test_id, "GET", "/product/phone-numbers", None, 1)


def test_atoms_phoneNumbers_list_all_phone_numbers_platform_sip() -> None:
    """Test listAllPhoneNumbersPlatformSip endpoint with WireMock"""
    test_id = "atoms.phone_numbers.list_all_phone_numbers_platform_sip.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.list_all_phone_numbers_platform_sip()
    verify_request_count(test_id, "GET", "/product/all-numbers", None, 1)


def test_atoms_phoneNumbers_search_rentable_phone_numbers_in_inventory() -> None:
    """Test searchRentablePhoneNumbersInInventory endpoint with WireMock"""
    test_id = "atoms.phone_numbers.search_rentable_phone_numbers_in_inventory.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.search_rentable_phone_numbers_in_inventory(
        country_code="US",
        provider="plivo",
    )
    verify_request_count(
        test_id, "GET", "/product/get-available-numbers", {"countryCode": "US", "provider": "plivo"}, 1
    )


def test_atoms_phoneNumbers_preview_prorated_rental_cost_for_renting_a_phone_number_today() -> None:
    """Test previewProratedRentalCostForRentingAPhoneNumberToday endpoint with WireMock"""
    test_id = "atoms.phone_numbers.preview_prorated_rental_cost_for_renting_a_phone_number_today.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.preview_prorated_rental_cost_for_renting_a_phone_number_today()
    verify_request_count(test_id, "GET", "/product/proration-amount", None, 1)


def test_atoms_phoneNumbers_rent_a_phone_number_from_the_telephony_inventory() -> None:
    """Test rentAPhoneNumberFromTheTelephonyInventory endpoint with WireMock"""
    test_id = "atoms.phone_numbers.rent_a_phone_number_from_the_telephony_inventory.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.rent_a_phone_number_from_the_telephony_inventory(
        phone_number="13183747513",
        provider="plivo",
    )
    verify_request_count(test_id, "POST", "/product/rent-number", None, 1)


def test_atoms_phoneNumbers_release_a_rented_phone_number() -> None:
    """Test releaseARentedPhoneNumber endpoint with WireMock"""
    test_id = "atoms.phone_numbers.release_a_rented_phone_number.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.release_a_rented_phone_number(
        product_id="6969109c84c74bed175f02a7",
    )
    verify_request_count(test_id, "POST", "/product/release-number", None, 1)


def test_atoms_phoneNumbers_get_stripe_customer_portal_url() -> None:
    """Test getStripeCustomerPortalUrl endpoint with WireMock"""
    test_id = "atoms.phone_numbers.get_stripe_customer_portal_url.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.get_stripe_customer_portal_url()
    verify_request_count(test_id, "GET", "/product/manage-subscription", None, 1)


def test_atoms_phoneNumbers_check_whether_the_organization_has_unpaid_invoices() -> None:
    """Test checkWhetherTheOrganizationHasUnpaidInvoices endpoint with WireMock"""
    test_id = "atoms.phone_numbers.check_whether_the_organization_has_unpaid_invoices.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.check_whether_the_organization_has_unpaid_invoices()
    verify_request_count(test_id, "GET", "/product/unpaid-invoices", None, 1)


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
