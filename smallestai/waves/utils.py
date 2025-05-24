import re
import io
from typing import List
from typing import Optional
from pydub import AudioSegment
from dataclasses import dataclass

from smallestai.waves.exceptions import ValidationError
from smallestai.waves.models import TTSModels, TTSLanguages_lightning, TTSLanguages_lightning_large, TTSLanguages_lightning_v2


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"
SENTENCE_END_REGEX = re.compile(r'.*[-.—!?,;:…।|]$')
SAMPLE_WIDTH = 2
CHANNELS = 1
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav']


@dataclass
class TTSOptions:
    model: str
    sample_rate: int
    voice_id: str
    api_key: str
    add_wav_header: bool
    speed: float
    consistency: float
    similarity: float
    enhancement: int


def validate_input(text: str, model: str, sample_rate: int, speed: float, consistency: Optional[float] = None, similarity: Optional[float] = None, enhancement: Optional[int] = None):
    if not text:
        raise ValidationError("Text cannot be empty.")
    if model not in TTSModels:
        raise ValidationError(f"Invalid model: {model}. Must be one of {TTSModels}")
    if not 8000 <= sample_rate <= 24000:
        raise ValidationError(f"Invalid sample rate: {sample_rate}. Must be between 8000 and 24000")
    if not 0.5 <= speed <= 2.0:
        raise ValidationError(f"Invalid speed: {speed}. Must be between 0.5 and 2.0")
    if consistency is not None and not 0.0 <= consistency <= 1.0:
        raise ValidationError(f"Invalid consistency: {consistency}. Must be between 0.0 and 1.0")
    if similarity is not None and not 0.0 <= similarity <= 1.0:
        raise ValidationError(f"Invalid similarity: {similarity}. Must be between 0.0 and 1.0")
    if enhancement is not None and not 0 <= enhancement <= 2:
        raise ValidationError(f"Invalid enhancement: {enhancement}. Must be between 0 and 2.")


def add_wav_header(frame_input: bytes, sample_rate: int = 24000, sample_width: int = 2, channels: int = 1) -> bytes:
    audio = AudioSegment(data=frame_input, sample_width=sample_width, frame_rate=sample_rate, channels=channels)
    wav_buf = io.BytesIO()
    audio.export(wav_buf, format="wav")
    wav_buf.seek(0)
    return wav_buf.read()


def preprocess_text(text: str) -> str:
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 250) -> List[str]:
    chunks = []
    while text:
        if len(text) <= chunk_size:
            chunks.append(text.strip())
            break

        chunk_text = text[:chunk_size]
        last_break_index = -1

        # Find last sentence boundary using regex
        for i in range(len(chunk_text) - 1, -1, -1):
            if SENTENCE_END_REGEX.match(chunk_text[:i + 1]):
                last_break_index = i
                break

        if last_break_index == -1:
            # Fallback to space if no sentence boundary found
            last_space = chunk_text.rfind(' ')
            if last_space != -1:
                last_break_index = last_space 
            else:
                last_break_index = chunk_size - 1

        chunks.append(text[:last_break_index + 1].strip())
        text = text[last_break_index + 1:].strip()

    return chunks


def get_smallest_languages(model: str = 'lightning') -> List[str]:
    if model == 'lightning':
        return TTSLanguages_lightning
    elif model == 'lightning-large':
        return TTSLanguages_lightning_large
    elif model == 'lightning-v2':
        return TTSLanguages_lightning_v2
    else:
        raise ValidationError(f"Invalid model: {model}. Must be one of {TTSModels}")

def get_smallest_models() -> List[str]:
    return TTSModels
