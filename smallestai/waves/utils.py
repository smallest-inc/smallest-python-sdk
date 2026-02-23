import os
from typing import List, Optional

from smallestai.waves.exceptions import ValidationError
from smallestai.waves.models import (
    TTSModels,
    TTSLanguages_lightning_v2,
    TTSLanguages_lightning_v3_1,
    STTModels,
    STTLanguages_pulse,
)


API_BASE_URL = "https://waves-api.smallest.ai/api/v1"

SAMPLE_WIDTH = 2
CHANNELS = 1
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav']

VALID_SAMPLE_RATES = {
    "lightning-v2": [8000, 16000, 24000],
    "lightning-v3.1": [8000, 16000, 24000, 44100],
}

DEFAULT_SAMPLE_RATES = {
    "lightning-v2": 24000,
    "lightning-v3.1": 44100,
}


def validate_stt_input(file_path: str, model: str, language: str):
    """Validate STT input parameters."""
    if not os.path.isfile(file_path):
        raise ValidationError("Invalid file path. File does not exist.")
    if model not in STTModels:
        raise ValidationError(f"Invalid model: {model}. Must be one of {STTModels}")
    if language not in STTLanguages_pulse:
        raise ValidationError(f"Invalid language: {language}. Must be one of {STTLanguages_pulse}")


def validate_tts_input(
    text: str,
    model: str,
    sample_rate: int,
    speed: float,
    consistency: Optional[float] = None,
    similarity: Optional[float] = None,
    enhancement: Optional[int] = None
):
    """Validate TTS input parameters."""
    if not text:
        raise ValidationError("Text cannot be empty.")
    if model not in TTSModels:
        raise ValidationError(f"Invalid model: {model}. Must be one of {TTSModels}")
    
    valid_rates = VALID_SAMPLE_RATES.get(model, [8000, 16000, 24000])
    if sample_rate not in valid_rates:
        raise ValidationError(f"Invalid sample rate: {sample_rate}. Must be one of {valid_rates} for model {model}")
    
    if not 0.5 <= speed <= 2.0:
        raise ValidationError(f"Invalid speed: {speed}. Must be between 0.5 and 2.0")
    
    if model == "lightning-v2":
        if consistency is not None and not 0.0 <= consistency <= 1.0:
            raise ValidationError(f"Invalid consistency: {consistency}. Must be between 0.0 and 1.0")
        if similarity is not None and not 0.0 <= similarity <= 1.0:
            raise ValidationError(f"Invalid similarity: {similarity}. Must be between 0.0 and 1.0")
        if enhancement is not None and not 0 <= enhancement <= 2:
            raise ValidationError(f"Invalid enhancement: {enhancement}. Must be between 0 and 2.")


def get_smallest_languages(model: str = 'lightning-v3.1') -> List[str]:
    """Get available languages for a model (TTS or STT)."""
    if model == 'lightning-v2':
        return TTSLanguages_lightning_v2
    elif model == 'lightning-v3.1':
        return TTSLanguages_lightning_v3_1
    elif model == 'pulse':
        return STTLanguages_pulse
    else:
        all_models = TTSModels + STTModels
        raise ValidationError(f"Invalid model: {model}. Must be one of {all_models}")


def get_tts_models() -> List[str]:
    """Get available TTS models."""
    return TTSModels


def get_stt_models() -> List[str]:
    """Get available STT models."""
    return STTModels
