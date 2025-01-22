import pytest
import re
import jiwer

from smallest.utils import (
    preprocess_text,
    chunk_text,
    get_smallest_languages,
    get_smallest_models
)


@pytest.mark.parametrize("input_text, expected_output", [
    (
        "Wow! The jubilant child, bursting with glee, $99.99     exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky. \n\n\n",
        "Wow! The jubilant child, bursting with glee, $99.99 exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow hued sky."
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


@pytest.mark.parametrize("expected_languages", [
    ['en', 'hi']
])
def test_get_smallest_languages(expected_languages):
    assert get_smallest_languages() == expected_languages

@pytest.mark.parametrize("expected_models", [
    ['lightning', 'lightning-large']
])
def test_get_smallest_models(expected_models):
    assert get_smallest_models() == expected_models