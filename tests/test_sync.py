import os
import jiwer
import httpx
import pytest
import logging
from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions, FileSource

from smallest.tts import Smallest

from dotenv import load_dotenv
load_dotenv()

REFERENCE = "Wow! The jubilant child, bursting with glee, exclaimed, 'Look at those magnificent, vibrant balloons!' as they danced under the shimmering, rainbow-hued sky—truly a spectacle of joy."

transforms = jiwer.Compose(
    [
        jiwer.ExpandCommonEnglishContractions(),
        jiwer.RemoveEmptyStrings(),
        jiwer.ToLowerCase(),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.RemovePunctuation(),
        jiwer.ReduceToListOfListOfWords(),
    ]
)

tts = Smallest(api_key=os.environ.get("SMALLESTAI_API_KEY"))

config: DeepgramClientOptions = DeepgramClientOptions(api_key=os.environ.get("DEEPGRAM_API_KEY"))

deepgram: DeepgramClient = DeepgramClient("", config)

options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
        )

def transcribe(buffer_data):
    payload: FileSource = {
        "buffer": buffer_data,
    }
    response = deepgram.listen.rest.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
    
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]

@pytest.mark.parametrize("reference_text", [REFERENCE])
def test_synthesize_save(reference_text):
    file_path = "test_sync_save.wav"
    try:
        tts.synthesize(reference_text, save_as=file_path)
        with open(file_path, "rb") as file:
            buffer_data = file.read()

        hypothesis = transcribe(buffer_data)
        wer = jiwer.wer(
            reference_text,
            hypothesis,
            truth_transform=transforms,
            hypothesis_transform=transforms,
        )
        logging.info(f"Word Error Rate: {wer}")
        assert wer <= 0.2
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

# Test synthesize function without saving directly
@pytest.mark.parametrize("reference_text", [REFERENCE])
def test_synthesize(reference_text):
    file_path = "test_sync.wav"
    try:
        audio = tts.synthesize(reference_text)
        with open(file_path, "wb") as file:
            file.write(audio)
        with open(file_path, "rb") as file:
            buffer_data = file.read()

        hypothesis = transcribe(buffer_data)
        wer = jiwer.wer(
            reference_text,
            hypothesis,
            truth_transform=transforms,
            hypothesis_transform=transforms,
        )
        logging.info(f"Word Error Rate: {wer}")
        assert wer <= 0.2
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
     



    
