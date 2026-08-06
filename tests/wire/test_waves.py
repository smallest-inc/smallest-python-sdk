from .conftest import get_client, verify_request_count

from smallestai.speech import PronunciationItem


def test_waves_get_pronunciation_dicts() -> None:
    """Test get_pronunciation_dicts endpoint with WireMock"""
    test_id = "waves.get_pronunciation_dicts.0"
    client = get_client(test_id)
    client.speech.get_pronunciation_dicts()
    verify_request_count(test_id, "GET", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_create_pronunciation_dict() -> None:
    """Test create_pronunciation_dict endpoint with WireMock"""
    test_id = "waves.create_pronunciation_dict.0"
    client = get_client(test_id)
    client.speech.create_pronunciation_dict(
        items=[
            PronunciationItem(
                word="mysql",
                pronunciation="my-sequel",
            )
        ],
    )
    verify_request_count(test_id, "POST", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_update_pronunciation_dict() -> None:
    """Test update_pronunciation_dict endpoint with WireMock"""
    test_id = "waves.update_pronunciation_dict.0"
    client = get_client(test_id)
    client.speech.update_pronunciation_dict(
        id="64f1234567890abcdef12345",
        items=[
            PronunciationItem(
                word="mysql",
                pronunciation="my-sequel",
            )
        ],
    )
    verify_request_count(test_id, "PUT", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_delete_pronunciation_dict() -> None:
    """Test delete_pronunciation_dict endpoint with WireMock"""
    test_id = "waves.delete_pronunciation_dict.0"
    client = get_client(test_id)
    client.speech.delete_pronunciation_dict(
        id="64f1234567890abcdef12345",
    )
    verify_request_count(test_id, "DELETE", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_synthesize_lightning() -> None:
    """Test synthesize_lightning endpoint with WireMock"""
    test_id = "waves.synthesize_lightning.0"
    client = get_client(test_id)
    client.speech.synthesize_lightning()
    verify_request_count(test_id, "POST", "/waves/v1/lightning/get_speech", None, 1)


def test_waves_synthesize_lightning_large() -> None:
    """Test synthesize_lightning_large endpoint with WireMock"""
    test_id = "waves.synthesize_lightning_large.0"
    client = get_client(test_id)
    client.speech.synthesize_lightning_large()
    verify_request_count(test_id, "POST", "/waves/v1/lightning-large/get_speech", None, 1)


def test_waves_synthesize_sse_lightning_large() -> None:
    """Test synthesize_sse_lightning_large endpoint with WireMock"""
    test_id = "waves.synthesize_sse_lightning_large.0"
    client = get_client(test_id)
    client.speech.synthesize_sse_lightning_large()
    verify_request_count(test_id, "POST", "/waves/v1/lightning-large/stream", None, 1)


def test_waves_synthesize_lightning_v2() -> None:
    """Test synthesize_lightning_v2 endpoint with WireMock"""
    test_id = "waves.synthesize_lightning_v2.0"
    client = get_client(test_id)
    client.speech.synthesize_lightning_v2()
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v2/get_speech", None, 1)


def test_waves_synthesize_sse_lightning_v2() -> None:
    """Test synthesize_sse_lightning_v2 endpoint with WireMock"""
    test_id = "waves.synthesize_sse_lightning_v2.0"
    client = get_client(test_id)
    client.speech.synthesize_sse_lightning_v2()
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v2/stream", None, 1)


def test_waves_get_voices() -> None:
    """Test get_voices endpoint with WireMock"""
    test_id = "waves.get_voices.0"
    client = get_client(test_id)
    client.speech.get_voices(
        model="lightning-v3.1",
    )
    verify_request_count(test_id, "GET", "/waves/v1/lightning-v3.1/get_voices", None, 1)


def test_waves_synthesize_tts() -> None:
    """Test synthesize_tts endpoint with WireMock"""
    test_id = "waves.synthesize_tts.0"
    client = get_client(test_id)
    for _ in client.speech.synthesize_tts(
        text="Hello from Waves TTS.",
        voice_id="magnus",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/tts", None, 1)


def test_waves_synthesize_sse_tts() -> None:
    """Test synthesize_sse_tts endpoint with WireMock"""
    test_id = "waves.synthesize_sse_tts.0"
    client = get_client(test_id)
    for _ in client.speech.synthesize_sse_tts(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/tts/live", None, 1)


def test_waves_list_voice_clones() -> None:
    """Test list_voice_clones endpoint with WireMock"""
    test_id = "waves.list_voice_clones.0"
    client = get_client(test_id)
    client.speech.list_voice_clones()
    verify_request_count(test_id, "GET", "/waves/v1/voice-cloning", None, 1)


def test_waves_create_voice_clone() -> None:
    """Test create_voice_clone endpoint with WireMock"""
    test_id = "waves.create_voice_clone.0"
    client = get_client(test_id)
    client.speech.create_voice_clone(
        file="example_file",
        display_name="displayName",
    )
    verify_request_count(test_id, "POST", "/waves/v1/voice-cloning", None, 1)
