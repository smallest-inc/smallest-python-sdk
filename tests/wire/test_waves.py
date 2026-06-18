from .conftest import get_client, verify_request_count

from smallestai.waves import PronunciationItem


def test_waves_get_pronunciation_dicts() -> None:
    """Test get_pronunciation_dicts endpoint with WireMock"""
    test_id = "waves.get_pronunciation_dicts.0"
    client = get_client(test_id)
    client.waves.get_pronunciation_dicts()
    verify_request_count(test_id, "GET", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_create_pronunciation_dict() -> None:
    """Test create_pronunciation_dict endpoint with WireMock"""
    test_id = "waves.create_pronunciation_dict.0"
    client = get_client(test_id)
    client.waves.create_pronunciation_dict(
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
    client.waves.update_pronunciation_dict(
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
    client.waves.delete_pronunciation_dict(
        id="64f1234567890abcdef12345",
    )
    verify_request_count(test_id, "DELETE", "/waves/v1/pronunciation-dicts", None, 1)


def test_waves_synthesize_lightning() -> None:
    """Test synthesize_lightning endpoint with WireMock"""
    test_id = "waves.synthesize_lightning.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_lightning(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning/get_speech", None, 1)


def test_waves_synthesize_lightning_large() -> None:
    """Test synthesize_lightning_large endpoint with WireMock"""
    test_id = "waves.synthesize_lightning_large.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_lightning_large(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-large/get_speech", None, 1)


def test_waves_synthesize_lightning_v2() -> None:
    """Test synthesize_lightning_v2 endpoint with WireMock"""
    test_id = "waves.synthesize_lightning_v2.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_lightning_v2(
        text="Hey i am your a text to speech model",
        voice_id="malcom",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v2/get_speech", None, 1)


def test_waves_synthesize_sse_lightning_large() -> None:
    """Test synthesize_sse_lightning_large endpoint with WireMock"""
    test_id = "waves.synthesize_sse_lightning_large.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_sse_lightning_large(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-large/stream", None, 1)


def test_waves_synthesize_sse_lightning_v2() -> None:
    """Test synthesize_sse_lightning_v2 endpoint with WireMock"""
    test_id = "waves.synthesize_sse_lightning_v2.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_sse_lightning_v2(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v2/stream", None, 1)


def test_waves_get_voices() -> None:
    """Test get_voices endpoint with WireMock"""
    test_id = "waves.get_voices.0"
    client = get_client(test_id)
    client.waves.get_voices(
        model="lightning",
    )
    verify_request_count(test_id, "GET", "/waves/v1/lightning/get_voices", None, 1)


def test_waves_add_voice() -> None:
    """Test add_voice endpoint with WireMock"""
    test_id = "waves.add_voice.0"
    client = get_client(test_id)
    client.waves.add_voice(
        file="example_file",
        display_name="displayName",
    )
    verify_request_count(test_id, "POST", "/waves/v1/lightning-large/add_voice", None, 1)


def test_waves_get_cloned_voices() -> None:
    """Test get_cloned_voices endpoint with WireMock"""
    test_id = "waves.get_cloned_voices.0"
    client = get_client(test_id)
    client.waves.get_cloned_voices()
    verify_request_count(test_id, "GET", "/waves/v1/lightning-large/get_cloned_voices", None, 1)


def test_waves_delete_voice() -> None:
    """Test delete_voice endpoint with WireMock"""
    test_id = "waves.delete_voice.0"
    client = get_client(test_id)
    client.waves.delete_voice(
        voice_id="voiceId",
    )
    verify_request_count(test_id, "DELETE", "/waves/v1/lightning-large", None, 1)


def test_waves_synthesize_lightning_v31() -> None:
    """Test synthesize_lightning_v3_1 endpoint with WireMock"""
    test_id = "waves.synthesize_lightning_v31.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_lightning_v31(
        text="Hey i am your a text to speech model",
        voice_id="daniel",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v3.1/get_speech", None, 1)


def test_waves_synthesize_sse_lightning_v31() -> None:
    """Test synthesize_sse_lightning_v3_1 endpoint with WireMock"""
    test_id = "waves.synthesize_sse_lightning_v31.0"
    client = get_client(test_id)
    for _ in client.waves.synthesize_sse_lightning_v31(
        text="text",
        voice_id="voice_id",
    ):
        pass
    verify_request_count(test_id, "POST", "/waves/v1/lightning-v3.1/stream", None, 1)
