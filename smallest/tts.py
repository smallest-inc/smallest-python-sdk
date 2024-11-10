import requests
from typing import Optional, Union, List, Generator, Iterable
import os
import wave

from .models import TTSModels, TTSLanguages, TTSVoices
from .exceptions import TTSError, APIError
from .utils import (TTSOptions, validate_input, preprocess_text, 
get_smallest_languages, get_smallest_voices, get_smallest_models, API_BASE_URL, SENTENCE_END_REGEX)

class Smallest:
    def __init__(
            self,
            api_key: Optional[str] = None,
            model: TTSModels = "lightning",
            sample_rate: int = 24000,
            voice: TTSVoices = "emily",
            language: TTSLanguages = "en",
            speed: Optional[float] = 1.0,
            add_wav_header: Optional[bool] = True,
            transliterate: Optional[bool] = False,
            remove_extra_silence: Optional[bool] = False
    ) -> None:
        """
        Smallest Instance for text-to-speech synthesis.

        This is a synchronous implementation of the text-to-speech functionality. 
        For an asynchronous version, please refer to the AsyncSmallest Instance.

        Parameters:
        - api_key (str): The API key for authentication, export it as 'SMALLEST_API_KEY' in your environment variables.
        - model (TTSModels): The model to be used for synthesis.
        - sample_rate (int): The sample rate for the audio output.
        - voice (TTSVoices): The voice to be used for synthesis.
        - language (TTSLanguages): The language for the synthesized speech.
        - add_wav_header (bool): Whether to add a WAV header to the output audio.
        - speed (float): The speed of the speech synthesis.
        - transliterate (bool): Whether to transliterate the text.

        Methods:
        - get_languages: Returns a list of available languages for synthesis.
        - get_voices: Returns a list of available voices for synthesis.
        - synthesize: Converts the provided text into speech and returns the audio content.
        - stream: Streams the synthesized audio synchronously in chunks.
        - stream_tts_input: Streams text-to-speech input from a generator or iterable of strings.
        """
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY")
        if not self.api_key:
            raise TTSError("API key is required")
        
        self.opts = TTSOptions(
            model=model,
            sample_rate=sample_rate,
            voice=voice,
            api_key=self.api_key,
            language=language,
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
        ) -> Union[bytes, None]:
        """
        Synthesize speech from the provided text.

        Parameters:
        - text (str): The text to be converted to speech.
        - save_as (Optional[str]): If provided, the synthesized audio will be saved to this file path. 
                                   The file must have a .wav extension.

        Returns:
        - Union[bytes, None]: The synthesized audio content in bytes if `save_as` is not specified; 
                              otherwise, returns None after saving the audio to the specified file.

        Raises:
        - TTSError: If the provided file name does not have a .wav extension when `save_as` is specified.
        - APIError: If the API request fails or returns an error.
        """
        validate_input(text, self.opts.voice, self.opts.model, self.opts.language, self.opts.sample_rate, self.opts.speed)

        payload = {
            "text": preprocess_text(text),
            "sample_rate": self.opts.sample_rate,
            "voice_id": self.opts.voice,
            "language": self.opts.language,
            "add_wav_header": self.opts.add_wav_header,
            "speed": self.opts.speed,
            "model": self.opts.model,
            "transliterate": self.opts.transliterate,
            "remove_extra_silence": self.opts.remove_extra_silence,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        res = requests.post(f"{API_BASE_URL}/{self.opts.model}/get_speech", json=payload, headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to synthesize speech: {res.text}")
        
        audio_content = res.content

        if save_as:
            if not save_as.endswith(".wav"):
                raise TTSError("Invalid file name. Extension must be .wav")
            
            if self.opts.add_wav_header:
                with open(save_as, "wb") as wf:
                    wf.write(audio_content)
            else:
                with wave.open(save_as, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(self.opts.sample_rate)
                    wf.writeframes(audio_content)
            return None
            
        return audio_content
        

    def stream_llm_output(
            self,
            text_stream: Union[Generator[str, None, None], Iterable[str]]
        ) -> Generator[bytes, None, None]:
        """
        Stream text-to-speech input from a generator or iterable of strings.

        This method processes a stream of text, synthesizing speech for complete sentences 
        and yielding audio chunks for each synthesized segment. It handles text input 
        until it encounters sentence-ending punctuation, at which point it synthesizes 
        the accumulated text into audio.

        Parameters:
        - text_stream (Generator[str, None, None] | Iterable[str]): A generator or iterable 
          containing strings of text to be converted to speech.

        Returns:
        - Generator[bytes, None, None]: A generator that yields audio chunks in bytes.

        Raises:
        - APIError: If the synthesis process fails or returns an error.
        """
        buffer = ""
        
        if self.opts.add_wav_header:
            self.opts.add_wav_header = False

        for text_chunk in text_stream:
            buffer += text_chunk

            if SENTENCE_END_REGEX.match(buffer):
                if buffer.strip():
                    audio_chunk = self.synthesize(buffer.strip())
                    yield audio_chunk
                buffer = ""

        if buffer.strip():
            audio_chunk = self.synthesize(buffer.strip())
            yield audio_chunk
