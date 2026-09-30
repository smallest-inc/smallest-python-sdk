from .conftest import get_client, verify_request_count


def test_atoms_sipTrunks_list_inbound() -> None:
    """Test list_inbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.list_inbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.list_inbound()
    verify_request_count(test_id, "GET", "/sip-trunk/inbound", None, 1)


def test_atoms_sipTrunks_create_inbound() -> None:
    """Test create_inbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.create_inbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.create_inbound(
        name="Acme carrier (inbound)",
    )
    verify_request_count(test_id, "POST", "/sip-trunk/inbound", None, 1)


def test_atoms_sipTrunks_delete_inbound() -> None:
    """Test delete_inbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.delete_inbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.delete_inbound(
        trunk_id="trunkId",
    )
    verify_request_count(test_id, "DELETE", "/sip-trunk/inbound/trunkId", None, 1)


def test_atoms_sipTrunks_update_inbound() -> None:
    """Test update_inbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.update_inbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.update_inbound(
        trunk_id="trunkId",
    )
    verify_request_count(test_id, "PATCH", "/sip-trunk/inbound/trunkId", None, 1)


def test_atoms_sipTrunks_list_outbound() -> None:
    """Test list_outbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.list_outbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.list_outbound()
    verify_request_count(test_id, "GET", "/sip-trunk/outbound", None, 1)


def test_atoms_sipTrunks_create_outbound() -> None:
    """Test create_outbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.create_outbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.create_outbound(
        name="Acme carrier (outbound)",
        address="sip.acme.com:5060",
        numbers=["+14155552671"],
    )
    verify_request_count(test_id, "POST", "/sip-trunk/outbound", None, 1)


def test_atoms_sipTrunks_delete_outbound() -> None:
    """Test delete_outbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.delete_outbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.delete_outbound(
        trunk_id="trunkId",
    )
    verify_request_count(test_id, "DELETE", "/sip-trunk/outbound/trunkId", None, 1)


def test_atoms_sipTrunks_update_outbound() -> None:
    """Test update_outbound endpoint with WireMock"""
    test_id = "atoms.sip_trunks.update_outbound.0"
    client = get_client(test_id)
    client.atoms.sip_trunks.update_outbound(
        trunk_id="trunkId",
    )
    verify_request_count(test_id, "PATCH", "/sip-trunk/outbound/trunkId", None, 1)
