import asyncio
from smallest.async_tts import AsyncSmallest

async def main():
    async with AsyncSmallest() as tts:
        text = "This is a test of the streaming speech synthesis function."
        async for audio_chunk in tts.stream(text):
            with open("output_streamed_audio.wav", "ab") as f:
                f.write(audio_chunk)

asyncio.run(main())
