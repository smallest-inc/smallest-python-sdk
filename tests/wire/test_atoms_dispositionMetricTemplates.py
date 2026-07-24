from .conftest import get_client, verify_request_count


def test_atoms_dispositionMetricTemplates_list_disposition_metric_templates() -> None:
    """Test listDispositionMetricTemplates endpoint with WireMock"""
    test_id = "atoms.disposition_metric_templates.list_disposition_metric_templates.0"
    client = get_client(test_id)
    client.atoms.disposition_metric_templates.list_disposition_metric_templates()
    verify_request_count(test_id, "GET", "/disposition-metric-templates", None, 1)
