import asyncio
import time
from threading import Thread
from queue import Queue, Empty
from typing import AsyncGenerator, Optional, Union, List, Dict, Any

from smallestai.waves.waves_client import WavesClient
from smallestai.waves.exceptions import APIError
from smallestai.waves.async_waves_client import AsyncWavesClient
from smallestai.waves.utils import SENTENCE_END_REGEX

class TextToAudioStream:
    def __init__(
        self,
        tts_instance: Union[WavesClient, AsyncWavesClient],
        queue_timeout: Optional[float] = 5.0,
        max_retries: Optional[int] = 3,
        verbose: bool = False
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
            verbose: Whether to log detailed metrics about TTS requests (default: False)
        """
        self.tts_instance = tts_instance
        self.tts_instance.opts.add_wav_header = False
        self.sentence_end_regex = SENTENCE_END_REGEX
        self.queue_timeout = queue_timeout
        self.max_retries = max_retries
        self.queue = Queue()
        self.buffer_size = 250
        self.stop_flag = False
        self.verbose = verbose
        
        # Metrics tracking
        self.request_count = 0
        self.request_logs: List[Dict[str, Any]] = []
        self.start_time = 0
        self.first_api_response_time = None
        self.end_time = 0

        if self.tts_instance.opts.model == 'lightning-large':
            self.buffer_size = 140


    async def _stream_llm_output(self, llm_output: AsyncGenerator[str, None]) -> None:
        """
        Streams the LLM output, splitting it into chunks based on sentence boundaries
        or space characters if no sentence boundary is found before reaching buffer_size.

        Parameters:
        - llm_output (AsyncGenerator[str, None]): An async generator yielding LLM output.
        """
        buffer = ""

        async for chunk in llm_output:
            buffer += chunk

            while len(buffer) > self.buffer_size:
                chunk_text = buffer[:self.buffer_size]
                last_break_index = -1

                # Find last sentence boundary using regex
                for i in range(len(chunk_text) - 1, -1, -1):
                    if self.sentence_end_regex.match(chunk_text[:i + 1]):
                        last_break_index = i
                        break

                if last_break_index == -1:
                    # Fallback to space if no sentence boundary found
                    last_space = chunk_text.rfind(' ')
                    if last_space != -1:
                        last_break_index = last_space
                    else:
                        last_break_index = self.buffer_size - 1

                # Add chunk to queue and update buffer
                self.queue.put(f'{buffer[:last_break_index + 1].replace("—", " ").strip()} ')
                buffer = buffer[last_break_index + 1:].strip()

        # Don't forget the remaining text
        if buffer:
            self.queue.put(f'{buffer.replace("—", " ").strip()} ')

        self.stop_flag = True


    def _synthesize_sync(self, sentence: str, retries: int = 0) -> Optional[bytes]:
        """Synchronously synthesizes a given sentence."""
        request_start_time = time.time()
        request_id = self.request_count + 1
        
        try:
            audio_content = self.tts_instance.synthesize(sentence)
            self.request_count += 1
            request_end_time = time.time()
            
            if self.verbose:
                request_duration = request_end_time - request_start_time
                if self.first_api_response_time is None:
                    self.first_api_response_time = time.time() - self.start_time
                
                self.request_logs.append({
                    "id": request_id,
                    "text": sentence,
                    "start_time": request_start_time - self.start_time,
                    "end_time": request_end_time - self.start_time,
                    "duration": request_duration,
                    "char_count": len(sentence),
                    "retries": retries
                })
                
            return audio_content
        except APIError as e:
            if retries < self.max_retries:
                if self.verbose:
                    print(f"Retry {retries + 1}/{self.max_retries} for request: '{sentence[:30]}...'")
                return self._synthesize_sync(sentence, retries + 1)
            else:
                if self.verbose:
                    print(f"Synthesis failed for sentence: {sentence} - Error: {e}. Retries Exhausted, for more information, visit https://waves.smallest.ai/")
                return None
            

    async def _synthesize_async(self, sentence: str, retries: int = 0) -> Optional[bytes]:
        """Asynchronously synthesizes a given sentence."""
        request_start_time = time.time()
        request_id = self.request_count + 1
        
        try:
            audio_content = await self.tts_instance.synthesize(sentence)
            self.request_count += 1
            request_end_time = time.time()
            
            if self.verbose:
                request_duration = request_end_time - request_start_time
                if self.first_api_response_time is None:
                    self.first_api_response_time = time.time() - self.start_time
                
                self.request_logs.append({
                    "id": request_id,
                    "text": sentence,
                    "start_time": request_start_time - self.start_time,
                    "end_time": request_end_time - self.start_time,
                    "duration": request_duration,
                    "char_count": len(sentence),
                    "retries": retries
                })
                
            return audio_content
        except APIError as e:
            if retries < self.max_retries:
                if self.verbose:
                    print(f"Retry {retries + 1}/{self.max_retries} for request: '{sentence[:30]}...'")
                return await self._synthesize_async(sentence, retries + 1)
            else:
                if self.verbose:
                    print(f"Synthesis failed for sentence: {sentence} - Error: {e}. Retries Exhausted, for more information, visit https://waves.smallest.ai/")
                return None


    async def _run_synthesis(self) -> AsyncGenerator[bytes, None]:
        """
        Continuously synthesizes sentences from the queue, yielding audio content.
        If no sentences are in the queue, it waits until new data is available or streaming is complete.
        """
        while not self.stop_flag or not self.queue.empty():
            try:
                sentence = self.queue.get_nowait()
                
                if isinstance(self.tts_instance, AsyncWavesClient):
                    audio_content = await self._synthesize_async(sentence)
                else:
                    loop = asyncio.get_running_loop()
                    audio_content = await loop.run_in_executor(None, self._synthesize_sync, sentence)
                
                if audio_content:
                    yield audio_content
                    
            except Empty:
                # Quick check if we should exit
                if self.stop_flag and self.queue.empty():
                    break
                    
                # Short sleep to avoid busy-waiting
                await asyncio.sleep(0.01)  # Much shorter sleep time (10ms)


    def _print_verbose_summary(self) -> None:
        """Print a summary of all metrics if verbose mode is enabled."""
        if not self.verbose:
            return
            
        total_duration = self.end_time - self.start_time
        
        print("\n" + "="*100)
        print(f"TEXT-TO-AUDIO STREAM METRICS")
        print("="*100)
        
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total requests made: {self.request_count}")
        print(f"  Time to first API response: {self.first_api_response_time:.3f}s")
        print(f"  Total processing time: {total_duration:.3f}s")
        
        # Print table header
        print("\nREQUEST DETAILS:")
        header = f"{'#':4} {'Start (s)':10} {'End (s)':10} {'Duration (s)':12} {'Characters':15} {'Text'}"
        print("\n" + header)
        print("-" * 100)
        
        # Print table rows
        for log in self.request_logs:
            row = (
                f"{log['id']:4} "
                f"{log['start_time']:10.3f} "
                f"{log['end_time']:10.3f} "
                f"{log['duration']:12.3f} "
                f"{log['char_count']:15} "
                f"{log['text'][:50]}{'...' if len(log['text']) > 50 else ''}"
            )
            print(row)
            
            # Print retry information if any
            if log['retries'] > 0:
                print(f"{'':4} {'':10} {'':10} {'':12} {'':15} Retries: {log['retries']}")
                
        print("\n" + "="*100)


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
        self.start_time = time.time()
        
        llm_thread = Thread(target=asyncio.run, args=(self._stream_llm_output(llm_output),))
        llm_thread.start()

        async for audio_content in self._run_synthesis():
            yield audio_content

        llm_thread.join()
        
        self.end_time = time.time()
        self._print_verbose_summary()