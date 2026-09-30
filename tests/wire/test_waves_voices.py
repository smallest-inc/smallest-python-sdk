from .conftest import get_client, verify_request_count


def test_waves_voices_get_all_voice_models() -> None:
    """Test getAllVoiceModels endpoint with WireMock"""
    test_id = "waves.voices.get_all_voice_models.0"
    client = get_client(test_id)
    client.waves.voices.get_all_voice_models()
    verify_request_count(test_id, "GET", "/waves/v1/voice/get-all-models", None, 1)
