import os
import copy
import requests
from typing import Optional, Union, List

from .models import TTSModels, TTSVoices
from .exceptions import TTSError, APIError
from .utils import (TTSOptions, validate_input, preprocess_text, 
get_smallest_languages, get_smallest_voices, get_smallest_models, API_BASE_URL)

class Smallest:
    def __init__(
            self,
            api_key: Optional[str] = None,
            model: TTSModels = "lightning",
            sample_rate: int = 24000,
            voice: TTSVoices = "emily",
            speed: Optional[float] = 1.0,
            add_wav_header: Optional[bool] = True,
            transliterate: Optional[bool] = False,
            remove_extra_silence: Optional[bool] = True
    ) -> None:
        """
        Smallest Instance for text-to-speech synthesis.

        This is a synchronous implementation of the text-to-speech functionality. 
        For an asynchronous version, please refer to the AsyncSmallest Instance.

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
        - synthesize: Converts the provided text into speech and returns the audio content.
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
            remove_extra_silence=remove_extra_silence
        )
        
    def get_languages(self) -> List[str]:
        """Returns a list of available languages."""
        return get_smallest_languages()
    
    def get_voices(self) -> List[str]:
        """Returns a list of available voices."""
        return get_smallest_voices()

    def get_models(self) -> List[str]:
        """Returns a list of available models."""
        return get_smallest_models()
    
    def synthesize(
            self,
            text: str,
            save_as: Optional[str] = None,
            **kwargs
        ) -> Union[bytes, None]:
        """
        Synthesize speech from the provided text.

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
            "remove_extra_silence": opts.remove_extra_silence,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        res = requests.post(f"{API_BASE_URL}/{opts.model}/get_speech", json=payload, headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to synthesize speech: {res.text}. Please check if you have set the correct API key. For more information, visit https://waves.smallest.ai/")
        
        audio_content = res.content

        if save_as:
            if not save_as.endswith(".wav"):
                raise TTSError("Invalid file name. Extension must be .wav")
            
            if self.opts.add_wav_header:
                with open(save_as, "wb") as wf:
                    wf.write(audio_content)
            else:
                raise TTSError("WAV header is required for saving audio. Set 'add_wav_header=True' to add a WAV header.")
            return None
            
        return audio_content
