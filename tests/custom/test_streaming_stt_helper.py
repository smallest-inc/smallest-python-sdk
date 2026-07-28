"""Unit tests for the typed streaming-STT helper (waves.helpers.stream_speech_to_text).

Logic-only: a fake client captures the request_options passed to
client.waves.speech_to_text.stream(...). No network, no real SDK STT surface needed.
"""

from smallestai.waves.helpers.streaming_stt import (
    build_stt_stream_query,
    stream_speech_to_text,
)


class _FakeStreamNamespace:
    def __init__(self):
        self.captured_request_options = None

    def stream(self, *, request_options=None):
        self.captured_request_options = request_options
        return "SOCKET_CM"  # stand-in for the context manager


class _FakeClient:
    def __init__(self):
        stt = _FakeStreamNamespace()
        self.waves = type("_W", (), {"speech_to_text": stt})()
        self._stt = stt


def test_defaults_and_required_language():
    q = build_stt_stream_query(language="en")
    assert q == {
        "model": "pulse",
        "language": "en",
        "sample_rate": 16000,
        "encoding": "linear16",
    }


def test_booleans_serialize_as_strings():
    q = build_stt_stream_query(
        language="hi",
        itn_normalize=True,
        finalize_on_words=False,
        punctuate=True,
        vad_events=False,
    )
    assert q["itn_normalize"] == "true"
    assert q["finalize_on_words"] == "false"
    assert q["punctuate"] == "true"
    assert q["vad_events"] == "false"


def test_keyword_boosting_list_is_comma_joined():
    q = build_stt_stream_query(language="en", keywords=["Smallest", "Atoms", "Waves"])
    assert q["keywords"] == "Smallest,Atoms,Waves"


def test_keyword_boosting_string_passes_through():
    q = build_stt_stream_query(language="en", keywords="Smallest,Atoms")
    assert q["keywords"] == "Smallest,Atoms"


def test_redaction_lists_are_comma_joined():
    q = build_stt_stream_query(language="en", redact_pii=["ssn", "email"], redact_pci=["card"])
    assert q["redact_pii"] == "ssn,email"
    assert q["redact_pci"] == "card"


def test_full_boolean_knob_set_serializes():
    q = build_stt_stream_query(
        language="en",
        word_timestamps=True,
        sentence_timestamps=False,
        diarize=True,
        capitalize=False,
        numerals=True,
        full_transcript=True,
        vad=False,
    )
    assert q["word_timestamps"] == "true"
    assert q["sentence_timestamps"] == "false"
    assert q["diarize"] == "true"
    assert q["capitalize"] == "false"
    assert q["numerals"] == "true"
    assert q["full_transcript"] == "true"
    assert q["vad"] == "false"


def test_value_params_pass_through():
    q = build_stt_stream_query(language="en", max_words=6, format="json", eou_timeout_ms=800)
    assert q["max_words"] == 6
    assert q["format"] == "json"
    assert q["eou_timeout_ms"] == 800


def test_none_optionals_are_omitted():
    q = build_stt_stream_query(language="en", eou_timeout_ms=None, vad_threshold=None)
    assert "eou_timeout_ms" not in q
    assert "vad_threshold" not in q


def test_numeric_optionals_pass_through():
    q = build_stt_stream_query(
        language="en", eou_timeout_ms=1000, vad_threshold=0.5, vad_min_speech_ms=120
    )
    assert q["eou_timeout_ms"] == 1000
    assert q["vad_threshold"] == 0.5
    assert q["vad_min_speech_ms"] == 120


def test_helper_forwards_query_into_request_options():
    client = _FakeClient()
    cm = stream_speech_to_text(client, language="en", sample_rate=8000)
    assert cm == "SOCKET_CM"
    ro = client._stt.captured_request_options
    assert ro["additional_query_parameters"] == {
        "model": "pulse",
        "language": "en",
        "sample_rate": 8000,
        "encoding": "linear16",
    }


def test_caller_overrides_win_over_typed_values():
    client = _FakeClient()
    stream_speech_to_text(
        client,
        language="en",
        additional_query_parameters={"language": "hi", "custom_flag": "x"},
    )
    aqp = client._stt.captured_request_options["additional_query_parameters"]
    assert aqp["language"] == "hi"  # caller override wins
    assert aqp["custom_flag"] == "x"  # unknown params still reach the wire


def test_existing_request_options_preserved():
    client = _FakeClient()
    stream_speech_to_text(
        client, language="en", request_options={"max_retries": 3}
    )
    ro = client._stt.captured_request_options
    assert ro["max_retries"] == 3
    assert ro["additional_query_parameters"]["language"] == "en"


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL {fn.__name__}: {e}")
    print(f"\n==== {len(fns) - failed} PASS / {failed} FAIL ====")
    sys.exit(1 if failed else 0)
