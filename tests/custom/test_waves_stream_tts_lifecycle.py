"""Socket lifecycle for the WavesStreamingTTS shim.

Every path that opens the WebSocket has to close it again. Before the fix only the
two happy paths did: an error mid-stream raised straight past the close, a caller who
stopped consuming the generator early left it open, and start_streaming_session never
closed at all and exposed no way to do it by hand.

No network: WebSocketApp is replaced with a fake that records sends and closes and
drives the callbacks itself.
"""

import json
from unittest.mock import patch

import pytest

from smallestai.waves.stream_tts import TTSConfig, WavesStreamingTTS


class _FakeWebSocketApp:
    """Stands in for websocket.WebSocketApp. `script` runs once the socket is open."""

    script = None
    opened = []

    def __init__(self, url, header=None, on_open=None, on_message=None, on_error=None, on_close=None):
        type(self).opened.append(self)
        self.url = url
        self.header = header
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.sent = []
        self.close_calls = 0

    def run_forever(self):
        self.on_open(self)
        if type(self).script is not None:
            type(self).script(self)

    def send(self, payload):
        self.sent.append(payload)

    def close(self):
        self.close_calls += 1

    # helpers the scripts use to act like the server
    def audio(self, raw_b64, status=""):
        self.on_message(self, json.dumps({"status": status, "data": {"audio": raw_b64}}))

    def complete(self):
        self.on_message(self, json.dumps({"status": "complete"}))

    def fail(self, message):
        self.on_message(self, json.dumps({"status": "error", "message": message}))


def _tts(script=None):
    _FakeWebSocketApp.script = script
    return WavesStreamingTTS(TTSConfig(voice_id="magnus", api_key="k"))


def _only_socket():
    """The one socket the run opened, so a test can ask whether it was closed."""
    assert len(_FakeWebSocketApp.opened) == 1
    return _FakeWebSocketApp.opened[0]


@pytest.fixture(autouse=True)
def _fake_socket():
    _FakeWebSocketApp.script = None
    _FakeWebSocketApp.opened = []
    with patch("smallestai.waves.stream_tts.WebSocketApp", _FakeWebSocketApp):
        yield
    _FakeWebSocketApp.script = None
    _FakeWebSocketApp.opened = []


def test_synthesize_closes_the_socket_when_the_stream_completes():
    tts = _tts(lambda ws: (ws.audio("aGk="), ws.complete()))

    chunks = list(tts.synthesize("hello"))

    assert chunks == [b"hi"]
    assert _only_socket().close_calls == 1


def test_synthesize_closes_the_socket_when_the_stream_errors():
    """The raise used to jump straight past the close, leaking the socket and its thread."""
    tts = _tts(lambda ws: ws.fail("upstream exploded"))

    with pytest.raises(Exception, match="upstream exploded"):
        list(tts.synthesize("hello"))

    assert _only_socket().close_calls == 1


def test_synthesize_closes_the_socket_when_the_caller_stops_early():
    """A consumer that breaks out of the loop never reached the close either."""
    tts = _tts(lambda ws: (ws.audio("YQ=="), ws.audio("Yg=="), ws.audio("Yw==")))

    stream = tts.synthesize("hello")
    assert next(stream) == b"a"
    stream.close()

    assert _only_socket().close_calls == 1


def test_start_streaming_session_closes_the_socket():
    """This one had no close on any path, and no public way to reach the socket."""
    tts = _tts(lambda ws: ws.complete())

    list(tts.start_streaming_session())

    assert _only_socket().close_calls == 1


def test_close_is_public_and_safe_to_repeat():
    tts = _tts(lambda ws: None)
    tts._connect()
    socket = tts.ws
    assert socket is not None

    tts.close()
    tts.close()

    assert tts.ws is None
    assert tts.is_connected is False
    assert socket.close_calls == 1


def test_a_connect_that_times_out_closes_the_half_open_socket():
    class _FastClock:
        def __init__(self):
            self.now = 0.0

        def time(self):
            self.now += 5.0
            return self.now

        def sleep(self, _seconds):
            pass

    never_opens = type("_NeverOpens", (_FakeWebSocketApp,), {"run_forever": lambda self: None})

    with patch("smallestai.waves.stream_tts.WebSocketApp", never_opens):
        with patch("smallestai.waves.stream_tts.time", _FastClock()):
            tts = WavesStreamingTTS(TTSConfig(voice_id="magnus", api_key="k"))
            with pytest.raises(Exception, match="Failed to connect"):
                tts._connect()

    assert _only_socket().close_calls == 1
