import os
from typing import List
from typing import Optional
from dataclasses import dataclass

from smallestai.waves.exceptions import ValidationError
from smallestai.waves.models import TTSModels, TTSLanguages_lightning, TTSLanguages_lightning_large, TTSLanguages_lightning_v2, ASRModels, ASRLanguages_lightning


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"
WEBSOCKET_URL = "wss://waves-api.smallest.ai/api/v1/lightning-v2/get_speech/stream"
SAMPLE_WIDTH = 2
CHANNELS = 1
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav']


@dataclass
class TTSOptions:
    model: str
    sample_rate: int
    voice_id: str
    api_key: str
    speed: float
    consistency: float
    similarity: float
    enhancement: int
    language: str
    output_format: str
    
@dataclass
class ASROptions:
    model: str
    api_key: str
    language: str
    word_timestamps: bool
    age_detection: bool
    gender_detection: bool
    emotion_detection: bool

def validate_asr_input(file_path: str, model: str, language: str):
    if not os.path.isfile(file_path):
        raise ValidationError("Invalid file path. File does not exist.")
    if model not in ASRModels:
        raise ValidationError(f"Invalid model: {model}. Must be one of {ASRModels}")
    if language not in ASRLanguages_lightning:
        raise ValidationError(f"Invalid language: {language}. Must be one of {ASRLanguages_lightning}")

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
