import pytest
import re
import jiwer

from smallest.utils import (
    preprocess_text,
    split_into_chunks,
    get_smallest_languages,
    get_smallest_voices,
    get_smallest_models
)


@pytest.mark.parametrize("input_text, expected_output", [
    (
        "Wow! The jubilant child, bursting with glee, $99.99     exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky. \n\n\n     वो रंग-बिरंगे गुब्बारे हवा में ऐसे झूल रहे थे जैसे एक खुशियों से \n\n 95  भरी दुनिया हो। सच में, यह एक अद्भुत और खुशी से भरा दृश्य था।",
        "Wow! The jubilant child, bursting with glee, $99.99 exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky. वो रंग-बिरंगे गुबबारे हवा में ऐसे झूल रहे थे जैसे एक खुशियों से 95 भरी दुनिया हो। सच में, यह एक अदभुत और खुशी से भरा दृशय था।"
    ),
    # can add more tests here
])
def test_preprocess_text(input_text, expected_output):
    assert preprocess_text(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    (
        "Wow! The jubilant child, bursting with glee, exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky. वो रंग बिरंगे गुब्बारे हवा में ऐसे झूल रहे थे जैसे एक खुशियों से भरी दुनिया हो। सच में, यह एक अद्भुत और खुशी से भरा दृश्य था।",
        [
            "Wow! The jubilant child, bursting with glee, exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky.",
            "वो रंग बिरंगे गुब्बारे हवा में ऐसे झूल रहे थे जैसे एक खुशियों से भरी दुनिया हो। सच में, यह एक अद्भुत और खुशी से भरा दृश्य था।"
        ]
    ),
    # Add more test cases here as needed
])
def test_split_into_chunks(input_text, expected_output):
    assert split_into_chunks(input_text) == expected_output


@pytest.mark.parametrize("expected_languages", [
    ['en', 'hi']
])
def test_get_smallest_languages(expected_languages):
    assert get_smallest_languages() == expected_languages