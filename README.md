![linkedin 1 2-100](https://github.com/user-attachments/assets/973cf19f-25bc-4357-8243-1a34967613f4)

<div align="center">
  <a href="https://twitter.com/smallest_AI">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/smallest_AI.svg?style=social&label=Follow%20smallest_AI" alt="Twitter">
  </a>
  <a href="https://discord.gg/ywShEyXHBW">
    <img src="https://dcbadge.vercel.app/api/server/ywShEyXHBW?style=flat" alt="Discord">
  </a>
  <a href="https://www.linkedin.com/company/smallest">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-blue" alt="Linkedin">
  </a>
  <a href="https://www.youtube.com/@smallest_ai">
    <img src="https://img.shields.io/static/v1?message=smallest_ai&logo=youtube&label=&color=FF0000&logoColor=white&labelColor=&style=for-the-badge" height=20 alt="Youtube">
  </a>
</div> 

## Official Python Client for Smallest AI API   

Smallest AI builds ultra-realistic, high-speed multi-lingual voice models tailored for real-time applications, achieving hyper-realistic audio generation in as fast as ~100 milliseconds for 10 seconds of audio. With this sdk, you can easily convert text into high-quality audio with humanlike expressiveness.

Currently, the library supports direct synthesis, real-time streaming, and the ability to synthesize streamed LLM output (experimental), both synchronously and asynchronously.  

## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
  - [Sync](#sync)
  - [Async](#async)
  - [Common Methods](#common-methods)

## Installation

To install the package, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/smallest-inc/smallest-python.git
   ```

2. Navigate to the cloned directory and install the package:
   ```bash
   cd smallest-python
   pip install .
   ```   
  

> Note ⚠️: The `stream_llm_output` function can only save audio using the wave package. This is because the WAV header must be added while writing to the file, not beforehand. Therefore, in this function, `add_wav_header` is set to `False` by default.


## Examples

### Sync

**Synthesize**

```python
import os
from smallest.tts import Smallest

def main():
    client = Smallest(api_key=os.environ.get("SMALLEST_API_KEY"))
    audio_data = client.synthesize("Hello, this is a test for sync synthesis function.")
    with open("sync_synthesize.wav", "wb") as f:
        f.write(audio_data)

if __name__ == "__main__":
    main()
```  

**Synthesize streamed LLM Output**

```python
import os
from groq import Groq
from smallest import Smallest
import wave

# Initialize any LLM client and TTS system
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tts = Smallest(api_key=os.environ.get("SMALLEST_API_KEY"))

def generate_text(prompt: str = "Tell me a very short story about a wise owl."):
    """Async generator for streaming text from Groq, you can use any other provider."""
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        stream=True,
    )

    for chunk in completion:
        text = chunk.choices[0].delta.content
        if text is not None:
            yield text

def save_audio_stream(audio_chunks, filename: str, sample_rate: int = 24000):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  
        wf.setsampwidth(2) 
        wf.setframerate(sample_rate)
        for chunk in audio_chunks:
            wf.writeframes(chunk)

def main():
    # Get text stream from LLM
    text_generator = generate_text()

    # Get audio chunks from the streaming TTS
    audio_chunks = tts.stream_llm_output(text_stream=text_generator)

    # Save the audio chunks to a WAV file
    save_audio_stream(audio_chunks, "output_llm_stream.wav")


if __name__ == "__main__":
    main()
```

### Async

**Synthesize**

```python
import os
import asyncio
import aiofiles
from smallest.async_tts import AsyncSmallest

client = AsyncSmallest(api_key=os.environ.get("SMALLEST_API_KEY"))

async def main():
    async with client as tts:
        audio_bytes = await tts.synthesize("Hello, this is a test of the async synthesis function.")
        async with aiofiles.open("async_synthesize.wav", "wb") as f:
            await f.write(audio_bytes)

if __name__ == "__main__":
    asyncio.run(main())
```

**Synthesize streamed LLM Output**
```python
import os
from groq import Groq
from smallest import AsyncSmallest
import wave
import asyncio

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tts_client = Smallest(api_key=os.environ.get("SMALLEST_API_KEY"))

async def generate_text(prompt: str = "Tell me a very short story about a wise owl."):
    """Async generator for streaming text from Groq, you can use any other provider."""
    completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        stream=True,
    )

    for chunk in completion:
        text = chunk.choices[0].delta.content
        if text is not None:
            yield text

async def save_audio_stream(audio_chunks, filename: str, sample_rate: int = 24000):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        async for chunk in audio_chunks:
            wf.writeframes(chunk)

async def main():
    async with tts_client as tts:
        # Get text stream from LLM
        text_generator = generate_text()

        # Get audio chunks from the streaming TTS
        audio_chunks = tts.stream_llm_output(text_stream=text_generator)

        # Save the audio chunks to a WAV file
        await save_audio_stream(audio_chunks, "output_llm_stream_async.wav")

if __name__ == "__main__":
    asyncio.run(main())
```

### Common Methods

```python
from smallest.tts import Smallest

client = Smallest()

print(f"Avalaible Languages: {client.get_languages()}")
print(f"Available Voices: {client.get_voices()}")
print(f"Available Models: {client.get_models()}")
```
