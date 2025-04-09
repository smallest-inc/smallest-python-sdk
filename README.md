![image](https://i.imgur.com/TJ2tT4g.png)   


<div align="center">
  <a href="https://twitter.com/smallest_AI">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/smallest_AI.svg?style=social&label=Follow%20smallest_AI" alt="Twitter">
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

Smallest AI offers an end to end Voice AI suite for developers trying to build real-time voice agents. You can either directly use our Text to Speech APIs through the Waves Client or use the Atoms Client to build and operate end to end enterprise ready Voice Agents.

With this sdk, you can easily interact with both Waves and Atoms from any Python 3.9+ application, by utilising WavesClient and AtomsClient classes respectively. Currently, the WavesClient supports direct synthesis and the ability to synthesize streamed LLM output, both synchronously and asynchronously. AtomsClient provides a simpler way of interacting with all our API's to develop and run agentic workflows. 

To learn how to use our API's, check out our documentation for [Atoms](https://atoms-docs.smallest.ai/introduction) and [Waves](https://waves-docs.smallest.ai/content/introduction/)

## Table of Contents

- [Installation](#installation)
- [Get the API Key](#get-the-api-key)
- [What are Atoms?](#what-are-atoms)
  - [Creating your first Agent](#creating-your-first-agent)
  - [Placing an outbound call](#placing-an-outbound-call)
  - [Providing context to the agent](#providing-context-to-the-agent)
  - [Configuring workflows to drive conversations](#configuring-workflows-to-drive-conversations)
  - [Provisioning bulk calling using campaigns](#provisioning-bulk-calling-using-campaigns)  
- [Getting started with Waves](#getting-started-with-waves)
  - [Best Practices for Input Text](#best-practices-for-input-text)
  - [Examples](#examples)
    - [Synchronous](#synchronous)
    - [Asynchronous](#asynchronous)
    - [LLM to Speech](#llm-to-speech)
    - [Add your Voice](#add-your-voice)
      - [Synchronously](#add-synchronously)
      - [Asynchronously](#add-asynchronously)
    - [Delete your Voice](#delete-your-voice)
      - [Synchronously](#delete-synchronously)
      - [Asynchronously](#delete-asynchronously)
  - [Available Methods](#available-methods)
  - [Technical Note: WAV Headers in Streaming Audio](#technical-note-wav-headers-in-streaming-audio)

## Installation

To install the latest version available   
```bash
pip install smallestai
```  
When using an SDK in your application, make sure to pin to at least the major version (e.g., ==1.*). This helps ensure your application remains stable and avoids potential issues from breaking changes in future updates.   
   

## Get the API Key  

1. Visit [console.smallest.ai](https://console.smallest.ai//) and sign up for an account or log in if you already have an account.  
2. Navigate to `API Keys` tab in your account dashboard.
3. Create a new API Key and copy it.
4. Export the API Key in your environment with the name `SMALLEST_API_KEY`, ensuring that your application can access it securely for authentication.


## What are Atoms

Atoms are agents that can talk to anyone on voice or text in any language, in any voice. Imagine an AI that you can hire to perform end-to-end tasks for your business. The following examples give an overview of how AtomsClient leverages abstractions such as KnowledgeBase, Campaigns and graph-based Workflows to let you build the smartest voice agent for your usecase.

You can find the full reference for Atoms [here](./docs/atoms/Api.md).

### Creating your first Agent

```python
from smallestai.atoms import AtomsClient

TARGET_PHONE_NUMBER = "+919666666666"
 
def main():
    # alternatively, you can export API Key as environment variable SMALLEST_API_KEY. 
    config = Configuration(
        access_token = 'SMALLEST_API_KEY' 
    )

    atoms_client = AtomsClient(config)

    agent_id = atoms_client.create_agent(
        create_agent_request={
            "name": "Atoms Multi-Modal Agent",
            "description": "My first atoms agent",
            "language": {
                "enabled": "en",
                "switching": False
            },
            "synthesizer": {
                "voiceConfig": {
                    "model": "waves_lightning_large",
                    "voiceId": "nyah"
                },
                "speed": 1.2,
                "consistency": 0.5,
                "similarity": 0,
                "enhancement": 1
            },
            "slmModel": "electron-v1",
        }
    ).data
    
    print(f"Successfully created agent with id: {agent_id}")

if __name__ == "__main__":
    main()
```

### Placing an outbound call

```python
from smallestai.atoms import AtomsClient
from smallestai.atoms import Configuration

TARGET_PHONE_NUMBER = "+919666666666"
MY_AGENT_ID = "67e****ff*ec***82*3c9e**"

def main():
    # assumes you have exported API_KEY in SMALLEST_API_KEY environment variable
    atoms_client = AtomsClient()

    call_response = atoms_client.start_outbound_call(
        start_outbound_call_request={
            "agent_id": MY_AGENT_ID,
            "phone_number": TARGET_PHONE_NUMBER,
        }
    )
    print(f"Successfully placed call with id: {call_response.conversation_id}")
           
if __name__ == "__main__":
    main()
```
### Providing context to the agent

An agent can be attached to a knowledge base, which it can look up during conversations. Here is how you can do it:

```python
from smallestai.atoms import AtomsClient

def main():
    # assumes you have exported API_KEY in SMALLEST_API_KEY environment variable
    atoms_client = AtomsClient()
    
    # Create a new knowledge base
    knowledge_base = atoms_client.create_knowledge_base(
        create_knowledge_base_request={
            "name": "Customer Support Knowledge Base",
            "description": "Contains FAQs and product information"
        }
    )
    knowledge_base_id = knowledge_base.data

    with open("product_manual.pdf", "rb") as f:
        media_content = f.read()
        media_response = atoms_client.upload_media_to_knowledge_base(
            id=knowledge_base_id,
            media=media_content
        )
    print("Added product_manual.pdf to knowledge base")

if __name__ == "__main__":
    main()
 ```   

### Configuring workflows to drive conversations

An agent can be configured with a graph-based workflow to help it drive meaningful conversations. You can explore making one on our [platform](https://atoms.smallest.ai/dashboard/agents). Refer to our [documentation](https://atoms-docs.smallest.ai/deep-dive/workflow/what-is-a-workflow) for learning more extensively.

![image](https://i.imgur.com/kRs53zV.png)

### Provisioning bulk calling using campaigns

To manage bulk calls, you can use [Atoms platform](https://atoms.smallest.ai/dashboard/audience) to create [audience](https://atoms-docs.smallest.ai/deep-dive/audience/audience) (collection of contacts) and then configure [campaigns](https://atoms-docs.smallest.ai/deep-dive/campaign/campaign) to run.  

## Getting started with Waves

### Best Practices for Input Text

### Examples

#### Synchronous  
A synchronous text-to-speech synthesis client. 

**Basic Usage:**   
```python

from smallestai.waves import WavesClient

def main():
    waves_client = WavesClient(api_key="SMALLEST_API_KEY")
    waves_client.synthesize(
        text="Hello, this is a test for sync synthesis function.",
        save_as="sync_synthesize.wav"
    )

if __name__ == "__main__":
    main()
```

**Parameters:**   
- `api_key`: Your API key (can be set via SMALLEST_API_KEY environment variable)
- `model`: TTS model to use (default: "lightning")
- `sample_rate`: Audio sample rate (default: 24000)
- `voice_id`: Voice ID (default: "emily")
- `speed`: Speech speed multiplier (default: 1.0)
- `consistency`: Controls word repetition and skipping. Decrease it to prevent skipped words, and increase it to prevent repetition. Only supported in `lightning-large` model. (default: 0.5)
- `similarity`: Controls the similarity between the synthesized audio and the reference audio. Increase it to make the speech more similar to the reference audio. Only supported in `lightning-large` model. (default: 0)
- `enhancement`: Enhances speech quality at the cost of increased latency. Only supported in `lightning-large` model. (default: False)
- `add_wav_header`: Whether to add a WAV header to the output audio.

These parameters are part of the `Smallest` instance. They can be set when creating the instance (as shown above). However, the `synthesize` function also accepts `kwargs`, allowing you to override these parameters for a specific synthesis request.

For example, you can modify the speech speed and sample rate just for a particular synthesis call:  
```py
client.synthesize(
    "Hello, this is a test for sync synthesis function.",
    save_as="sync_synthesize.wav",
    speed=1.5,  # Overrides default speed
    sample_rate=16000  # Overrides default sample rate
)
```


#### Asynchronous   
Asynchronous text-to-speech synthesis client.    

**Basic Usage:**   
```python
import asyncio
import aiofiles
import smallestai

async def main():
    client = smallestai.waves.AsyncWavesClient(api_key="SMALLEST_API_KEY")
    async with client as tts:
        audio_bytes = await tts.synthesize("Hello, this is a test of the async synthesis function.") 
        async with aiofiles.open("async_synthesize.wav", "wb") as f:
            await f.write(audio_bytes) # alternatively you can use the `save_as` parameter.

if __name__ == "__main__":
    asyncio.run(main())
```

**Running Asynchronously in a Jupyter Notebook**   
If you are using a Jupyter Notebook, use the following approach to execute the asynchronous function within an existing event loop:
```python
import asyncio
import aiofiles
from smallest import AsyncSmallest

async def main():
    client = AsyncSmallest(api_key="SMALLEST_API_KEY")
    async with client as tts:
        audio_bytes = await tts.synthesize("Hello, this is a test of the async synthesis function.") 
        async with aiofiles.open("async_synthesize.wav", "wb") as f:
            await f.write(audio_bytes) # alternatively you can use the `save_as` parameter.

await main()
```

**Parameters:**    
- `api_key`: Your API key (can be set via SMALLEST_API_KEY environment variable)
- `model`: TTS model to use (default: "lightning")
- `sample_rate`: Audio sample rate (default: 24000)
- `voice_id`: Voice ID (default: "emily")
- `speed`: Speech speed multiplier (default: 1.0)
- `consistency`: Controls word repetition and skipping. Decrease it to prevent skipped words, and increase it to prevent repetition. Only supported in `lightning-large` model.
- `similarity`: Controls the similarity between the synthesized audio and the reference audio. Increase it to make the speech more similar to the reference audio. Only supported in `lightning-large` model.
- `enhancement`: Enhances speech quality at the cost of increased latency. Only supported in `lightning-large` model.
- `add_wav_header`: Whether to add a WAV header to the output audio.

These parameters are part of the `AsyncSmallest` instance. They can be set when creating the instance (as shown above). However, the `synthesize` function also accepts `kwargs`, allowing you to override any of these parameters on a per-request basis.  

For example, you can modify the speech speed and sample rate just for a particular synthesis request:  
```py
audio_bytes = await tts.synthesize(
    "Hello, this is a test of the async synthesis function.",
    speed=1.5,  # Overrides default speed
    sample_rate=16000  # Overrides default sample rate
)
```

#### LLM to Speech    

The `TextToAudioStream` class provides real-time text-to-speech processing, converting streaming text into audio output. It's particularly useful for applications like voice assistants, live captioning, or interactive chatbots that require immediate audio feedback from text generation. Supports both synchronous and asynchronous TTS instance.

##### Stream through a WebSocket

```python
import asyncio
import websockets
from groq import Groq
from smallest import Smallest, TextToAudioStream  

# Initialize Groq (LLM) and Smallest (TTS) instances
llm = Groq(api_key="GROQ_API_KEY")
tts = Smallest(api_key="SMALLEST_API_KEY")
WEBSOCKET_URL = "wss://echo.websocket.events" # Mock WebSocket server

# Async function to stream text generation from LLM
async def generate_text(prompt):
    completion = llm.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
        stream=True,
    )

    # Yield text as it is generated
    for chunk in completion:
        text = chunk.choices[0].delta.content
        if text:
            yield text

# Main function to run the process
async def main():
    # Initialize the TTS processor
    processor = TextToAudioStream(tts_instance=tts)

    # Generate text from LLM
    llm_output = generate_text("Explain text to speech like I am five in 5 sentences.")

    # Stream the generated speech throught a websocket
    async with websockets.connect(WEBSOCKET_URL) as ws:
        print("Connected to WebSocket server.")

        # Stream the generated speech
        async for audio_chunk in processor.process(llm_output):
            await ws.send(audio_chunk)  # Send audio chunk
            echoed_data = await ws.recv()  # Receive the echoed message
            print("Received from server:", echoed_data[:20], "...")  # Print first 20 bytes

        print("WebSocket connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
```

##### Save to a File
```python
import wave
import asyncio
from groq import Groq
from smallest import Smallest, TextToAudioStream

llm = Groq(api_key="GROQ_API_KEY")
tts = Smallest(api_key="SMALLEST_API_KEY")

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

#### Add your Voice   
The Smallest AI SDK allows you to clone your voice by uploading an audio file. This feature is available both synchronously and asynchronously, making it flexible for different use cases. Below are examples of how to use this functionality.  

##### Add Synchronously
```python
from smallest import Smallest

def main():
    client = Smallest(api_key="SMALLEST_API_KEY")
    res = client.add_voice(display_name="My Voice", file_path="my_voice.wav")
    print(res)

if __name__ == "__main__":
    main()
```  

##### Add Asynchronously
```python
import asyncio
from smallest import AsyncSmallest

async def main():
    client = AsyncSmallest(api_key="SMALLEST_API_KEY")
    res = await client.add_voice(display_name="My Voice", file_path="my_voice.wav")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Delete your Voice
The Smallest AI SDK allows you to delete your cloned voice. This feature is available both synchronously and asynchronously, making it flexible for different use cases. Below are examples of how to use this functionality.

##### Delete Synchronously
```python
from smallest import Smallest

def main():
    client = Smallest(api_key="SMALLEST_API_KEY")
    res = client.delete_voice(voice_id="voice_id")
    print(res)

if __name__ == "__main__":
    main()
```

##### Delete Asynchronously
```python
import asyncio
from smallest import AsyncSmallest

async def main():
    client = AsyncSmallest(api_key="SMALLEST_API_KEY")
    res = await client.delete_voice(voice_id="voice_id")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Available Methods

```python
from smallest import Smallest

client = Smallest(api_key="SMALLEST_API_KEY")

print(f"Available Languages: {client.get_languages()}")
print(f"Available Voices: {client.get_voices(model='lightning')}")
print(f"Available Voices: {client.get_cloned_voices()}")
print(f"Available Models: {client.get_models()}")
```

#### Technical Note: WAV Headers in Streaming Audio

When implementing audio streaming with chunks of synthesized speech, WAV headers are omitted from individual chunks because:

##### Technical Issues
- Each WAV header contains metadata about the entire audio file.
- Multiple headers would make chunks appear as separate audio files and add redundancy.
- Headers contain file-specific data (like total size) that's invalid for chunks.
- Sequential playback of chunks with headers causes audio artifacts (pop sounds) when concatenating or playing audio sequentially.
- Audio players would try to reinitialize audio settings for each chunk.

##### Best Practices for Audio Streaming
1. Stream raw PCM audio data without headers
2. Add a single WAV header only when:
   - Saving the complete stream to a file
   - Initializing the audio playback system
   - Converting the stream to a standard audio format