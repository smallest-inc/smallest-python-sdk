from .conftest import get_client, verify_request_count

from smallestai.speech import ElectronMessage


def test_waves_electron_complete() -> None:
    """Test complete endpoint with WireMock"""
    test_id = "waves.electron.complete.0"
    client = get_client(test_id)
    client.speech.electron.complete(
        model="electron",
        messages=[
            ElectronMessage(
                role="user",
                content="Hello!",
            )
        ],
    )
    verify_request_count(test_id, "POST", "/waves/v1/chat/completions", None, 1)
