import datetime

from .conftest import get_client, verify_request_count


def test_atoms_billing_get_balance() -> None:
    """Test get_balance endpoint with WireMock"""
    test_id = "atoms.billing.get_balance.0"
    client = get_client(test_id)
    client.agents.billing.get_balance()
    verify_request_count(test_id, "GET", "/payment/v1/credits/balance", None, 1)


def test_atoms_billing_get_ledger() -> None:
    """Test get_ledger endpoint with WireMock"""
    test_id = "atoms.billing.get_ledger.0"
    client = get_client(test_id)
    client.agents.billing.get_ledger(
        from_=datetime.datetime.fromisoformat("2026-07-01T00:00:00+00:00"),
        to=datetime.datetime.fromisoformat("2026-07-28T00:00:00+00:00"),
    )
    verify_request_count(
        test_id, "GET", "/payment/v1/credits/ledger", {"from": "2026-07-01T00:00:00Z", "to": "2026-07-28T00:00:00Z"}, 1
    )


def test_atoms_billing_get_usage_breakdown() -> None:
    """Test get_usage_breakdown endpoint with WireMock"""
    test_id = "atoms.billing.get_usage_breakdown.0"
    client = get_client(test_id)
    client.agents.billing.get_usage_breakdown()
    verify_request_count(test_id, "GET", "/payment/v1/credits/usage/breakdown", None, 1)


def test_atoms_billing_list_invoices() -> None:
    """Test list_invoices endpoint with WireMock"""
    test_id = "atoms.billing.list_invoices.0"
    client = get_client(test_id)
    client.agents.billing.list_invoices()
    verify_request_count(test_id, "GET", "/payment/v1/invoices", None, 1)


def test_atoms_billing_get_invoice_pdf() -> None:
    """Test get_invoice_pdf endpoint with WireMock"""
    test_id = "atoms.billing.get_invoice_pdf.0"
    client = get_client(test_id)
    client.agents.billing.get_invoice_pdf(
        invoice_id="invoiceId",
    )
    verify_request_count(test_id, "GET", "/payment/v1/invoices/invoiceId/pdf", None, 1)
