from .conftest import get_client, verify_request_count


def test_waves_ops_get_waves_health() -> None:
    """Test getWavesHealth endpoint with WireMock"""
    test_id = "waves.ops.get_waves_health.0"
    client = get_client(test_id)
    client.waves.ops.get_waves_health()
    verify_request_count(test_id, "GET", "/waves/v1/health", None, 1)
