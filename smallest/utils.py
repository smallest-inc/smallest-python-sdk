import re
import io
import unicodedata
from typing import List
from pydub import AudioSegment
from dataclasses import dataclass
from sacremoses import MosesPunctNormalizer

from .exceptions import ValidationError
from .models import TTSModels, TTSLanguages, TTSVoices


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"
SENTENCE_END_REGEX = re.compile(r'.*[-.!?;:…\n]$')
SAMPLE_WIDTH = 2
CHANNELS = 1


@dataclass
class TTSOptions:
    model: TTSModels
    sample_rate: int
    voice: TTSVoices
    api_key: str
    add_wav_header: bool
    speed: float
    transliterate: bool
    remove_extra_silence: bool


def validate_input(text: str, voice: TTSVoices, model: TTSModels, sample_rate: int, speed: float):
    if not text:
        raise ValidationError("Text cannot be empty")
    if voice not in TTSVoices.__args__:
        raise ValidationError(f"Invalid voice: {voice}")
    if model not in ['lightning']:
        raise ValidationError(f"Invalid model: {model}")
    if not 8000 <= sample_rate <= 48000:
        raise ValidationError(f"Invalid sample rate: {sample_rate}. Must be between 8000 and 48000")
    if not 0.5 <= speed <= 2.0:
        raise ValidationError(f"Invalid speed: {speed}. Must be between 0.5 and 2.0")


def add_wav_header(frame_input: bytes, sample_rate: int = 24000, sample_width: int = 2, channels: int = 1) -> bytes:
        audio = AudioSegment(data=frame_input, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
        wav_buf = io.BytesIO()
        audio.export(wav_buf, format="wav")
        wav_buf.seek(0)
        return wav_buf.read()


def preprocess_text(text: str) -> str:
    # Replace special characters with their normal form
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = text.lower()
    # Normalize punctuation using Moses punct normalizer
    mpn = MosesPunctNormalizer()
    text = mpn.normalize(text)
    return text.strip()


def get_smallest_languages() -> List[str]:
    return list(TTSLanguages.__args__)

def get_smallest_voices() -> List[str]:
    return list(TTSVoices.__args__)

def get_smallest_models() -> List[str]:
    return ["lightning"]
