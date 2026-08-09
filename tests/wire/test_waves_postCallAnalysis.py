from .conftest import get_client, verify_request_count

from smallestai.waves import DispositionMetric


def test_waves_postCallAnalysis_analyze() -> None:
    """Test analyze endpoint with WireMock"""
    test_id = "waves.post_call_analysis.analyze.0"
    client = get_client(test_id)
    client.waves.post_call_analysis.analyze(
        transcript="User: I want a refund for my torn jacket. Agent: I have logged your complaint and issued a full refund of $80.",
        disposition_metrics=[
            DispositionMetric(
                identifier="refund_issued",
                disposition_metric_prompt="Was a refund issued to the customer?",
                disposition_metric_type="BOOLEAN",
            )
        ],
    )
    verify_request_count(test_id, "POST", "/waves/v1/pca", None, 1)


def test_waves_postCallAnalysis_generate() -> None:
    """Test generate endpoint with WireMock"""
    test_id = "waves.post_call_analysis.generate.0"
    client = get_client(test_id)
    client.waves.post_call_analysis.generate(
        prompt="Say hello in exactly three words.",
    )
    verify_request_count(test_id, "POST", "/waves/v1/pca/generate", None, 1)
