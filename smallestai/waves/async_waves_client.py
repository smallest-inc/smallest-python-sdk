import os
import json
import aiohttp
import aiofiles
import requests
from typing import Optional, List

from smallestai.waves.exceptions import InvalidError, APIError
from smallestai.waves.utils import (validate_tts_input, validate_stt_input,
                     get_smallest_languages, get_tts_models, get_stt_models, ALLOWED_AUDIO_EXTENSIONS, API_BASE_URL,
                     DEFAULT_SAMPLE_RATES)


class AsyncWavesClient:
    def __init__(self, api_key: str = None) -> None:
        """
        Asynchronous Waves Client for Text-to-Speech and Speech-to-Text.

        Args:
        - api_key (str): The API key for authentication.
                         Set via parameter or 'SMALLEST_API_KEY' environment variable.

        Methods:
        - synthesize: Async text to speech.
        - transcribe: Async speech to text.
        - get_languages: Returns available languages for a model.
        - get_voices: Returns available voices for a model.
        - get_models: Returns available TTS models.
        """
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY")
        if not self.api_key:
            raise InvalidError()
        self.session = None

    async def __aenter__(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _ensure_session(self):
        """Ensure session exists for direct calls"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            return True
        return False

    def get_languages(self, model: str = "lightning-v3.1") -> List[str]:
        """Returns a list of available languages for a model (TTS or STT)."""
        return get_smallest_languages(model)

    def get_cloned_voices(self) -> str:
        """Returns a list of your cloned voices."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/lightning-large/get_cloned_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get cloned voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)

    def get_voices(self, model: str = "lightning-v3.1") -> str:
        """Returns a list of available voices for a TTS model."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/{model}/get_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)

    def get_tts_models(self) -> List[str]:
        """Returns a list of available TTS models."""
        return get_tts_models()

    def get_stt_models(self) -> List[str]:
        """Returns a list of available STT models."""
        return get_stt_models()

    async def synthesize(
            self,
            text: str,
            model: str = "lightning-v3.1",
            voice_id: Optional[str] = None,
            sample_rate: Optional[int] = None,
            speed: float = 1.0,
            language: str = "en",
            output_format: str = "wav",
            consistency: Optional[float] = 0.5,
            similarity: Optional[float] = 0.0,
            enhancement: Optional[int] = 1,
            pronunciation_dicts: Optional[List[str]] = None
        ) -> bytes:
        """
        Async synthesize speech from text.

        Args:
        - text (str): The text to convert to speech.
        - model (str): TTS model. Options: "lightning-v3.1", "lightning-v2". Default: "lightning-v3.1".
        - voice_id (str): Voice ID. Default: "sophia" for v3.1, "alice" for v2.
        - sample_rate (int): Sample rate in Hz. Default: 44100 for v3.1, 24000 for v2.
        - speed (float): Speech speed (0.5-2.0). Default: 1.0.
        - language (str): Language code. Default: "en".
        - output_format (str): Output format ("pcm", "mp3", "wav", "mulaw"). Default: "wav".
        - consistency (float): Word repetition control (0-1). Only for lightning-v2. Default: 0.5.
        - similarity (float): Reference audio similarity (0-1). Only for lightning-v2. Default: 0.0.
        - enhancement (int): Quality enhancement (0-2). Only for lightning-v2. Default: 1.
        - pronunciation_dicts (List[str]): Pronunciation dictionary IDs. Default: None.

        Returns:
        - bytes: The synthesized audio content.

        Raises:
        - ValidationError: If input parameters are invalid.
        - APIError: If the API request fails.
        """
        if sample_rate is None:
            sample_rate = DEFAULT_SAMPLE_RATES.get(model, 24000)
        
        if voice_id is None:
            voice_id = "sophia" if model == "lightning-v3.1" else "alice"

        validate_tts_input(text, model, sample_rate, speed, consistency, similarity, enhancement)

        should_cleanup = False
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
            should_cleanup = True

        try:
            payload = {
                "text": text,
                "voice_id": voice_id,
                "sample_rate": sample_rate,
                "speed": speed,
                "language": language,
                "output_format": output_format
            }
            
            if model == "lightning-v2":
                if consistency is not None:
                    payload["consistency"] = consistency
                if similarity is not None:
                    payload["similarity"] = similarity
                if enhancement is not None:
                    payload["enhancement"] = enhancement
            
            if pronunciation_dicts:
                payload["pronunciation_dicts"] = pronunciation_dicts
                    
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            async with self.session.post(f"{API_BASE_URL}/{model}/get_speech", json=payload, headers=headers) as res:
                if res.status != 200:
                    raise APIError(f"Failed to synthesize speech: {await res.text()}. For more information, visit https://waves.smallest.ai/")
                
                audio_bytes = await res.content.read()  

            return audio_bytes
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None

    async def add_voice(self, display_name: str, file_path: str) -> str:
        """
        Clone a voice from an audio file.

        Args:
        - display_name (str): Display name for the new voice.
        - file_path (str): Path to the reference audio file.

        Returns:
        - str: API response as JSON.

        Raises:
        - InvalidError: If the file is invalid.
        - APIError: If the API request fails.
        """
        url = f"{API_BASE_URL}/lightning-large/add_voice"

        if not os.path.exists(file_path):
            raise InvalidError("Invalid file path. File does not exist.")

        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
            raise InvalidError(f"Invalid file type. Supported formats are: {ALLOWED_AUDIO_EXTENSIONS}")

        headers = {
            'Authorization': f"Bearer {self.api_key}",
        }

        should_cleanup = await self._ensure_session()

        try:
            async with aiofiles.open(file_path, 'rb') as f:
                file_data = await f.read()

            data = aiohttp.FormData()
            content_type = file_extension[1:]
            
            data.add_field('displayName', display_name)
            data.add_field('file', file_data, filename=file_path, content_type=f"audio/{content_type}")

            async with self.session.post(url, headers=headers, data=data) as res:
                if res.status != 200:
                    raise APIError(f"Failed to add voice: {await res.text()}. For more information, visit https://waves.smallest.ai/")

                return await res.json()
        
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None

    async def delete_voice(self, voice_id: str) -> str:
        """
        Delete a cloned voice.

        Args:
        - voice_id (str): The voice ID to delete.

        Returns:
        - str: API response.

        Raises:
        - APIError: If the API request fails.
        """
        url = f"{API_BASE_URL}/lightning-large"
        payload = {'voiceId': voice_id}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        should_cleanup = await self._ensure_session()

        try:
            async with self.session.delete(url, headers=headers, json=payload) as res:
                if res.status != 200:
                    raise APIError(f"Failed to delete voice: {await res.text()}. For more information, visit https://waves.smallest.ai/")

                return await res.json()
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None
                
    async def transcribe(
        self,
        file_path: str,
        language: str = "en",
        word_timestamps: bool = False,
        diarize: bool = False,
        age_detection: bool = False,
        gender_detection: bool = False,
        emotion_detection: bool = False,
        model: str = "pulse"
    ) -> dict:
        """
        Async transcribe audio from a file.

        Args:
        - file_path (str): Path to the audio file.
        - language (str): Language code. Use "multi" for auto-detection. Default: "en".
        - word_timestamps (bool): Include word-level timestamps. Default: False.
        - diarize (bool): Enable speaker diarization. Default: False.
        - age_detection (bool): Predict speaker age. Default: False.
        - gender_detection (bool): Predict speaker gender. Default: False.
        - emotion_detection (bool): Predict speaker emotion. Default: False.
        - model (str): STT model. Default: "pulse".

        Returns:
        - dict: Transcription result.

        Raises:
        - ValidationError: If inputs are invalid.
        - APIError: If the API request fails.
        """
        validate_stt_input(file_path, model, language)

        params = {
            'model': model,
            'language': language,
            'word_timestamps': str(bool(word_timestamps)).lower(),
            'diarize': str(bool(diarize)).lower(),
            'age_detection': str(bool(age_detection)).lower(),
            'gender_detection': str(bool(gender_detection)).lower(),
            'emotion_detection': str(bool(emotion_detection)).lower()
        }

        url = f"{API_BASE_URL}/pulse/get_text"

        should_cleanup = await self._ensure_session()

        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            content_type = f"audio/{file_extension[1:]}" if file_extension else "application/octet-stream"

            async with aiofiles.open(file_path, 'rb') as f:
                file_data = await f.read()

            headers = {
                'Authorization': f"Bearer {self.api_key}",
                'Content-Type': content_type
            }

            async with self.session.post(url, headers=headers, params=params, data=file_data) as res:
                if res.status != 200:
                    raise APIError(
                        f"Failed to transcribe audio: {await res.text()}. "
                        "For more information, visit https://waves-docs.smallest.ai/"
                    )
                return await res.json()
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None
