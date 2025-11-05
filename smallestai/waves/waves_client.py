import os
import json
import copy
import requests
from typing import Optional, Union, List

from smallestai.waves.exceptions import InvalidError, APIError
from smallestai.waves.utils import (TTSOptions, validate_input, validate_asr_input,
                        get_smallest_languages, get_smallest_models, ALLOWED_AUDIO_EXTENSIONS, API_BASE_URL)

class WavesClient:
    def __init__(
        self,
        api_key: str = None,
        model: Optional[str] = "lightning",
        sample_rate: Optional[int] = 24000,
        voice_id: Optional[str] = "emily",
        speed: Optional[float] = 1.0,
        consistency: Optional[float] = 0.5,
        similarity: Optional[float] = 0.0,
        enhancement: Optional[int] = 1,
        language: Optional[str] = "en",
        output_format: Optional[str] = "wav"
    ) -> None:
        """
        Smallest Instance for text-to-speech synthesis.

        This is a synchronous implementation of the text-to-speech functionality. 
        For an asynchronous version, please refer to the AsyncSmallest Instance.

        Args:
        - api_key (str): The API key for authentication, export it as 'SMALLEST_API_KEY' in your environment variables.
        - model (TTSModels): The model to be used for synthesis.
        - sample_rate (int): The sample rate for the audio output.
        - voice_id (TTSVoices): The voice to be used for synthesis.
        - speed (float): The speed of the speech synthesis.
        - consistency (float): This parameter controls word repetition and skipping. Decrease it to prevent skipped words, and increase it to prevent repetition. Only supported in `lightning-large` model. Range - [0, 1]
        - similarity (float): This parameter controls the similarity between the synthesized audio and the reference audio. Increase it to make the speech more similar to the reference audio. Only supported in `lightning-large` model. Range - [0, 1]
        - enhancement (int): Enhances speech quality at the cost of increased latency. Only supported in `lightning-large` model. Range - [0, 2].
        - language (str): The language for synthesis. Default is "en".
        - output_format (str): The output audio format. Options: "pcm", "mp3", "wav", "mulaw". Default is "pcm".

        Methods:
        - get_languages: Returns a list of available languages for synthesis.
        - get_voices: Returns a list of available voices for synthesis.
        - get_models: Returns a list of available models for synthesis.
        - synthesize: Converts the provided text into speech and returns the audio content.
        """
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY")
        if not self.api_key:
            raise InvalidError()
        if model == "lightning-large" and voice_id is None:
            voice_id = "lakshya"

        self.chunk_size = 250
        
        self.opts = TTSOptions(
            model=model,
            sample_rate=sample_rate,
            voice_id=voice_id,
            api_key=self.api_key,
            speed=speed,
            consistency=consistency,
            similarity=similarity,
            enhancement=enhancement,
            language=language,
            output_format=output_format
        )
    
        
    def get_languages(self, model:str="lightning") -> List[str]:
        """Returns a list of available languages."""
        return get_smallest_languages(model)
    
    def get_cloned_voices(self) -> str:
        """Returns a list of your cloned voices."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/lightning-large/get_cloned_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get cloned voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)
    

    def get_voices(
            self,
            model: Optional[str] = "lightning"
        ) -> str:
        """Returns a list of available voices."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        res = requests.request("GET", f"{API_BASE_URL}/{model}/get_voices", headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to get voices: {res.text}. For more information, visit https://waves.smallest.ai/")
        
        return json.dumps(res.json(), indent=4, ensure_ascii=False)
    

    def get_models(self) -> List[str]:
        """Returns a list of available models."""
        return get_smallest_models()
    
    
    def synthesize(
            self,
            text: str,
            **kwargs
        ) -> Union[bytes]:
        """
        Synthesize speech from the provided text.

        - text (str): The text to be converted to speech.
        - stream (Optional[bool]): If True, returns an iterator yielding audio chunks instead of a full byte array.
        - kwargs: Additional optional parameters to override `__init__` options for this call.

        Returns:
        - Union[bytes, None, Iterator[bytes]]: 
            - If `stream=True`, returns an iterator yielding audio chunks.
            - If `save_as` is provided, saves the file and returns None.
            - Otherwise, returns the synthesized audio content as bytes.

        Raises:
        - InvalidError: If the provided file name does not have a .wav or .mp3 extension when `save_as` is specified.
        - APIError: If the API request fails or returns an error.
        """
        opts = copy.deepcopy(self.opts)
        valid_keys = set(vars(opts).keys())

        invalid_keys = [key for key in kwargs if key not in valid_keys]
        if invalid_keys:
            raise ValueError(f"Invalid parameter(s) in kwargs: {', '.join(invalid_keys)}. Allowed parameters are: {', '.join(valid_keys)}")
                                
        for key, value in kwargs.items():
            setattr(opts, key, value)

        validate_input(text, opts.model, opts.sample_rate, opts.speed, opts.consistency, opts.similarity, opts.enhancement)

        payload = {
            "text": text,
            "voice_id": opts.voice_id,
            "sample_rate": opts.sample_rate,
            "speed": opts.speed,
            "consistency": opts.consistency,
            "similarity": opts.similarity,
            "enhancement": opts.enhancement,
            "language": opts.language,
            "output_format": opts.output_format
        }

        if opts.model == "lightning-large" or opts.model == "lightning-v2":
            if opts.consistency is not None:
                payload["consistency"] = opts.consistency
            if opts.similarity is not None:
                payload["similarity"] = opts.similarity
            if opts.enhancement is not None:
                payload["enhancement"] = opts.enhancement
                
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        res = requests.post(f"{API_BASE_URL}/{opts.model}/get_speech", json=payload, headers=headers)
        if res.status_code != 200:
            raise APIError(f"Failed to synthesize speech: {res.text}. Please check if you have set the correct API key. For more information, visit https://waves.smallest.ai/")
                
        return res.content
    
    
    def add_voice(self, display_name: str, file_path: str) -> str:
        """
        Instantly clone your voice synchronously.

        Args:
        - display_name (str): The display name for the new voice.
        - file_path (str): The path to the reference audio file to be cloned.

        Returns:
        - str: The response from the API as a formatted JSON string.

        Raises:
        - InvalidError: If the file does not exist or is not a valid audio file.
        - APIError: If the API request fails or returns an error.
        """
        if not os.path.isfile(file_path):
            raise InvalidError("Invalid file path. File does not exist.")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ALLOWED_AUDIO_EXTENSIONS:
            raise InvalidError(f"Invalid file type. Supported formats are: {ALLOWED_AUDIO_EXTENSIONS}")
        
        url = f"{API_BASE_URL}/lightning-large/add_voice"
        payload = {'displayName': display_name}

        files = [('file', (os.path.basename(file_path), open(file_path, 'rb'), 'audio/wav'))]

        headers = {
            'Authorization': f"Bearer {self.api_key}",
        }

        response = requests.post(url, headers=headers, data=payload, files=files)
        if response.status_code != 200:
            raise APIError(f"Failed to add voice: {response.text}. For more information, visit https://waves.smallest.ai/")

        return response.json()


    def delete_voice(self, voice_id: str) -> str:
        """
        Delete a cloned voice synchronously.

        Args:
        - voice_id (str): The ID of the voice to be deleted.

        Returns:
        - str: The response from the API.

        Raises:
        - APIError: If the API request fails or returns an error.
        """
        url = f"{API_BASE_URL}/lightning-large"
        payload = {'voiceId': voice_id}

        headers = {
            'Authorization': f"Bearer {self.api_key}",
        }

        response = requests.delete(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise APIError(f"Failed to delete voice: {response.text}. For more information, visit https://waves.smallest.ai/")
        
        return response.json()
    
    def transcribe(
        self,
        file_path: str,
        language: Optional[str] = "en",
        word_timestamps: Optional[bool] = False,
        age_detection: Optional[bool] = False,
        gender_detection: Optional[bool] = False,
        emotion_detection: Optional[bool] = False,
        model: Optional[str] = "lightning"
    ) -> dict:
        validate_asr_input(file_path, model, language)

        url = f"{API_BASE_URL}/speech-to-text"
        headers = {
            'Authorization': f"Bearer {self.api_key}",
        }
        payload = {
            'model': model,
            'language': language,
            'word_timestamps': str(bool(word_timestamps)).lower(),
            'age_detection': str(bool(age_detection)).lower(),
            'gender_detection': str(bool(gender_detection)).lower(),
            'emotion_detection': str(bool(emotion_detection)).lower()
        }

        file_extension = os.path.splitext(file_path)[1].lower()
        content_type = f"audio/{file_extension[1:]}" if file_extension else "application/octet-stream"

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, content_type)}
            response = requests.post(url, headers=headers, files=files, data=payload)

        if response.status_code != 200:
            raise APIError(f"Failed to transcribe audio: {response.text}. For more information, visit https://waves-docs.smallest.ai/v4.0.0/content/api-references/asr-post-api")

        return response.json()