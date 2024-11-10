import aiohttp
from typing import Optional, Union, AsyncGenerator, Iterable, List
import os
import aiofiles

from .models import TTSModels, TTSLanguages, TTSVoices
from .exceptions import TTSError, APIError
from .utils import (TTSOptions, validate_input, preprocess_text, add_wav_header,
                     get_smallest_languages, get_smallest_voices, get_smallest_models, API_BASE_URL, SENTENCE_END_REGEX)


class AsyncSmallest:
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
        AsyncSmallest Instance for asynchronous text-to-speech synthesis.

        This class provides an asynchronous implementation of the text-to-speech functionality. 
        It allows for non-blocking synthesis of speech from text, making it suitable for applications 
        that require async processing.

        Parameters:
        - api_key (str): The API key for authentication, export it as 'SMALLEST_API_KEY' in your environment variables.  
        - model (TTSModels): The model to be used for synthesis.
        - sample_rate (int): The sample rate for the audio output.
        - voice (TTSVoices): The voice to be used for synthesis.
        - language (TTSLanguages): The language for the synthesized speech.
        - add_wav_header (bool): Whether to add a WAV header to the output audio.
        - speed (float): The speed of the speech synthesis, range is [0.5, 2.0].
        - transliterate (bool): Whether to transliterate the text.
        - remove_extra_silence (bool): Whether to remove extra silence from the synthesized audio.

        Methods:
        - get_languages: Returns a list of available languages for synthesis.
        - get_voices: Returns a list of available voices for synthesis.
        - synthesize: Asynchronously converts the provided text into speech and returns the audio content.
        - stream: Asynchronously streams the synthesized audio in chunks using websocket.
        - stream_tts_input: Asynchronously streams text-to-speech input from an async generator or iterable of strings.
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
        ) -> Union[bytes, None]:
        """
        Asynchronously synthesize speech from the provided text.

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
            "remove_extra_silence": self.opts.remove_extra_silence
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if not self.session:
            self.session = aiohttp.ClientSession()
        
        async with self.session.post(f"{API_BASE_URL}/{self.opts.model}/get_speech", json=payload, headers=headers) as res:
            if res.status != 200:
                raise APIError(f"Failed to synthesize speech: {await res.text()}")
            
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


    async def stream_llm_output(
        self,
        text_stream: AsyncGenerator[str, None] | Iterable[str],
    ) -> AsyncGenerator[bytes, None]:
        """
        Asynchronously stream text-to-speech input from an async generator or iterable of strings.  
        This method processes a stream of text, synthesizing speech for complete sentences 
        and yielding audio chunks for each synthesized segment. It handles text input 
        until it encounters sentence-ending punctuation, at which point it synthesizes 
        the accumulated text into audio.    
        Parameters:
        - text_stream (AsyncGenerator[str, None] | Iterable[str]): An async generator or iterable 
          containing strings of text to be converted to speech. 
        Yields:
        - bytes: Audio chunks in bytes. 
        Raises:
        - APIError: If the synthesis process fails or returns an error.
        """
        buffer = ""
    
        if self.opts.add_wav_header:
            self.opts.add_wav_header = False
            
        async for text_chunk in self._aiter(text_stream):
            buffer += text_chunk
    
            if SENTENCE_END_REGEX.match(buffer):
                if buffer.strip():
                    audio_chunk = await self.synthesize(buffer.strip())
                    yield audio_chunk
                buffer = ""
    
        if buffer.strip():
            audio_chunk = await self.synthesize(buffer.strip())
            yield audio_chunk


    async def _aiter(self, iterable):
        if hasattr(iterable, '__aiter__'):
            async for item in iterable:
                yield item
        else:
            for item in iterable:
                yield item
