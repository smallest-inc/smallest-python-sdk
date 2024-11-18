import asyncio
from threading import Thread
from queue import Queue, Empty
from typing import AsyncGenerator, Optional, Union

from .tts import Smallest
from .exceptions import APIError
from .async_tts import AsyncSmallest
from .utils import SENTENCE_END_REGEX

class TextToAudioStream:
    def __init__(
        self,
        tts_instance: Union[Smallest, AsyncSmallest],
        queue_timeout: float = 5.0,
        max_retries: int = 3
    ):
        """
        A real-time text-to-speech processor that converts streaming text into audio output.
        Useful for applications requiring immediate audio feedback from text generation,
        such as voice assistants, live captioning, or interactive chatbots.  

        ⚠️ `add_wav_header` is disabled by default for streaming efficiency. Refer to the README for more information.  

        Features:  
        - Streams audio chunks as soon as text is available.
        - Handles both sync and async text-to-speech engines.
        - Automatically retries failed synthesis attempts.
        - Low latency between text generation and speech output.

        Args:
            tts_instance: The text-to-speech engine to use (Smallest or AsyncSmallest)
            queue_timeout: How long to wait for new text (seconds, default: 1.0)
            max_retries: Number of retry attempts for failed synthesis (default: 3)
        """
        self.tts_instance = tts_instance
        self.sentence_end_regex = SENTENCE_END_REGEX
        self.queue_timeout = queue_timeout
        self.max_retries = max_retries
        self.queue = Queue()
        self.buffer_size = 250
        self.stop_flag = False
        self.tts_instance.opts.add_wav_header = False


    async def _stream_llm_output(self, llm_output: AsyncGenerator[str, None]) -> None:
        """
        Streams the LLM output, splitting it into sentences and adding each to the queue.

        Parameters:
        - llm_output (AsyncGenerator[str, None]): An async generator yielding LLM output.
        """
        buffer = ""
        async for chunk in llm_output:
            buffer += chunk
            if self.sentence_end_regex.match(buffer) or self.buffer_size > 600:
                self.queue.put(buffer)
                buffer = ""

        if buffer:
            self.queue.put(buffer)

        self.stop_flag = True  # completion flag when LLM output ends


    async def _synthesize_async(self, sentence: str, retries: int = 0) -> Optional[bytes]:
        """Asynchronously synthesizes a given sentence."""
        try:
            return await self.tts_instance.synthesize(sentence)
        except APIError as e:
            if retries < self.max_retries:
                return await self._synthesize_async(sentence, retries + 1)
            else:
                print(f"Synthesis failed for sentence: {sentence} - Error: {e}. Retries Exhausted, for more information, visit https://waves.smallest.ai/")
                return None


    def _synthesize_sync(self, sentence: str, retries: int = 0) -> Optional[bytes]:
        """Synchronously synthesizes a given sentence."""
        try:
            return self.tts_instance.synthesize(sentence)
        except APIError as e:
            if retries < self.max_retries:
                return self._synthesize_sync(sentence, retries + 1)
            else:
                print(f"Synthesis failed for sentence: {sentence} - Error: {e}. Retries Exhausted, for more information, visit https://waves.smallest.ai/")
                return None


    async def _run_synthesis(self) -> AsyncGenerator[bytes, None]:
        """
        Continuously synthesizes sentences from the queue, yielding audio content.
        If no sentences are in the queue, it waits until new data is available or streaming is complete.
        """
        while not self.stop_flag or not self.queue.empty():
            try:
                sentence = self.queue.get(timeout=self.queue_timeout)
                if isinstance(self.tts_instance, AsyncSmallest):
                    audio_content = await self._synthesize_async(sentence)
                else:
                    loop = asyncio.get_running_loop()
                    audio_content = await loop.run_in_executor(None, self._synthesize_sync, sentence)
                
                if audio_content:
                    yield audio_content
            except Empty:
                if self.stop_flag:
                    break
                await asyncio.sleep(0.1)  # avoid busy waiting if the queue is empty


    async def process(self, llm_output: AsyncGenerator[str, None]) -> AsyncGenerator[bytes, None]:
        """
        Convert streaming text into audio in real-time.

        Handles the entire pipeline from receiving text to producing audio,
        yielding audio chunks as soon as they're ready.

        Args:
            llm_output: An async generator that yields text chunks.

        Yields:
            Raw audio data chunks (without WAV headers) that can be:
            - Played directly through an audio device
            - Saved to a file
            - Streamed over a network
            - Further processed as needed
        """
        llm_thread = Thread(target=asyncio.run, args=(self._stream_llm_output(llm_output),))
        llm_thread.start()

        async for audio_content in self._run_synthesis():
            yield audio_content

        llm_thread.join()
