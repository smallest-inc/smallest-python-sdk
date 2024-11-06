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

## Examples

### Sync

**Synthesize**

```python
import os
from smallest.tts import Smallest

client = Smallest(api_key=os.environ["SMALLEST_API_KEY"])

audio_data = client.synthesize("Hello, this is a test for sync synthesis function.")

with open("sync_synthesize.wav", "wb") as f:
    f.write(audio_data)
```  

**Stream**  

```python
import os
from smallest.tts import Smallest

client = Smallest(api_key=os.environ.get("SMALLESTAI_API_KEY"))

with open("sync_astream.wav", "ab") as f:
    for audio_chunk in client.stream("Hello, this is a test for Sync Streaming function."):
        f.write(audio_chunk)
        print("Received chunk...")
```  

### Async

**Synthesize**

```python
import os
import asyncio
import aiofiles
from smallest.async_tts import AsyncSmallest

client = AsyncSmallest(api_key=os.environ.get("SMALLESTAI_API_KEY"))

async def main():
    async with client as tts:
        audio_bytes = await tts.synthesize("Hello, this is a test of the async synthesis function.")
        async with aiofiles.open("async_synthesize.wav", "wb") as f:
            await f.write(audio_bytes)

if __name__ == "__main__":
    asyncio.run(main())
```

**Stream**

```python
import os
import asyncio
import aiofiles
from smallest.async_tts import AsyncSmallest

client = AsyncSmallest(api_key=os.environ.get("SMALLESTAI_API_KEY"))

async def main():
    async with aiofiles.open("async_stream.wav", "wb") as f:
        async for chunk in client.stream("Hello, this is a test of the async streaming function."):
            await f.write(chunk)
            print("Received chunk...")

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
