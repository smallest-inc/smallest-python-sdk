import os
import copy
import aiohttp
import aiofiles
from typing import Optional, Union, List

from .models import TTSModels, TTSVoices
from .exceptions import TTSError, APIError
from .utils import (TTSOptions, validate_input, preprocess_text, add_wav_header,
                     get_smallest_languages, get_smallest_voices, get_smallest_models, API_BASE_URL)


class AsyncSmallest:
    def __init__(
            self,
            api_key: Optional[str] = None,
            model: TTSModels = "lightning",
            sample_rate: int = 24000,
            voice: TTSVoices = "emily",
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
        - voice (TTSVoices): The voice to be used for synthesis.
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
            raise TTSError("API key is required")
        
        self.opts = TTSOptions(
            model=model,
            sample_rate=sample_rate,
            voice=voice,
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

    def get_languages(self) -> List[str]:
        """Returns a list of available languages."""
        return get_smallest_languages()
    
    def get_voices(self) -> List[str]:
        """Returns a list of available voices."""
        return get_smallest_voices()

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
        opts = copy.deepcopy(self.opts)
        for key, value in kwargs.items():
            setattr(opts, key, value)

        validate_input(text, opts.voice, opts.model, opts.sample_rate, opts.speed)

        payload = {
            "text": preprocess_text(text),
            "sample_rate": opts.sample_rate,
            "voice_id": opts.voice,
            "add_wav_header": opts.add_wav_header,
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
            
            audio_content = await res.read()

        if save_as:
            if not save_as.endswith(".wav"):
                raise TTSError("Invalid file name. Extension must be .wav")
            
            if self.opts.add_wav_header:
                async with aiofiles.open(save_as, mode='wb') as f:
                    await f.write(audio_content)
            else:
                async with aiofiles.open(save_as, mode='wb') as f:
                    await f.write(add_wav_header(audio_content, self.opts.sample_rate))
            return None

        return audio_content
