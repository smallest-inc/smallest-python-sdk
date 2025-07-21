import os
import pytest
import pytest_asyncio
import jiwer
import re
import aiohttp
from unittest.mock import patch, Mock
from dotenv import load_dotenv

from smallestai.waves.async_waves_client import AsyncWavesClient
from smallestai.waves.exceptions import TTSError, APIError

# Load environment variables from .env file
load_dotenv()

SMALLEST_API_KEY = os.getenv("SMALLEST_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Text normalization for WER calculation
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Helper to get transcription from Deepgram
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

@pytest_asyncio.fixture
async def async_client():
    if not SMALLEST_API_KEY:
        pytest.skip("SMALLEST_API_KEY not set")
    client = AsyncWavesClient(api_key=SMALLEST_API_KEY)
    yield client

def test_async_client_initialization_no_key():
    with patch.dict(os.environ, {"SMALLEST_API_KEY": ""}):
        with pytest.raises(TTSError):
            AsyncWavesClient()

@pytest.mark.asyncio
async def test_async_synthesize_and_verify_wer(async_client):
    """Tests async synthesize method and verifies output with Deepgram ASR."""
    text = "Hello world, this is a test of the Smallest AI asynchronous text to speech client."
    
    audio_bytes = await async_client.synthesize(text=text, output_format="wav")
    
    assert audio_bytes is not None
    assert isinstance(audio_bytes, bytes)
  
    transcribed_text = await get_transcription(audio_bytes)
    
    original_normalized = normalize_text(text)
    transcribed_normalized = normalize_text(transcribed_text)
    
    wer = jiwer.wer(original_normalized, transcribed_normalized)
    
    print(f"\nOriginal: '{original_normalized}'")
    print(f"Transcribed: '{transcribed_normalized}'")
    print(f"Word Error Rate (WER): {wer}")
    
    assert wer < 0.1

@pytest.mark.asyncio
async def test_async_synthesize_invalid_kwargs(async_client):
    """Tests that async synthesize raises an error for invalid kwargs."""
    with pytest.raises(ValueError, match="Invalid parameter\\(s\\) in kwargs"):
        await async_client.synthesize("test", invalid_param="some_value")

@pytest.mark.asyncio
async def test_async_delete_voice_failure(async_client):
    """Tests async delete_voice failure case."""
    # This requires mocking the session inside the client
    await async_client._ensure_session()
    with patch.object(async_client.session, 'delete') as mock_delete:
        mock_response = Mock()
        mock_response.status = 404
        async def mock_text():
            return "Not Found"
        mock_response.text = mock_text
        mock_delete.return_value.__aenter__.return_value = mock_response

        with pytest.raises(APIError, match="Failed to delete voice"):
            await async_client.delete_voice("non_existent_voice_id")