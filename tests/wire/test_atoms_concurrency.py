from .conftest import get_client, verify_request_count

from smallestai.agents.concurrency import UpdateConcurrencyReservationsRequestReservationsItem


def test_atoms_concurrency_get_concurrency() -> None:
    """Test getConcurrency endpoint with WireMock"""
    test_id = "atoms.concurrency.get_concurrency.0"
    client = get_client(test_id)
    client.agents.concurrency.get_concurrency()
    verify_request_count(test_id, "GET", "/concurrency", None, 1)


def test_atoms_concurrency_update_concurrency_reservations() -> None:
    """Test updateConcurrencyReservations endpoint with WireMock"""
    test_id = "atoms.concurrency.update_concurrency_reservations.0"
    client = get_client(test_id)
    client.agents.concurrency.update_concurrency_reservations(
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
