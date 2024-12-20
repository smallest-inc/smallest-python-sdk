import re
import io
import unicodedata
from typing import List
from pydub import AudioSegment
from dataclasses import dataclass
from sacremoses import MosesPunctNormalizer

from smallest.exceptions import ValidationError
from smallest.models import TTSModels, TTSLanguages, TTSVoices


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"
SENTENCE_END_REGEX = re.compile(r'.*[-.—!?;:…\n]$')
CHUNK_SIZE = 250
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
    if voice not in TTSVoices:
        raise ValidationError(f"Invalid voice: {voice}")
    if model not in TTSModels:
        raise ValidationError(f"Invalid model: {model}")
    if not 8000 <= sample_rate <= 24000:
        raise ValidationError(f"Invalid sample rate: {sample_rate}. Must be between 8000 and 24000")
    if not 0.5 <= speed <= 2.0:
        raise ValidationError(f"Invalid speed: {speed}. Must be between 0.5 and 2.0")


def add_wav_header(frame_input: bytes, sample_rate: int = 24000, sample_width: int = 2, channels: int = 1) -> bytes:
        audio = AudioSegment(data=frame_input, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
        wav_buf = io.BytesIO()
        audio.export(wav_buf, format="wav")
        wav_buf.seek(0)
        return wav_buf.read()


def preprocess_text(text: str) -> str:
    text = text.replace("\n", " ").replace("\t", " ").replace("—", " ")
    text = re.sub(r'\s+', ' ', text)
    mpn = MosesPunctNormalizer()
    text = mpn.normalize(text)
    return text.strip()


def split_into_chunks(text: str) -> List[str]:
    """
    Splits the input text into chunks based on sentence boundaries
    defined by SENTENCE_END_REGEX and the maximum chunk size.
    Only splits at valid sentence boundaries to avoid breaking words.
    """
    chunks = []
    while text:
        # If the remaining text is shorter than chunk size, add it as final chunk
        if len(text) <= CHUNK_SIZE:
            chunks.append(text.strip())
            break

        # Find the last sentence boundary within CHUNK_SIZE
        chunk_text = text[:CHUNK_SIZE]
        last_break_index = -1

        # Check each character in reverse order to find last punctuation
        for i in range(len(chunk_text) - 1, -1, -1):
            if chunk_text[i] in '-.—!?;:…\n':
                last_break_index = i
                break

        if last_break_index == -1:
            # If no punctuation found in chunk, look for the last space
            # to avoid breaking words
            last_space = chunk_text.rfind(' ')
            if last_space != -1:
                last_break_index = last_space
            else:
                # If no space found, use the full chunk size
                last_break_index = CHUNK_SIZE - 1

        # Add the chunk up to the break point
        chunks.append(text[:last_break_index + 1].strip())
        # Continue with remaining text
        text = text[last_break_index + 1:].strip()

    return chunks


def get_smallest_languages() -> List[str]:
    return list(TTSLanguages)

def get_smallest_voices() -> List[str]:
    return list(TTSVoices)

def get_smallest_models() -> List[str]:
    return ["lightning"]
