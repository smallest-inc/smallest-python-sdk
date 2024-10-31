## Python Client for Smallest AI API   

Smallest AI builds ultra-realistic, high-speed multi-lingual voice models tailored for real-time applications, achieving hyper-realistic audio generation in as fast as ~100 milliseconds for 10 seconds of audio. With this sdk, you can easily convert text into high-quality audio with humanlike expressiveness.

Currently, the library supports direct synthesis, real-time streaming, and the ability to stream an LLM-generated output, both synchronously and asynchronously.  

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
  - [get_languages](#get_languages)
  - [get_voices](#get_voices)
  - [get_models](#get_models)
  - [Additional Methods](#additional-methods)

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

### Usage Example (Sync)

```python
from smallest.tts import Smallest

tts = Smallest(api_key="your_api_key")

audio_data = tts.synthesize("Hello, this is a test.")
```

### Usage Example (Async)

```python
import asyncio
from smallest.async_tts import AsyncSmallest

async def main():
    async with AsyncSmallest(api_key="your_api_key") as tts:
        text = "This is a test of the streaming speech synthesis function."
        async for audio_chunk in tts.stream(text):
            with open("output_streamed_audio.wav", "ab") as f:
                f.write(audio_chunk)

asyncio.run(main())
```