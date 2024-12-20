from typing import Literal, List, Tuple, cast
import aiohttp
import asyncio

API_BASE_URL = "https://waves-api.smallest.ai/api/v1"

async def _fetch_voice_and_model() -> Tuple[List[str], List[str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/voice/get-all-models") as response:
            api_response = await response.json()

            voices = []
            for model in api_response:
                for voice in model['voiceIds']:
                    voices.append(voice['voiceId'])
            models = [model['modelName'] for model in api_response]
            return models, voices

models, voices = asyncio.run(_fetch_voice_and_model())

TTSLanguages = ["en", "hi"]
TTSModels = models
TTSVoices = voices