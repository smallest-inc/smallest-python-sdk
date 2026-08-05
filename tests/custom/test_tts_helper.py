"""waves TTS convenience helpers collapse the synthesize_* surface to two obvious
entry points. Verified with a mocked client (no network)."""
import os
import tempfile
import unittest
from unittest import mock

from smallestai.waves.helpers import (
    CONTENT_EXPIRY_HEADER,
    DEFAULT_TTS_MODEL,
    EXPIRE_CONTENT_HEADER,
    synthesize_bytes,
    synthesize_to_file,
    synthesize_with_expiry,
)


def _client(chunks):
    c = mock.MagicMock()
    c.waves.synthesize_tts.return_value = iter(chunks)
    return c


class TtsHelperTest(unittest.TestCase):
    def test_synthesize_bytes_joins_chunks(self):
        c = _client([b"ab", b"cd", b"e"])
        self.assertEqual(synthesize_bytes(c, "hi", voice_id="v"), b"abcde")

    def test_synthesize_to_file_writes_and_counts(self):
        c = _client([b"12", b"345"])
        path = os.path.join(tempfile.gettempdir(), "ut_tts_helper.bin")
        n = synthesize_to_file(c, "hi", voice_id="v", path=path)
        self.assertEqual(n, 5)
        with open(path, "rb") as fh:
            self.assertEqual(fh.read(), b"12345")

    def test_defaults_and_kwargs_forwarded(self):
        c = _client([b"x"])
        synthesize_bytes(c, "hi", voice_id="v", speed=1.2)
        _, kw = c.waves.synthesize_tts.call_args
        self.assertEqual(kw["voice_id"], "v")
        self.assertEqual(kw["model"], DEFAULT_TTS_MODEL)
        self.assertEqual(kw["output_format"], "wav")
        self.assertEqual(kw["speed"], 1.2)

    def test_expire_content_sets_header_and_preserves_caller_headers(self):
        c = _client([b"x"])
        synthesize_bytes(
            c,
            "hi",
            voice_id="v",
            expire_content=True,
            request_options={"additional_headers": {"x-trace": "1"}},
        )
        _, kw = c.waves.synthesize_tts.call_args
        headers = kw["request_options"]["additional_headers"]
        self.assertEqual(headers[EXPIRE_CONTENT_HEADER], "true")
        self.assertEqual(headers["x-trace"], "1")  # caller header preserved

    def test_no_header_when_expire_content_false(self):
        c = _client([b"x"])
        synthesize_bytes(c, "hi", voice_id="v")
        _, kw = c.waves.synthesize_tts.call_args
        self.assertNotIn("request_options", kw)

    def test_synthesize_with_expiry_returns_outcome(self):
        c = mock.MagicMock()
        raw = mock.MagicMock()
        raw.data = iter([b"ab", b"cd"])
        raw.headers = {CONTENT_EXPIRY_HEADER: "not-entitled"}
        cm = mock.MagicMock()
        cm.__enter__.return_value = raw
        c.waves.with_raw_response.synthesize_tts.return_value = cm
        audio, outcome = synthesize_with_expiry(c, "hi", voice_id="v")
        self.assertEqual(audio, b"abcd")
        self.assertEqual(outcome, "not-entitled")
        _, kw = c.waves.with_raw_response.synthesize_tts.call_args
        self.assertEqual(kw["request_options"]["additional_headers"][EXPIRE_CONTENT_HEADER], "true")


if __name__ == "__main__":
    unittest.main()
