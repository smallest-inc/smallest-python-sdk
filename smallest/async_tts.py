import os
import copy
import json
import aiohttp
import aiofiles
import requests
from typing import Optional, Union, List

from smallest.exceptions import TTSError, APIError
from smallest.utils import (TTSOptions, validate_input, preprocess_text, add_wav_header, chunk_text,
                     get_smallest_languages, get_smallest_models, API_BASE_URL)


class AsyncSmallest:
    def __init__(
        self,
        api_key: str = None,
        model: Optional[str] = "lightning",
        sample_rate: Optional[int] = 24000,
        voice_id: Optional[str] = "emily",
        speed: Optional[float] = 1.0,
        add_wav_header: Optional[bool] = True,
        transliterate: Optional[bool] = False,
        remove_extra_silence: Optional[bool] = False
    ) -> None:
        """
        AsyncSmallest Instance for asynchronous text-to-speech synthesis.

        This class provides an asynchronous implementation of the text-to-speech functionality.
        It allows for non-blocking synthesis of speech from text, making it suitable for applications
        that require async processing.

        Args:
        - api_key (str): The API key for authentication, export it as 'SMALLEST_API_KEY' in your environment variables.
        - model (TTSModels): The model to be used for synthesis.
        - sample_rate (int): The sample rate for the audio output.
        - voice_id (TTSVoices): The voice to be used for synthesis.
        - speed (float): The speed of the speech synthesis.
        - add_wav_header (bool): Whether to add a WAV header to the output audio.
        - transliterate (bool): Whether to transliterate the text.
        - remove_extra_silence (bool): Whether to remove extra silence from the synthesized audio.

        Methods:
        - get_languages: Returns a list of available languages for synthesis.
        - get_voices: Returns a list of available voices for synthesis.
        - get_models: Returns a list of available models for synthesis.
        - synthesize: Asynchronously converts the provided text into speech and returns the audio content.
        """
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY")
        if not self.api_key:
            raise TTSError()
        self.chunk_size = 250

        self.opts = TTSOptions(
            model=model,
            sample_rate=sample_rate,
            voice_id=voice_id,
            api_key=self.api_key,
            add_wav_header=add_wav_header,
            speed=speed,
            transliterate=transliterate,
            remove_extra_silence=remove_extra_silence,
        )
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
    

    def get_languages(self) -> List[str]:
        """Returns a list of available languages."""
        return get_smallest_languages()

    def get_cloned_voices(self) -> str:
        """Returns a list of your cloned voices."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/lightning-large/get_cloned_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get cloned voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)
    

    def get_voices(
            self,
            model: Optional[str] = "lightning"
        ) -> str:
        """Returns a list of available voices."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/{model}/get_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)


    def get_models(self) -> List[str]:
        """Returns a list of available models."""
        return get_smallest_models()


    async def synthesize(
            self,
            text: str,
            save_as: Optional[str] = None,
            **kwargs
        ) -> Union[bytes, None]:
        """
        Asynchronously synthesize speech from the provided text.

        Args:
        - text (str): The text to be converted to speech.
        - save_as (Optional[str]): If provided, the synthesized audio will be saved to this file path.
                                   The file must have a .wav extension.
        - kwargs: Additional optional parameters to override `__init__` options for this call.

        Returns:
        - Union[bytes, None]: The synthesized audio content in bytes if `save_as` is not specified;
                              otherwise, returns None after saving the audio to the specified file.

        Raises:
        - TTSError: If the provided file name does not have a .wav extension when `save_as` is specified.
        - APIError: If the API request fails or returns an error.
        """
        should_cleanup = await self._ensure_session()

        try:
            opts = copy.deepcopy(self.opts)
            for key, value in kwargs.items():
                setattr(opts, key, value)

            validate_input(preprocess_text(text), opts.model, opts.sample_rate, opts.speed)

            self.chunk_size = 250
            if opts.model == 'ligtning-large':
                self.chunk_size = 140

            chunks = chunk_text(text, self.chunk_size)
            audio_content = b""

            for chunk in chunks:
                payload = {
                    "text": preprocess_text(chunk),
                    "sample_rate": opts.sample_rate,
                    "voice_id": opts.voice_id,
                    "add_wav_header": False,
                    "speed": opts.speed,
                    "model": opts.model,
                    "transliterate": opts.transliterate,
                    "remove_extra_silence": opts.remove_extra_silence
                }

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                if not self.session:
                    self.session = aiohttp.ClientSession()

                async with self.session.post(f"{API_BASE_URL}/{opts.model}/get_speech", json=payload, headers=headers) as res:
                    if res.status != 200:
                        raise APIError(f"Failed to synthesize speech: {await res.text()}. For more information, visit https://waves.smallest.ai/")

                    audio_content += await res.read()

            if save_as:
                if not save_as.endswith(".wav"):
                    raise TTSError("Invalid file name. Extension must be .wav")

                async with aiofiles.open(save_as, mode='wb') as f:
                    await f.write(add_wav_header(audio_content, opts.sample_rate))

                return None

            if opts.add_wav_header:
                return add_wav_header(audio_content, opts.sample_rate)

            return audio_content
        
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None


    async def add_voice(self, display_name: str, file_path: str) -> str:
        """
        Instantly clone your voice asynchronously.

        Args:
        - display_name (str): The display name for the new voice.
        - file_path (str): The path to the reference audio file to be cloned.

        Returns:
        - str: The response from the API as a formatted JSON string.

        Raises:
        - TTSError: If the file does not exist or is not a valid audio file.
        - APIError: If the API request fails or returns an error.
        """
        url = f"{API_BASE_URL}/lightning-large/add_voice"

        if not os.path.exists(file_path):
            raise TTSError("Invalid file path. File does not exist.")

        ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav']
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
            raise TTSError(f"Invalid file type. Supported formats are: {ALLOWED_AUDIO_EXTENSIONS}")

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

                return json.dumps(await res.json(), indent=4, ensure_ascii=False)
        
        finally:
            if should_cleanup and self.session:
                await self.session.close()
                self.session = None

