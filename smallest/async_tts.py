import aiohttp
from typing import Optional, Union, List, AsyncGenerator
import io
import os
import aiofiles

from .models import TTSModels, TTSLanguages, TTSVoices
from .exceptions import TTSError, APIError
from .utils import (TTSOptions, validate_input, preprocess_text, add_wav_header,
                    waves_streaming, get_smallest_languages, get_smallest_voices, get_smallest_models, API_BASE_URL, SENTENCE_END_REGEX)


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
        - api_key (str): The API key for authentication.
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
            async with aiofiles.open(save_as, mode='wb') as f:
                await f.write(add_wav_header(audio_content))
            return None
        
        if self.opts.add_wav_header:
            audio_content = add_wav_header(audio_content, self.opts.sample_rate)

        return audio_content
        
    async def stream(
        self,
        text: str,
        keep_ws_open: Optional[bool] = True,
        get_end_of_response_token: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        """
        Asynchronously stream synthesized audio using websockets.

        Parameters:
        - text (str): The text to be converted to speech.
        - keep_ws_open (bool): If True, the websocket connection will be kept open after the synthesis process.
        - get_end_of_response_token (bool): If True, the generator will yield a token indicating the end of the response.

        Yields:
        - bytes: Audio chunks in bytes with WAV header included.

        Raises:
        - APIError: If the synthesis process fails or returns an error.
        - TTSError: If the input validation fails.
        """
        validate_input(text, self.opts.voice, self.opts.model, self.opts.language, self.opts.sample_rate, self.opts.speed)

        websocket_url = f"wss://waves-api.smallest.ai/api/v1/{self.opts.model}/get_streaming_speech?token={self.api_key}"

        payload = [{
            "text": preprocess_text(text),
            "sample_rate": self.opts.sample_rate,
            "voice_id": self.opts.voice,
            "language": self.opts.language,
            "add_wav_header": self.opts.add_wav_header,
            "speed": self.opts.speed,
            "keep_ws_open": keep_ws_open,
            "remove_extra_silence": self.opts.remove_extra_silence,
            "transliterate": self.opts.transliterate,
            "get_end_of_response_token": get_end_of_response_token
        }]

        headers = {
            "origin": "https://smallest.ai",
        }

        wav_audio_bytes = await waves_streaming(url=websocket_url, payloads=payload, headers=headers)
    
        if wav_audio_bytes is None:
            raise APIError("Failed to stream audio. Please check your API token and connection.")
            
        if self.opts.add_wav_header:
            wav_audio_bytes = add_wav_header(frame_input=wav_audio_bytes, sample_rate=self.opts.sample_rate)
        
        yield wav_audio_bytes

    async def stream_tts_input(
            self,
            text_stream
        ):
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
        buffer = io.StringIO()
        async for text in self._aiter(text_stream):
            text = preprocess_text(text)
            if text:
                buffer.write(text + " ")
                if SENTENCE_END_REGEX.search(text):
                    full_text = buffer.getvalue().strip()
                    audio_chunk = await self.synthesize(full_text)
                    yield audio_chunk
                    buffer = io.StringIO()
        
        # If there's remaining text in the buffer after streaming ends
        if buffer.tell() > 0:
            full_text = buffer.getvalue()
            full_text = preprocess_text(full_text)
            audio_chunk = await self.synthesize(buffer)
            yield audio_chunk


    async def _aiter(self, iterable):
        if hasattr(iterable, '__aiter__'):
            async for item in iterable:
                yield item
        else:
            for item in iterable:
                yield item
