import io
import re
import unicodedata
from sacremoses import MosesPunctNormalizer
from pydub import AudioSegment
import time
import asyncio
import websockets
import websocket as sync_websocket
import json
from typing import List, Generator, AsyncGenerator
from dataclasses import dataclass

from .models import TTSModels, TTSLanguages, TTSVoices
from .exceptions import ValidationError


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"
SENTENCE_END_REGEX = re.compile(r'.*[-.!?;:…]$')
SAMPLE_WIDTH = 2
CHANNELS = 1

@dataclass
class TTSOptions:
    model: TTSModels
    sample_rate: int
    voice: TTSVoices
    api_key: str
    language: TTSLanguages
    add_wav_header: bool
    speed: float
    transliterate: bool
    remove_extra_silence: bool

def validate_input(text: str, voice: TTSVoices, model: TTSModels, language: TTSLanguages, sample_rate: int, speed: float):
    if not text:
        raise ValidationError("Text cannot be empty")
    if voice not in TTSVoices.__args__:
        raise ValidationError(f"Invalid voice: {voice}")
    if model not in TTSModels.__args__:
        raise ValidationError(f"Invalid model: {model}")
    if language not in TTSLanguages.__args__:
        raise ValidationError(f"Invalid language: {language}")
    if not 8000 <= sample_rate <= 48000:
        raise ValidationError(f"Invalid sample rate: {sample_rate}. Must be between 8000 and 48000")
    if not 0.5 <= speed <= 2.0:
        raise ValidationError(f"Invalid speed: {speed}. Must be between 0.5 and 2.0")


def preprocess_text(text: str) -> str:
    # Replace special characters with their normal form
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    # Normalize punctuation using Moses punct normalizer
    mpn = MosesPunctNormalizer()
    text = mpn.normalize(text)
    return text.strip()


def calculate_chunk_size(text: str, speed: float = 1.0, sample_rate: int = 24000, default_wpm: int = 130, chunks_count: int = 50) -> int:
        word_count = len(preprocess_text(text).split())
        adjusted_wpm = default_wpm * speed
        duration_seconds = (word_count / adjusted_wpm) * 60
        bytes_per_second = sample_rate * 2  
        total_audio_size = int(bytes_per_second * duration_seconds)
        return max(1024, total_audio_size // chunks_count)


def add_wav_header(frame_input: bytes, sample_rate: int = 24000, sample_width: int = 2, channels: int = 1) -> bytes:
        audio = AudioSegment(data=frame_input, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
        wav_buf = io.BytesIO()
        audio.export(wav_buf, format="wav")
        wav_buf.seek(0)
        return wav_buf.read()


async def waves_streaming(url: str, payloads: list, headers: dict, timeout: int = 2) -> AsyncGenerator[bytes, None]:
    try:
        async with websockets.connect(url, extra_headers=headers) as ws:
            for payload in payloads:
                data = json.dumps(payload)
                await ws.send(data)

                while True:
                    try:
                        response_part = await asyncio.wait_for(ws.recv(), timeout=timeout)
                        
                        if response_part == "<START>":
                            continue
                        elif response_part == "<END>":
                            break
                        elif isinstance(response_part, bytes):
                            yield response_part
                            
                    except asyncio.TimeoutError:
                        break

    except websockets.exceptions.ConnectionClosed as e:
        if e.code == 1000:
            print("Connection closed normally (code 1000).")
        else:
            print(f"Connection closed with code {e.code}: {e.reason}")
    except Exception as e:
        print(f"Exception occurred: {e}")
        

def sync_waves_streaming(url: str, payloads: list, headers: dict, timeout: int = 2) -> Generator[bytes, None]:
    try:
        # Convert headers to the format expected by websocket-client
        header_list = [f"{k}: {v}" for k, v in headers.items()]
        ws = sync_websocket.create_connection(url, header=header_list, timeout=timeout)

        for payload in payloads:
            data = json.dumps(payload)
            ws.send(data)

            while True:
                try:
                    response_part = ws.recv()
                    if response_part == "<START>":
                        continue
                    elif response_part == "<END>":
                        break
                    elif isinstance(response_part, bytes):
                        yield response_part
                except sync_websocket.WebSocketTimeoutException:
                    break

        ws.close()

    except sync_websocket.WebSocketConnectionClosedException as e:
        print(f"Connection closed: {e}")
        return
    except Exception as e:
        print(f"Exception occurred: {e}")
        return


def get_smallest_languages() -> List[str]:
    return list(TTSLanguages.__args__)

def get_smallest_voices() -> List[str]:
    return list(TTSVoices.__args__)

def get_smallest_models() -> List[str]:
    return ["lightning"]
