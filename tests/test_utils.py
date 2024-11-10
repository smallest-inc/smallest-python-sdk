import pytest

from smallest.utils import (
    preprocess_text,
    get_smallest_languages,
    get_smallest_voices,
    get_smallest_models
)


@pytest.mark.parametrize("input_text,expected_output", [
    (
        "Check out this amazing website: example.com! It has 10,000 unique visitors per day.\n\nAlso, the price is $99.99",
        "check out this amazing website: example dot com! it has ten thousand unique visitors per day. also, the price is $ninety-nine point nine nine"
    ),
    # can add more tests here
])
def test_preprocess_text(input_text, expected_output):
    assert preprocess_text(input_text) == expected_output


@pytest.mark.parametrize("expected_languages", [
    ['en', 'hi']
])
def test_get_smallest_languages(expected_languages):
    assert get_smallest_languages() == expected_languages


@pytest.mark.parametrize("expected_voices", [
    ["emily", "jasmine", "arman", "james", "mithali", "aravind", "raj"]
])
def test_get_smallest_voices(expected_voices):
    assert get_smallest_voices() == expected_voices


@pytest.mark.parametrize("expected_models", [
    ["lightning"]
])
def test_get_smallest_models(expected_models):
    assert get_smallest_models() == expected_models