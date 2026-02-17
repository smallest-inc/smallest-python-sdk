from smallestai.waves.waves_client import WavesClient
from smallestai.waves.async_waves_client import AsyncWavesClient
from smallestai.waves.stream_tts import WavesStreamingTTS, TTSConfig

# Backwards-compatible alias for the renamed class (see issue #46)
TextToAudioStream = WavesStreamingTTS

__all__ = ["WavesClient", "AsyncWavesClient", "WavesStreamingTTS", "TTSConfig", "TextToAudioStream"]
