"""waves TTS convenience helpers collapse the synthesize_* surface to two obvious
entry points. Verified with a mocked client (no network)."""
import os
import tempfile
import unittest
from unittest import mock

from smallestai.waves.helpers import DEFAULT_TTS_MODEL, synthesize_bytes, synthesize_to_file


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


if __name__ == "__main__":
    unittest.main()
