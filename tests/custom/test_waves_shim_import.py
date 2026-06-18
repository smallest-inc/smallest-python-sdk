"""Regression test for the 4.3.1 compatibility shim.

`from smallestai.waves import WavesStreamingTTS, TTSConfig` regressed
between 4.3.1 and 4.3.9 during the Fern migration. This test guards
against the same break recurring if Fern regen rewrites
`src/smallestai/waves/__init__.py` and drops the manual lazy-import
entries protected by `.fernignore`.
"""


def test_legacy_waves_imports_work() -> None:
    from smallestai.waves import TTSConfig, WavesStreamingTTS

    config = TTSConfig(voice_id="magnus", api_key="test-key")
    assert isinstance(WavesStreamingTTS(config), WavesStreamingTTS)


def test_tts_config_accepts_pronunciation_dicts() -> None:
    from smallestai.waves import TTSConfig

    config = TTSConfig(
        voice_id="magnus",
        api_key="test-key",
        pronunciation_dicts=["dict_abc", "dict_def"],
    )
    assert config.pronunciation_dicts == ["dict_abc", "dict_def"]


def test_tts_config_rejects_v2_only_consistency_param() -> None:
    import pytest

    from smallestai.waves import TTSConfig

    with pytest.raises(TypeError):
        TTSConfig(voice_id="magnus", api_key="test-key", consistency=0.5)  # type: ignore[call-arg]
