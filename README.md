## Python Client for Smallest AI API

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