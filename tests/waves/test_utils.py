import pytest
from smallestai.waves.utils import validate_input, get_smallest_languages, get_smallest_models
from smallestai.waves.exceptions import ValidationError
from smallestai.waves.models import TTSModels, TTSLanguages_lightning, TTSLanguages_lightning_large, TTSLanguages_lightning_v2

def test_validate_input_valid():
    """Tests that validate_input passes with valid parameters."""
    validate_input(text="hello world", model="lightning", sample_rate=16000, speed=1.0)
    validate_input(
        text="test",
        model="lightning-large",
        sample_rate=24000,
        speed=2.0,
        consistency=0.5,
        similarity=0.5,
        enhancement=1
    )

def test_validate_input_invalid():
    """Tests that validate_input raises ValidationError for invalid parameters."""
    with pytest.raises(ValidationError, match="Text cannot be empty"):
        validate_input(text="", model="lightning", sample_rate=16000, speed=1.0)

    with pytest.raises(ValidationError, match="Invalid model"):
        validate_input(text="test", model="invalid-model", sample_rate=16000, speed=1.0)

    with pytest.raises(ValidationError, match="Invalid sample rate"):
        validate_input(text="test", model="lightning", sample_rate=7000, speed=1.0)

    with pytest.raises(ValidationError, match="Invalid speed"):
        validate_input(text="test", model="lightning", sample_rate=16000, speed=3.0)

    with pytest.raises(ValidationError, match="Invalid consistency"):
        validate_input(text="test", model="lightning-large", sample_rate=16000, speed=1.0, consistency=1.1)

    with pytest.raises(ValidationError, match="Invalid similarity"):
        validate_input(text="test", model="lightning-large", sample_rate=16000, speed=1.0, similarity=-0.1)
        
    with pytest.raises(ValidationError, match="Invalid enhancement"):
        validate_input(text="test", model="lightning-large", sample_rate=16000, speed=1.0, enhancement=3)

def test_get_smallest_languages():
    """Tests the get_smallest_languages function."""
    assert get_smallest_languages("lightning") == TTSLanguages_lightning
    assert get_smallest_languages("lightning-large") == TTSLanguages_lightning_large
    assert get_smallest_languages("lightning-v2") == TTSLanguages_lightning_v2
    with pytest.raises(ValidationError, match="Invalid model"):
        get_smallest_languages("invalid-model")

def test_get_smallest_models():
    """Tests the get_smallest_models function."""
    assert get_smallest_models() == TTSModels