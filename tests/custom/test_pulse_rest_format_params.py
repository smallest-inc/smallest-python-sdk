"""Regression test for Pulse REST formatting-flag parameters.

The spec at fern/apis/waves/openapi/pulse-stt-openapi.yaml documents three
query params on POST /waves/v1/pulse/get_text — `format`, `punctuate`, and
`capitalize` (string enum "true"/"false"). They were missing from the
4.3.x SDK; restored in 4.4.0. This test guards against the regression
by asserting all four client surfaces accept the params.
"""

import inspect


def _assert_pulse_params_present(method, label: str) -> None:
    sig = inspect.signature(method)
    for name in ("format", "punctuate", "capitalize"):
        assert name in sig.parameters, f"{label}.transcribe_pulse missing `{name}` param"


def test_sync_wrapper_transcribe_pulse_has_format_params() -> None:
    from smallestai.waves.client import WavesClient

    _assert_pulse_params_present(WavesClient.transcribe_pulse, "WavesClient")


def test_async_wrapper_transcribe_pulse_has_format_params() -> None:
    from smallestai.waves.client import AsyncWavesClient

    _assert_pulse_params_present(AsyncWavesClient.transcribe_pulse, "AsyncWavesClient")


def test_sync_raw_transcribe_pulse_has_format_params() -> None:
    from smallestai.waves.raw_client import RawWavesClient

    _assert_pulse_params_present(RawWavesClient.transcribe_pulse, "RawWavesClient")


def test_async_raw_transcribe_pulse_has_format_params() -> None:
    from smallestai.waves.raw_client import AsyncRawWavesClient

    _assert_pulse_params_present(AsyncRawWavesClient.transcribe_pulse, "AsyncRawWavesClient")
