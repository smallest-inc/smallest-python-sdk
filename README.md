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
- [Get the API Key](#get-the-api-key)
- [Examples](#examples)
  - [Sync](#sync)
  - [Async](#async)
  - [LLM to Speech](#llm-to-speech)
- [Available Methods](#available-methods)
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

## Get the API Key  

1. Visit [waves.smallest.ai](https://waves.smallest.ai/) and sign up for an account or log in if you already have an account.  
2. Navigate to `API Key` tab in your account dashboard.
3. Create a new API Key and copy it.
4. Export the API Key in your environment with the name `SMALLEST_API_KEY`, ensuring that your application can access it securely for authentication.

## Examples

### Sync  
A synchronous text-to-speech synthesis client. 

**Basic Usage:**   
```python
import os
from smallest import Smallest

def main():
    client = Smallest(api_key=os.environ.get("SMALLEST_API_KEY"))
    audio_data = client.synthesize("Hello, this is a test for sync synthesis function.")
    with open("sync_synthesize.wav", "wb") as f:
        f.write(audio_data)

if __name__ == "__main__":
    main()
```

**Parameters:**   
- `api_key`: Your API key (can be set via SMALLEST_API_KEY environment variable)
- `model`: TTS model to use (default: "lightning")
- `sample_rate`: Audio sample rate (default: 24000)
- `voice`: Voice ID (default: "emily")
- `speed`: Speech speed multiplier (default: 1.0)
- `add_wav_header`: Include WAV header in output (default: True)
- `transliterate`: Enable text transliteration (default: False)
- `remove_extra_silence`: Remove additional silence (default: True)

### Async   
A synchronous text-to-speech synthesis client.    

**Basic Usage:**   
```python
import os
import asyncio
import aiofiles
from smallest import AsyncSmallest

client = AsyncSmallest(api_key=os.environ.get("SMALLEST_API_KEY"))

async def main():
    async with client as tts:
        audio_bytes = await tts.synthesize("Hello, this is a test of the async synthesis function.")
        async with aiofiles.open("async_synthesize.wav", "wb") as f:
            await f.write(audio_bytes)

if __name__ == "__main__":
    asyncio.run(main())
```

**Parameters:**    
- `api_key`: Your API key (can be set via SMALLEST_API_KEY environment variable)
- `model`: TTS model to use (default: "lightning")
- `sample_rate`: Audio sample rate (default: 24000)
- `voice`: Voice ID (default: "emily")
- `speed`: Speech speed multiplier (default: 1.0)
- `add_wav_header`: Include WAV header in output (default: True)
- `transliterate`: Enable text transliteration (default: False)
- `remove_extra_silence`: Remove additional silence (default: True)

### LLM to Speech    

The `TextToAudioStream` class provides real-time text-to-speech processing, converting streaming text into audio output with minimal latency. It's particularly useful for applications like voice assistants, live captioning, or interactive chatbots that require immediate audio feedback from text generation. Supports both synchronous and asynchronous TTS instance.

```python
import os
import wave
import asyncio
from groq import Groq
from smallest import Smallest
from smallest import TextToAudioStream

llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tts = Smallest(api_key=os.environ.get("SMALLEST_API_KEY"))

async def generate_text(prompt):
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
    llm_output = generate_text("Explain text to speech like I am five in 5 sentences.")
    
    # As an example, save the generated audio to a WAV file.
    await save_audio_to_wav("llm_to_speech.wav", processor, llm_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**Parameters:**   

- `tts_instance`: Text-to-speech engine (Smallest or AsyncSmallest)
- `queue_timeout`: Wait time for new text (seconds, default: 5.0)
- `max_retries`: Number of retry attempts for failed synthesis (default: 3)

**Output Format:**   
The processor yields raw audio data chunks without WAV headers for streaming efficiency. These chunks can be:

- Played directly through an audio device
- Saved to a file
- Streamed over a network
- Further processed as needed


## Available Methods

```python
from smallest.tts import Smallest

client = Smallest()

print(f"Avalaible Languages: {client.get_languages()}")
print(f"Available Voices: {client.get_voices()}")
print(f"Available Models: {client.get_models()}")
```

## Technical Note: WAV Headers in Streaming Audio

When implementing audio streaming with chunks of synthesized speech, WAV headers are omitted from individual chunks because:

#### Technical Issues
- Each WAV header contains metadata about the entire audio file.
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
