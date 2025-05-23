import pytest
import re
import jiwer

from smallestai.waves.utils import (
    preprocess_text,
    chunk_text,
    get_smallest_languages,
    get_smallest_models
)
from smallestai.waves.models import (
    TTSLanguages_lightning,
    TTSLanguages_lightning_large,
    TTSLanguages_lightning_v2,
    TTSModels
)


@pytest.mark.parametrize("input_text, expected_output", [
    (
        "Wow! The jubilant child, bursting with glee, $99.99     exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky. \n\n\n",
        "Wow! The jubilant child, bursting with glee, $99.99 exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky."
    ),
    # can add more tests here
])
def test_preprocess_text(input_text, expected_output):
    assert preprocess_text(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    (
        "Wow! The jubilant child, bursting with glee, exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky.",
        [
            "Wow! The jubilant child, bursting with glee, exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky.",
        ]
    ),
    # Add more test cases here as needed
])
def test_split_into_chunks(input_text, expected_output):
    assert chunk_text(input_text) == expected_output


@pytest.mark.parametrize("model, expected_languages", [
    ('lightning', TTSLanguages_lightning),
    ('lightning-large', TTSLanguages_lightning_large),
    ('lightning-v2', TTSLanguages_lightning_v2),
    (None, TTSLanguages_lightning),  # Test default parameter
])
def test_get_smallest_languages(model, expected_languages):
    if model is None:
        assert get_smallest_languages() == expected_languages
    else:
        assert get_smallest_languages(model) == expected_languages

@pytest.mark.parametrize("expected_models", [
    TTSModels,
])
def test_get_smallest_models(expected_models):
    assert get_smallest_models() == expected_models