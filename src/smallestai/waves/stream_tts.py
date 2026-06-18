"""
WavesStreamingTTS — thin compatibility shim for the legacy
`from smallestai.waves import WavesStreamingTTS, TTSConfig` pattern
shipped in smallestai==4.3.1.

This wraps the Lightning v3.1 streaming WebSocket endpoint
(`wss://api.smallest.ai/waves/v1/lightning-v3.1/get_speech/stream`).

Code that worked on 4.3.1 keeps working on 4.4.0 with one
behavior change: the underlying model is `lightning-v3.1` (not the
deprecated `lightning-v2`). This means:
  - Removed `consistency` param (v2-only — silently dropped if passed).
  - Added `pronunciation_dicts` param.
  - Output audio is 44.1 kHz capable.

For new code, prefer the namespaced Fern client:

    client.waves.lightning_v31tts.connect(...)

This shim exists to avoid breaking customers on the 4.3.1 pattern.
"""
import json
import base64
import time
import threading
import queue
from typing import Generator, Optional, Sequence
from dataclasses import dataclass, field

from websocket import WebSocketApp  # from `websocket-client` package


@dataclass
class TTSConfig:
    """Configuration for WavesStreamingTTS.

    Mirrors the 4.3.1 shape; `consistency` was removed because Lightning
    v3.1 does not accept it (silently dropped if passed via dict).
    """
    voice_id: str
    api_key: str
    language: str = "en"
    sample_rate: int = 24000
    speed: float = 1.0
    enhancement: Optional[int] = None
    similarity: Optional[float] = None
    max_buffer_flush_ms: int = 0
    pronunciation_dicts: Optional[Sequence[str]] = None


class WavesStreamingTTS:
    """Streaming TTS over WebSocket against Lightning v3.1.

    Example::

        from smallestai.waves import WavesStreamingTTS, TTSConfig
        config = TTSConfig(voice_id="magnus", api_key="...")
        streaming_tts = WavesStreamingTTS(config)
        audio_chunks = list(streaming_tts.synthesize("Hello world"))
    """

    # Lightning v3.1 streaming endpoint. Old 4.3.1 hardcoded the deprecated
    # v2 endpoint — that was a bug and is fixed in 4.4.0.
    WS_URL = "wss://api.smallest.ai/waves/v1/lightning-v3.1/get_speech/stream"

    def __init__(self, config: TTSConfig):
        self.config = config
        self.ws_url = self.WS_URL
        self.ws: Optional[WebSocketApp] = None
        self.audio_queue: queue.Queue = queue.Queue()
        self.error_queue: queue.Queue = queue.Queue()
        self.is_complete = False
        self.is_connected = False
        self.request_id: Optional[str] = None

    def _get_headers(self):
        return [f"Authorization: Bearer {self.config.api_key}"]

    def _create_payload(self, text: str, continue_stream: bool = False, flush: bool = False) -> dict:
        payload: dict = {
            "voice_id": self.config.voice_id,
            "text": text,
            "language": self.config.language,
            "sample_rate": self.config.sample_rate,
            "speed": self.config.speed,
            "max_buffer_flush_ms": self.config.max_buffer_flush_ms,
            "continue": continue_stream,
            "flush": flush,
        }
        if self.config.enhancement is not None:
            payload["enhancement"] = self.config.enhancement
        if self.config.similarity is not None:
            payload["similarity"] = self.config.similarity
        if self.config.pronunciation_dicts:
            payload["pronunciation_dicts"] = list(self.config.pronunciation_dicts)
        return payload

    def _on_open(self, ws):
        self.is_connected = True

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            status = data.get("status", "")

            if status == "error":
                self.error_queue.put(Exception(data.get("message", "Unknown error")))
                return

            if not self.request_id:
                self.request_id = data.get("request_id")

            audio_b64 = data.get("data", {}).get("audio")
            if audio_b64:
                self.audio_queue.put(base64.b64decode(audio_b64))

            if status == "complete":
                self.is_complete = True
                self.audio_queue.put(None)

        except Exception as e:
            self.error_queue.put(e)

    def _on_error(self, ws, error):
        self.error_queue.put(error)

    def _on_close(self, ws, *args):
        self.is_connected = False
        if not self.is_complete:
            self.audio_queue.put(None)

    def _connect(self):
        if self.ws:
            self.ws.close()

        self.ws = WebSocketApp(
            self.ws_url,
            header=self._get_headers(),
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        # 10s connect timeout (legacy used 5s — bumped for CI / cold-start tolerance)
        timeout = 10.0
        start_time = time.time()
        while not self.is_connected and time.time() - start_time < timeout:
            time.sleep(0.1)

        if not self.is_connected:
            raise Exception(
                "Failed to connect to WebSocket "
                f"{self.ws_url} within {timeout}s. "
                "Check your network and that SMALLEST_API_KEY is valid."
            )

    def synthesize(self, text: str) -> Generator[bytes, None, None]:
        """Synthesize a single text string and stream back PCM audio chunks."""
        self._reset_state()
        self._connect()

        payload = self._create_payload(text)
        self.ws.send(json.dumps(payload))

        while True:
            if not self.error_queue.empty():
                raise self.error_queue.get()

            try:
                chunk = self.audio_queue.get(timeout=1.0)
                if chunk is None:
                    break
                yield chunk
            except queue.Empty:
                if self.is_complete:
                    break
                continue

        self.ws.close()

    def synthesize_streaming(
        self,
        text_stream: Generator[str, None, None],
        continue_stream: bool = True,
        auto_flush: bool = True,
    ) -> Generator[bytes, None, None]:
        """Synthesize a stream of text chunks. Useful when piping LLM output."""
        self._reset_state()
        self._connect()

        def send_text():
            try:
                for text_chunk in text_stream:
                    if text_chunk.strip():
                        payload = self._create_payload(text_chunk, continue_stream=continue_stream)
                        self.ws.send(json.dumps(payload))

                if auto_flush:
                    flush_payload = self._create_payload("", flush=True)
                    self.ws.send(json.dumps(flush_payload))
            except Exception as e:
                self.error_queue.put(e)

        sender_thread = threading.Thread(target=send_text)
        sender_thread.daemon = True
        sender_thread.start()

        while True:
            if not self.error_queue.empty():
                raise self.error_queue.get()

            try:
                chunk = self.audio_queue.get(timeout=1.0)
                if chunk is None:
                    break
                yield chunk
            except queue.Empty:
                if self.is_complete:
                    break
                continue

        self.ws.close()

    def send_text_chunk(self, text: str, continue_stream: bool = True, flush: bool = False):
        if not self.is_connected:
            raise Exception("WebSocket not connected")
        payload = self._create_payload(text, continue_stream=continue_stream, flush=flush)
        self.ws.send(json.dumps(payload))

    def flush_buffer(self):
        if not self.is_connected:
            raise Exception("WebSocket not connected")
        payload = self._create_payload("", flush=True)
        self.ws.send(json.dumps(payload))

    def start_streaming_session(self) -> Generator[bytes, None, None]:
        self._reset_state()
        self._connect()

        while True:
            if not self.error_queue.empty():
                raise self.error_queue.get()

            try:
                chunk = self.audio_queue.get(timeout=0.1)
                if chunk is None:
                    break
                yield chunk
            except queue.Empty:
                if self.is_complete:
                    break
                continue

    def _reset_state(self):
        self.audio_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.is_complete = False
        self.is_connected = False
        self.request_id = None

