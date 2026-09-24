from .conftest import get_client, verify_request_count

from smallestai.atoms.concurrency import UpdateConcurrencyReservationsRequestReservationsItem


def test_atoms_concurrency_get_concurrency() -> None:
    """Test getConcurrency endpoint with WireMock"""
    test_id = "atoms.concurrency.get_concurrency.0"
    client = get_client(test_id)
    client.atoms.concurrency.get_concurrency()
    verify_request_count(test_id, "GET", "/concurrency", None, 1)


def test_atoms_concurrency_update_concurrency_reservations() -> None:
    """Test updateConcurrencyReservations endpoint with WireMock"""
    test_id = "atoms.concurrency.update_concurrency_reservations.0"
    client = get_client(test_id)
    client.atoms.concurrency.update_concurrency_reservations(
        reservations=[
            UpdateConcurrencyReservationsRequestReservationsItem(
                agent_id="agentId",
                webcall=1,
                outbound=1,
                inbound=1,
                chat=1,
            )
        ],
    )
    verify_request_count(test_id, "PUT", "/concurrency/reservations", None, 1)


def test_atoms_concurrency_get_cps_limits() -> None:
    """Test getCpsLimits endpoint with WireMock"""
    test_id = "atoms.concurrency.get_cps_limits.0"
    client = get_client(test_id)
    client.atoms.concurrency.get_cps_limits()
    verify_request_count(test_id, "GET", "/product/cps-limits", None, 1)


def test_atoms_concurrency_update_custom_trunk_cps_limit() -> None:
    """Test updateCustomTrunkCpsLimit endpoint with WireMock"""
    test_id = "atoms.concurrency.update_custom_trunk_cps_limit.0"
    client = get_client(test_id)
    client.atoms.concurrency.update_custom_trunk_cps_limit(
        termination_url="43.205.53.11:5091",
        cps_limit=2,
    )
    verify_request_count(test_id, "PATCH", "/product/custom-trunk/cps-limit", None, 1)
