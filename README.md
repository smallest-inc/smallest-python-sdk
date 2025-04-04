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

Smallest AI builds high-speed multi-lingual voice models tailored for real-time applications, achieving ultra-realistic audio generation in as fast as ~100 milliseconds for 10 seconds of audio. With this sdk, you can easily convert text into high-quality audio with humanlike expressiveness.

Currently, the WavesClient supports direct synthesis and the ability to synthesize streamed LLM output, both synchronously and asynchronously.  

## Table of Contents

- [Installation](#installation)
- [Get the API Key](#get-the-api-key)
- [Atoms Documentation](#atoms-documentation)
  - [Getting Started](#getting-started)
  - [Documentation for API Endpoints](#documentation-for-api-endpoints)
  - [Documentation For Models](#documentation-for-models)
- [Waves Documentation](#waves-documentation)
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


## Atoms Documentation

### Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
import smallestai.atoms
from smallestai.atoms.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://atoms-api.smallest.ai/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = atoms.Configuration(
    host = "https://atoms-api.smallest.ai/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): BearerAuth
configuration = atoms.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with atoms.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = atoms.AgentTemplatesApi(api_client)
    create_agent_from_template_request = atoms.CreateAgentFromTemplateRequest()

    try:
        # Create agent from template
        api_response = api_instance.create_agent_from_template(create_agent_from_template_request)
        print("The response of AgentTemplatesApi->create_agent_from_template:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AgentTemplatesApi->create_agent_from_template: %s\n" % e)
```

### Documentation for API Endpoints

All URIs are relative to *https://atoms-api.smallest.ai/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AgentTemplatesApi* | [**create_agent_from_template**](docs/atoms/AgentTemplatesApi.md#create_agent_from_template) | **POST** /agent/from-template | Create agent from template
*AgentTemplatesApi* | [**get_agent_templates**](docs/atoms/AgentTemplatesApi.md#get_agent_templates) | **GET** /agent/template | Get agent templates
*AgentsApi* | [**create_agent**](docs/atoms/AgentsApi.md#create_agent) | **POST** /agent | Create a new agent
*AgentsApi* | [**delete_agent**](docs/atoms/AgentsApi.md#delete_agent) | **DELETE** /agent/{id} | Delete an agent
*AgentsApi* | [**get_agent_by_id**](docs/atoms/AgentsApi.md#get_agent_by_id) | **GET** /agent/{id} | Get agent by ID
*AgentsApi* | [**get_agents**](docs/atoms/AgentsApi.md#get_agents) | **GET** /agent | Get all agents
*AgentsApi* | [**update_agent**](docs/atoms/AgentsApi.md#update_agent) | **PATCH** /agent/{id} | Update an agent
*CallsApi* | [**start_outbound_call**](docs/atoms/CallsApi.md#start_outbound_call) | **POST** /conversation/outbound | Start an outbound call
*CampaignsApi* | [**create_campaign**](docs/atoms/CampaignsApi.md#create_campaign) | **POST** /campaign | Create a campaign
*CampaignsApi* | [**delete_campaign**](docs/atoms/CampaignsApi.md#delete_campaign) | **DELETE** /campaign/{id} | Delete a campaign
*CampaignsApi* | [**get_campaign_by_id**](docs/atoms/CampaignsApi.md#get_campaign_by_id) | **GET** /campaign/{id} | Get a campaign
*CampaignsApi* | [**get_campaigns**](docs/atoms/CampaignsApi.md#get_campaigns) | **GET** /campaign | Retrieve all campaigns
*CampaignsApi* | [**pause_campaign**](docs/atoms/CampaignsApi.md#pause_campaign) | **POST** /campaign/{id}/pause | Pause a campaign
*CampaignsApi* | [**start_campaign**](docs/atoms/CampaignsApi.md#start_campaign) | **POST** /campaign/{id}/start | Start a campaign
*KnowledgeBaseApi* | [**create_knowledge_base**](docs/atoms/KnowledgeBaseApi.md#create_knowledge_base) | **POST** /knowledgebase | Create a knowledge base
*KnowledgeBaseApi* | [**delete_knowledge_base**](docs/atoms/KnowledgeBaseApi.md#delete_knowledge_base) | **DELETE** /knowledgebase/{id} | Delete a knowledge base
*KnowledgeBaseApi* | [**delete_knowledge_base_item**](docs/atoms/KnowledgeBaseApi.md#delete_knowledge_base_item) | **DELETE** /knowledgebase/{knowledgeBaseId}/items/{knowledgeBaseItemId} | Delete a knowledge base item
*KnowledgeBaseApi* | [**get_knowledge_base_by_id**](docs/atoms/KnowledgeBaseApi.md#get_knowledge_base_by_id) | **GET** /knowledgebase/{id} | Get a knowledge base
*KnowledgeBaseApi* | [**get_knowledge_base_items**](docs/atoms/KnowledgeBaseApi.md#get_knowledge_base_items) | **GET** /knowledgebase/{id}/items | Get all knowledge base items
*KnowledgeBaseApi* | [**get_knowledge_bases**](docs/atoms/KnowledgeBaseApi.md#get_knowledge_bases) | **GET** /knowledgebase | Get all knowledge bases
*KnowledgeBaseApi* | [**upload_media_to_knowledge_base**](docs/atoms/KnowledgeBaseApi.md#upload_media_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-media | Upload a media to a knowledge base
*KnowledgeBaseApi* | [**upload_text_to_knowledge_base**](docs/atoms/KnowledgeBaseApi.md#upload_text_to_knowledge_base) | **POST** /knowledgebase/{id}/items/upload-text | Upload a text to a knowledge base
*LogsApi* | [**get_conversation_logs**](docs/atoms/LogsApi.md#get_conversation_logs) | **GET** /conversation/{id} | Get conversation logs
*OrganizationApi* | [**get_organization**](docs/atoms/OrganizationApi.md#get_organization) | **GET** /organization | Get organization details
*UserApi* | [**get_current_user**](docs/atoms/UserApi.md#get_current_user) | **GET** /user | Get user details

### Documentation For Models

 - [AgentDTO](docs/atoms/AgentDTO.md)
 - [AgentDTOLanguage](docs/atoms/AgentDTOLanguage.md)
 - [AgentDTOSynthesizer](docs/atoms/AgentDTOSynthesizer.md)
 - [AgentDTOSynthesizerVoiceConfig](docs/atoms/AgentDTOSynthesizerVoiceConfig.md)
 - [ApiResponse](docs/atoms/ApiResponse.md)
 - [BadRequestErrorResponse](docs/atoms/BadRequestErrorResponse.md)
 - [CreateAgentFromTemplate200Response](docs/atoms/CreateAgentFromTemplate200Response.md)
 - [CreateAgentFromTemplateRequest](docs/atoms/CreateAgentFromTemplateRequest.md)
 - [CreateAgentRequest](docs/atoms/CreateAgentRequest.md)
 - [CreateAgentRequestLanguage](docs/atoms/CreateAgentRequestLanguage.md)
 - [CreateAgentRequestLanguageSynthesizer](docs/atoms/CreateAgentRequestLanguageSynthesizer.md)
 - [CreateAgentRequestLanguageSynthesizerVoiceConfig](docs/atoms/CreateAgentRequestLanguageSynthesizerVoiceConfig.md)
 - [CreateCampaign201Response](docs/atoms/CreateCampaign201Response.md)
 - [CreateCampaign201ResponseData](docs/atoms/CreateCampaign201ResponseData.md)
 - [CreateCampaignRequest](docs/atoms/CreateCampaignRequest.md)
 - [CreateKnowledgeBase201Response](docs/atoms/CreateKnowledgeBase201Response.md)
 - [CreateKnowledgeBaseRequest](docs/atoms/CreateKnowledgeBaseRequest.md)
 - [DeleteAgent200Response](docs/atoms/DeleteAgent200Response.md)
 - [GetAgentById200Response](docs/atoms/GetAgentById200Response.md)
 - [GetAgentTemplates200Response](docs/atoms/GetAgentTemplates200Response.md)
 - [GetAgentTemplates200ResponseDataInner](docs/atoms/GetAgentTemplates200ResponseDataInner.md)
 - [GetAgents200Response](docs/atoms/GetAgents200Response.md)
 - [GetAgents200ResponseData](docs/atoms/GetAgents200ResponseData.md)
 - [GetCampaignById200Response](docs/atoms/GetCampaignById200Response.md)
 - [GetCampaignById200ResponseData](docs/atoms/GetCampaignById200ResponseData.md)
 - [GetCampaigns200Response](docs/atoms/GetCampaigns200Response.md)
 - [GetCampaigns200ResponseDataInner](docs/atoms/GetCampaigns200ResponseDataInner.md)
 - [GetCampaigns200ResponseDataInnerAgent](docs/atoms/GetCampaigns200ResponseDataInnerAgent.md)
 - [GetCampaigns200ResponseDataInnerAudience](docs/atoms/GetCampaigns200ResponseDataInnerAudience.md)
 - [GetCampaignsRequest](docs/atoms/GetCampaignsRequest.md)
 - [GetConversationLogs200Response](docs/atoms/GetConversationLogs200Response.md)
 - [GetConversationLogs200ResponseData](docs/atoms/GetConversationLogs200ResponseData.md)
 - [GetCurrentUser200Response](docs/atoms/GetCurrentUser200Response.md)
 - [GetCurrentUser200ResponseData](docs/atoms/GetCurrentUser200ResponseData.md)
 - [GetKnowledgeBaseById200Response](docs/atoms/GetKnowledgeBaseById200Response.md)
 - [GetKnowledgeBaseItems200Response](docs/atoms/GetKnowledgeBaseItems200Response.md)
 - [GetKnowledgeBases200Response](docs/atoms/GetKnowledgeBases200Response.md)
 - [GetOrganization200Response](docs/atoms/GetOrganization200Response.md)
 - [GetOrganization200ResponseData](docs/atoms/GetOrganization200ResponseData.md)
 - [GetOrganization200ResponseDataMembersInner](docs/atoms/GetOrganization200ResponseDataMembersInner.md)
 - [GetOrganization200ResponseDataSubscription](docs/atoms/GetOrganization200ResponseDataSubscription.md)
 - [InternalServerErrorResponse](docs/atoms/InternalServerErrorResponse.md)
 - [KnowledgeBaseDTO](docs/atoms/KnowledgeBaseDTO.md)
 - [KnowledgeBaseItemDTO](docs/atoms/KnowledgeBaseItemDTO.md)
 - [StartOutboundCall200Response](docs/atoms/StartOutboundCall200Response.md)
 - [StartOutboundCall200ResponseData](docs/atoms/StartOutboundCall200ResponseData.md)
 - [StartOutboundCallRequest](docs/atoms/StartOutboundCallRequest.md)
 - [UnauthorizedErrorReponse](docs/atoms/UnauthorizedErrorReponse.md)
 - [UpdateAgent200Response](docs/atoms/UpdateAgent200Response.md)
 - [UpdateAgentRequest](docs/atoms/UpdateAgentRequest.md)
 - [UpdateAgentRequestLanguage](docs/atoms/UpdateAgentRequestLanguage.md)
 - [UpdateAgentRequestSynthesizer](docs/atoms/UpdateAgentRequestSynthesizer.md)
 - [UpdateAgentRequestSynthesizerVoiceConfig](docs/atoms/UpdateAgentRequestSynthesizerVoiceConfig.md)
 - [UpdateAgentRequestSynthesizerVoiceConfigOneOf](docs/atoms/UpdateAgentRequestSynthesizerVoiceConfigOneOf.md)
 - [UpdateAgentRequestSynthesizerVoiceConfigOneOf1](docs/atoms/UpdateAgentRequestSynthesizerVoiceConfigOneOf1.md)
 - [UploadTextToKnowledgeBaseRequest](docs/atoms/UploadTextToKnowledgeBaseRequest.md)

## Waves Documentation

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
