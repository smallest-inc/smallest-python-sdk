from .conftest import get_client, verify_request_count


def test_atoms_compliance_get_compliance_status() -> None:
    """Test getComplianceStatus endpoint with WireMock"""
    test_id = "atoms.compliance.get_compliance_status.0"
    client = get_client(test_id)
    client.atoms.compliance.get_compliance_status(
        country_iso="IN",
        number_type="local",
        user_type="individual",
    )
    verify_request_count(
        test_id, "GET", "/compliance/status", {"countryIso": "IN", "numberType": "local", "userType": "individual"}, 1
    )


def test_atoms_compliance_get_compliance_requirements() -> None:
    """Test getComplianceRequirements endpoint with WireMock"""
    test_id = "atoms.compliance.get_compliance_requirements.0"
    client = get_client(test_id)
    client.atoms.compliance.get_compliance_requirements(
        country_iso="IN",
        number_type="local",
        user_type="individual",
    )
    verify_request_count(
        test_id,
        "GET",
        "/compliance/requirements",
        {"countryIso": "IN", "numberType": "local", "userType": "individual"},
        1,
    )


def test_atoms_compliance_submit_a_compliance_application() -> None:
    """Test submitAComplianceApplication endpoint with WireMock"""
    test_id = "atoms.compliance.submit_a_compliance_application.0"
    client = get_client(test_id)
    client.atoms.compliance.submit_a_compliance_application(
        files=["example_files"],
        country_iso="countryIso",
        number_type="local",
        user_type="individual",
        end_user="endUser",
        documents="documents",
    )
    verify_request_count(test_id, "POST", "/compliance/applications", None, 1)


def test_atoms_compliance_resubmit_a_rejected_compliance_application() -> None:
    """Test resubmitARejectedComplianceApplication endpoint with WireMock"""
    test_id = "atoms.compliance.resubmit_a_rejected_compliance_application.0"
    client = get_client(test_id)
    client.atoms.compliance.resubmit_a_rejected_compliance_application(
        id="id",
        files=["example_files"],
        documents="documents",
    )
    verify_request_count(test_id, "PATCH", "/compliance/applications/id", None, 1)


def test_atoms_compliance_refresh_compliance_application_status() -> None:
    """Test refreshComplianceApplicationStatus endpoint with WireMock"""
    test_id = "atoms.compliance.refresh_compliance_application_status.0"
    client = get_client(test_id)
    client.atoms.compliance.refresh_compliance_application_status(
        id="id",
    )
    verify_request_count(test_id, "POST", "/compliance/applications/id/refresh", None, 1)
