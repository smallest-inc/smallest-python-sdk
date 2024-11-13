![image](https://i.imgur.com/TJ2tT4g.png)   


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

Smallest AI builds high-speed multi-lingual voice models tailored for real-time applications, achieving ultra-realistic audio generation in as fast as ~100 milliseconds for 10 seconds of audio. With this sdk, you can easily convert text into high-quality audio with humanlike expressiveness.

Currently, the library supports direct synthesis and the ability to synthesize streamed LLM output, both synchronously and asynchronously.  

## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
  - [Sync](#sync)
  - [Async](#async)
  - [LLM to Speech](#llm-to-speech)
  - [Common Methods](#common-methods)
  - [Technical Note: WAV Headers in Streaming Audio](#technical-note-wav-headers-in-streaming-audio)

## Installation

To install the package, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/smallest-inc/smallest-python-sdk.git
   ```

2. Navigate to the cloned directory and install the package:
   ```bash
   cd smallest-python
   pip install .
   ```    

## Examples

### Sync  

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

### Async  

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

### LLM to Speech  

```python
import wave
import asyncio
from groq import Groq
from smallest.tts import Smallest
from smallest.stream_tts import TextToAudioStream

llm = Groq()
tts = Smallest()

async def generate_text(prompt: str = "explain text to speech like i am five in 5 sentences"):
    """Async generator for streaming text from Groq. You can use any LLM"""
    completion = llm.chat.completions.create(
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

async def save_audio_to_wav(file_path, processor, llm_output):
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2) 
        wav_file.setframerate(24000)
        
        async for audio_chunk in processor.process(llm_output):
            wav_file.writeframes(audio_chunk)

async def main():
    # Initialize the TTS processor with the TTS instance
    processor = TextToAudioStream(tts_instance=tts)
    
    # Generate text asynchronously and process it
    llm_output = generate_text("explain text to speech like i am five in 5 sentences in fun way")
    
    # As an example, save the generated audio to a WAV file.
    await save_audio_to_wav("llm_to_speech.wav", processor, llm_output)

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

### Technical Note: WAV Headers in Streaming Audio

When implementing audio streaming with chunks of synthesized speech, WAV headers are omitted from individual chunks because:

#### Technical Issues
- Each WAV header (44 bytes) contains metadata about the entire audio file.
- Multiple headers would make chunks appear as separate audio files and add redundancy.
- Headers contain file-specific data (like total size) that's invalid for chunks.
- Sequential playback of chunks with headers causes audio artifacts (pop sounds) when concatenating or playing audio sequentially.
- Audio players would try to reinitialize audio settings for each chunk.

### Best Practices
1. Stream raw PCM audio data without headers
2. Add a single WAV header only when:
   - Saving the complete stream to a file
   - Initializing the audio playback system
   - Converting the stream to a standard audio format
