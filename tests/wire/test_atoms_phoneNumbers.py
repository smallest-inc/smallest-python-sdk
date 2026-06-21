from .conftest import get_client, verify_request_count


def test_atoms_phoneNumbers_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.phone_numbers.list_.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.list()
    verify_request_count(test_id, "GET", "/product/phone-numbers", None, 1)


def test_atoms_phoneNumbers_list_all_phone_numbers_platform_sip() -> None:
    """Test listAllPhoneNumbersPlatformSip endpoint with WireMock"""
    test_id = "atoms.phone_numbers.list_all_phone_numbers_platform_sip.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.list_all_phone_numbers_platform_sip()
    verify_request_count(test_id, "GET", "/product/all-numbers", None, 1)


def test_atoms_phoneNumbers_search_rentable() -> None:
    """Test search_rentable endpoint with WireMock"""
    test_id = "atoms.phone_numbers.search_rentable.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.search_rentable(
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


def test_atoms_phoneNumbers_rent() -> None:
    """Test rent endpoint with WireMock"""
    test_id = "atoms.phone_numbers.rent.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.rent(
        phone_number="13183747513",
        provider="plivo",
    )
    verify_request_count(test_id, "POST", "/product/rent-number", None, 1)


def test_atoms_phoneNumbers_release() -> None:
    """Test release endpoint with WireMock"""
    test_id = "atoms.phone_numbers.release.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.release(
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


def test_atoms_phoneNumbers_import_sip() -> None:
    """Test import_sip endpoint with WireMock"""
    test_id = "atoms.phone_numbers.import_sip.0"
    client = get_client(test_id)
    client.atoms.phone_numbers.import_sip(
        phone_number="+14155551234",
        sip_termination_url="sip:trunk.your-provider.com",
        name="Main Support Line",
        sip_username="",
        sip_password="",
    )
    verify_request_count(test_id, "POST", "/product/import-phone-number", None, 1)
