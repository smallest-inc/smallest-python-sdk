import json
import base64
import time
import threading
import queue
from typing import Generator
from dataclasses import dataclass
from websocket import WebSocketApp

@dataclass
class TTSConfig:
    voice_id: str
    api_key: str
    language: str = "en"
    sample_rate: int = 24000
    speed: float = 1.0
    consistency: float = 0.5
    enhancement: int = 1
    similarity: float = 0
    max_buffer_flush_ms: int = 0

class WavesStreamingTTS:
    def __init__(self, config: TTSConfig):
        self.config = config
        self.ws_url = "wss://waves-api.smallest.ai/api/v1/lightning-v2/get_speech/stream"
        self.ws = None
        self.audio_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.is_complete = False
        self.is_connected = False
        self.request_id = None
        
    def _get_headers(self):
        return [f"Authorization: Bearer {self.config.api_key}"]
    
    def _create_payload(self, text: str, continue_stream: bool = False, flush: bool = False):
        return {
            "voice_id": self.config.voice_id,
            "text": text,
            "language": self.config.language,
            "sample_rate": self.config.sample_rate,
            "speed": self.config.speed,
            "consistency": self.config.consistency,
            "similarity": self.config.similarity,
            "enhancement": self.config.enhancement,
            "max_buffer_flush_ms": self.config.max_buffer_flush_ms,
            "continue": continue_stream,
            "flush": flush
        }
    
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
            on_close=self._on_close
        )
        
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
        
        timeout = 5.0
        start_time = time.time()
        while not self.is_connected and time.time() - start_time < timeout:
            time.sleep(0.1)
            
        if not self.is_connected:
            raise Exception("Failed to connect to WebSocket")
    
    def synthesize(self, text: str) -> Generator[bytes, None, None]:
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
    
    def synthesize_streaming(self, text_stream: Generator[str, None, None], 
                           continue_stream: bool = True, 
                           auto_flush: bool = True) -> Generator[bytes, None, None]:
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