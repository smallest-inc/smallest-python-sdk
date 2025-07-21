import os
import pytest
import jiwer
import re
import aiohttp
import wave
from io import BytesIO
from dotenv import load_dotenv

from smallestai.waves.stream_tts import TTSConfig, WavesStreamingTTS

# Load environment variables from .env file
load_dotenv()
SMALLEST_API_KEY = os.getenv("SMALLEST_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

async def get_transcription(audio_bytes: bytes) -> str:
    if not DEEPGRAM_API_KEY:
        pytest.skip("DEEPGRAM_API_KEY not set")
        
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"
    headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}", "Content-Type": "audio/wav"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=audio_bytes) as response:
            response.raise_for_status()
            res_json = await response.json()
            return res_json["results"]["channels"][0]["alternatives"][0]["transcript"]

@pytest.fixture
def streaming_tts():
    if not SMALLEST_API_KEY:
        pytest.skip("SMALLEST_API_KEY not set")
    config = TTSConfig(
        voice_id="aditi",
        api_key=SMALLEST_API_KEY,
        sample_rate=24000,
        speed=1.0,
        max_buffer_flush_ms=100
    )
    return WavesStreamingTTS(config)

@pytest.mark.asyncio
async def test_synthesize_and_verify_wer(streaming_tts):
    text = "Hello world, this is a test of the Smallest AI streaming TTS SDK."
    audio_chunks = []
    for chunk in streaming_tts.synthesize(text):
        assert isinstance(chunk, bytes)
        audio_chunks.append(chunk)
    assert len(audio_chunks) > 0

    # Convert PCM to WAV for Deepgram
    buffer = BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(b''.join(audio_chunks))
    wav_bytes = buffer.getvalue()

    transcribed_text = await get_transcription(wav_bytes)
    original_normalized = normalize_text(text)
    transcribed_normalized = normalize_text(transcribed_text)
    wer = jiwer.wer(original_normalized, transcribed_normalized)
    print(f"\nOriginal: '{original_normalized}'")
    print(f"Transcribed: '{transcribed_normalized}'")
    print(f"Word Error Rate (WER): {wer}")
    assert wer < 0.1

@pytest.mark.asyncio
async def test_synthesize_streaming_and_verify_wer(streaming_tts):
    text = "Streaming synthesis with chunked text input for Smallest SDK."
    def text_stream():
        for word in text.split():
            yield word + " "
    audio_chunks = []
    for chunk in streaming_tts.synthesize_streaming(text_stream()):
        assert isinstance(chunk, bytes)
        audio_chunks.append(chunk)
    assert len(audio_chunks) > 0

    buffer = BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(b''.join(audio_chunks))
    wav_bytes = buffer.getvalue()

    transcribed_text = await get_transcription(wav_bytes)
    original_normalized = normalize_text(text)
    transcribed_normalized = normalize_text(transcribed_text)
    wer = jiwer.wer(original_normalized, transcribed_normalized)
    print(f"\nOriginal: '{original_normalized}'")
    print(f"Transcribed: '{transcribed_normalized}'")
    print(f"Word Error Rate (WER): {wer}")
    assert wer < 0.1