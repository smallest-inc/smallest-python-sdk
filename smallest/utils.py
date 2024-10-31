import io
import re
import unicodedata
from num2words import num2words
from sacremoses import MosesPunctNormalizer
from pydub import AudioSegment
import time
import asyncio
import websockets
import websocket as sync_websocket
import json
from typing import List
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
    
    # Remove new lines, tabs, multiple spaces, etc
    text = re.sub(r'\s+', ' ', text)
    
    # Turn digits into words
    def replace_numbers(match):
        num = match.group()
        # Handle numbers with commas like '10,000'
        num = num.replace(",", "")
        return num2words(num)
    text = re.sub(r'\b\d{1,3}(,\d{3})*(\.\d{1,2})?\b', replace_numbers, text)
    
    # lower case all the text
    text = text.lower()
    
    # Normalize punctuation using Moses punct normalizer
    mpn = MosesPunctNormalizer()
    text = mpn.normalize(text)
    
    # Replace dots in URLs with 'dot'
    text = re.sub(r'(\w+)\.(\w+)', r'\1 dot \2', text)
    
    return text.strip()


def calculate_chunk_size(
        text: str,
        speed: float = 1.0,
        sample_rate: int = 24000,
        default_wpm: int = 130,
        chunks_count: int = 50
    ) -> int:
        word_count = len(preprocess_text(text).split())
        adjusted_wpm = default_wpm * speed
        duration_seconds = (word_count / adjusted_wpm) * 60
        bytes_per_second = sample_rate * 2  
        total_audio_size = int(bytes_per_second * duration_seconds)
        return max(1024, total_audio_size // chunks_count)


def add_wav_header(frame_input, sample_rate=24000, sample_width=2, channels=1):
        audio = AudioSegment(data=frame_input, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
        wav_buf = io.BytesIO()
        audio.export(wav_buf, format="wav")
        wav_buf.seek(0)
        return wav_buf.read()

async def waves_streaming(url: str, payloads: list, headers: dict, timeout: int = 2, close_connection_timeout: int = 500) -> bytes:
        """Awaaz streaming demo function.

        Args:
            url (str): URL
            payloads (list): List of dictionaries of payloads that are sent to API.

        Returns:
            bytes: Audio bytes generated for the sentences concatenated together.
        """
        wav_audio_bytes = b""
        start_time = time.time()

        try:
            async with websockets.connect(url, extra_headers=headers) as ws:
                 for payload in payloads:
                    data = json.dumps(payload)
                    await ws.send(data)

                    # Collect responses until no more data or timeout
                    response = b""
                    while True:
                        response_part = await asyncio.wait_for(ws.recv(),
                                                               timeout=timeout)
                        if response_part == "<START>":
                            break
                        elif response_part == "<END>":
                            break
                        else:
                            response += response_part

                    # Handle the accumulated response if needed
                    wav_audio_bytes += response
                    time.sleep(1)

                    # Optionally close the connection if needed
                    if (time.time() - start_time) > close_connection_timeout:
                        await ws.close()
                        break 

        except websockets.exceptions.ConnectionClosed as e:
            if e.code == 1000:
                print("Connection closed normally (code 1000).")
            else:
                print(f"Connection closed with code {e.code}: {e.reason}")
            return None
        except Exception as e:
            print(f"Exception occurred: {e}")
        finally:
            return wav_audio_bytes
        

def sync_waves_streaming(url: str, payloads: list, headers: dict, timeout: int = 2, close_connection_timeout: int = 500) -> bytes:
    """waves streaming demo function.
    Args:
        url (str): URL
        payload (list): A dictionary representing the payload to send to the API.
    Returns:
        bytes: Audio bytes generated for the sentences concatenated together.
    """
    wav_audio_bytes = b""
    start_time = time.time()

    try:
        ws = sync_websocket.create_connection(url, header=[f"{k}: {v}" for k, v in headers.items()])

        for payload in payloads:
            data = json.dumps(payload)
            ws.send(data)

            response = b""
            while True:
                response_part = ws.recv()
                if response_part == "<START>":
                    break
                elif response_part == "<END>":
                    break
                else:
                    response += response_part

            wav_audio_bytes += response

            if (time.time() - start_time) > close_connection_timeout:
                ws.close()
                print("Connection closed due to timeout.")
                return wav_audio_bytes

        ws.close()

    except sync_websocket.WebSocketConnectionClosedException as e:
        print(f"Connection closed: {e}")
        return None
    except Exception as e:
        print(f"Exception occurred: {e}")

    return wav_audio_bytes


def get_smallest_languages() -> List[str]:
    return list(TTSLanguages.__args__)

def get_smallest_voices() -> List[str]:
    return list(TTSVoices.__args__)

def get_smallest_models() -> List[str]:
    return ["lightning"]