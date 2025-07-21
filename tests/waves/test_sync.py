import os
import pytest
import jiwer
import re
import aiohttp
from unittest.mock import patch, Mock
from dotenv import load_dotenv

from smallestai.waves.waves_client import WavesClient
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

@pytest.fixture
def client():
    if not SMALLEST_API_KEY:
        pytest.skip("SMALLEST_API_KEY not set")
    return WavesClient(api_key=SMALLEST_API_KEY)

def test_client_initialization_no_key():
    with patch.dict(os.environ, {"SMALLEST_API_KEY": ""}):
        with pytest.raises(TTSError):
            WavesClient()

@pytest.mark.asyncio
async def test_synthesize_and_verify_wer(client):
    """Tests synthesize method and verifies output with Deepgram ASR."""
    text = "Hello world, this is a test of the Smallest AI text to speech API."
    
    audio_bytes = client.synthesize(text=text, output_format="wav")
    
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

def test_synthesize_invalid_kwargs(client):
    """Tests that synthesize raises an error for invalid kwargs."""
    with pytest.raises(ValueError, match="Invalid parameter\\(s\\) in kwargs"):
        client.synthesize("test", invalid_param="some_value")

@patch('requests.request')
def test_get_voices(mock_request, client):
    """Tests get_voices method with a mock."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"voices": ["emily", "lakshya"]}
    mock_request.return_value = mock_response
    
    voices = client.get_voices()
    assert '"emily"' in voices
    mock_request.assert_called_once()

@patch('requests.post')
def test_add_voice_failure(mock_post, client):
    """Tests add_voice failure case."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response
    
    with pytest.raises(APIError, match="Failed to add voice"):
        # Use a dummy file path as it won't be accessed due to the mock
        with open('dummy.wav', 'w') as f: f.write('dummy')
        client.add_voice("test_voice", "dummy.wav")
        os.remove('dummy.wav')

@patch('requests.delete')
def test_delete_voice(mock_delete, client):
    """Tests delete_voice method with a mock."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_delete.return_value = mock_response
    
    response = client.delete_voice("some_voice_id")
    assert '"ok"' in response
    mock_delete.assert_called_once()