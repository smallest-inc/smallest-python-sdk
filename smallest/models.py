from typing import Literal
from typing import List
import requests

API_BASE_URL = "https://waves-api.smallest.ai/api/v1"

def get_voice_and_model() -> List[str]:
    api_response = requests.get(f"{API_BASE_URL}/voice/get-all-models").json()
    voices = []
    for model in api_response:
        for voice in model['voiceIds']:
            voices.append(voice['voiceId'])
    models = [model['modelName'] for model in api_response]
    return models, voices

models, voices = get_voice_and_model()

TTSModels = Literal[*models]
TTSLanguages = Literal["en", "hi"]
TTSVoices = Literal[*voices]