# SmallestAI Python SDK

[![pypi](https://img.shields.io/pypi/v/smallestai)](https://pypi.python.org/pypi/smallestai)

`pip install smallestai` gives you one package with two surfaces, plus a CLI:

- **Atoms** — build, configure, deploy, and phone-call voice AI agents (`client.atoms`).
- **Waves** — low-latency text-to-speech and speech-to-text, sync/async and streaming (`client.waves`).
- **CLI** — `smallestai` for managing agents and deploying agent-crew code.

```sh
pip install smallestai
```

## Table of Contents

- [Quickstart](#quickstart-create-an-agent-and-call-it)
- [Text-to-speech and speech-to-text](#text-to-speech-and-speech-to-text-waves)
- [Agent crew: your own LLM](#agent-crew-your-own-llm-in-the-middle)
- [CLI](#cli)
- [Async client](#async-client)
- [Environments](#environments)
- [Exception handling](#exception-handling)
- [Streaming and websockets](#streaming-and-websockets)
- [Advanced](#advanced)
  - [Access raw response data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom client](#custom-client)
- [Reference and docs](#reference-and-docs)
- [Contributing](#contributing)

## Quickstart: create an agent and call it

```python
from smallestai import SmallestAI

client = SmallestAI(api_key="<your-api-key>")

# create an agent (the response .data is the new agent id)
agent_id = client.atoms.agents.create_agent(name="my-first-agent").data

# place an outbound call (from_product_id is a rented number's product id)
client.atoms.calls.start_outbound_call(
    agent_id=agent_id,
    phone_number="+1XXXXXXXXXX",
    from_product_id="<rented-number-product-id>",
)
```

## Text-to-speech and speech-to-text (Waves)

`synthesize_tts` streams audio bytes. List available voices with `client.waves.get_voices()`.

```python
from smallestai import SmallestAI

client = SmallestAI(api_key="<your-api-key>")

with open("out.wav", "wb") as f:
    for chunk in client.waves.synthesize_tts(text="Hello from Smallest.", voice_id="<voice-id>"):
        f.write(chunk)
```

Streaming speech-to-text helper:

```python
from smallestai.waves.helpers import stream_speech_to_text

for event in stream_speech_to_text(client, language="en"):
    print(event)
```

## Agent crew: your own LLM in the middle

An agent crew runs the LLM turn on a model **you** choose while Smallest handles
STT and TTS. Point the crew node's `OpenAIClient` at any OpenAI-compatible
endpoint (a hosted API, or a local model via Ollama):

```python
from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.clients.openai import OpenAIClient

class Assistant(OutputCrewNode):
    def __init__(self):
        super().__init__(name="assistant")
        self.llm = OpenAIClient(
            model="claude-haiku-4-5",
            api_key="<your-llm-key>",
            base_url="https://api.anthropic.com/v1/",   # or http://localhost:11434/v1 for Ollama
        )

    async def generate_response(self):
        async for chunk in await self.llm.chat(self.context.messages, stream=True):
            if chunk.content:
                yield chunk.content
```

Conversation history is handled for you: every turn is appended to `self.context`,
and you send `self.context.messages` to the model each turn.

Deploy it with the CLI:

```sh
smallestai auth login
smallestai agent-crew init --agent-id <agent-id>
smallestai agent-crew deploy --entry-point server.py
smallestai agent-crew builds        # pick the build -> Make Live
```

A flat directory (`server.py` + `requirements.txt` at the root) is the simplest
layout; a `src/` layout with a `pyproject.toml` also works (declare all runtime
deps in the pyproject).

## CLI

```sh
smallestai auth login               # store your API key
smallestai agents list              # list, get, call, and manage agents
smallestai agent-crew deploy ...     # package and deploy crew code
smallestai agent-crew chat           # talk to a running crew locally
```

## Async client

The SDK exports an `async` client with the same surface:

```python
import asyncio
from smallestai import AsyncSmallestAI

async def main():
    client = AsyncSmallestAI(api_key="<your-api-key>")
    agents = await client.atoms.agents.list_agents()
    print(agents.data)

asyncio.run(main())
```

## Environments

```python
from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment

client = SmallestAI(environment=SmallestAIEnvironment.PRODUCTION)
```

## Exception handling

```python
from smallestai.core.api_error import ApiError

try:
    client.atoms.agents.get_agent(id="does-not-exist")
except ApiError as e:
    print(e.status_code, e.body)
```

## Streaming and websockets

Waves supports real-time, low-latency streaming over websockets. `stream()` returns a context manager; iterate it to process messages as they arrive.

```python
from smallestai import SmallestAI

client = SmallestAI(api_key="<your-api-key>")

# real-time speech-to-text
with client.waves.speech_to_text.stream() as socket:
    for message in socket:
        print(message)
```

The async client mirrors this with `async with` / `async for`. Text-to-speech streams too: `synthesize_tts(...)` yields audio bytes as they are generated (see above).

## Advanced

### Access raw response data

Use `.with_raw_response` to get the response headers and status alongside the parsed data.

```python
response = client.atoms.agents.with_raw_response.get_agent(id="<agent-id>")
print(response.headers)       # response headers
print(response.status_code)   # status code
print(response.data)          # parsed object
```

### Retries

The SDK retries retryable requests with exponential backoff (default 2). Configure it at the client or per request.

```python
client = SmallestAI(api_key="<your-api-key>", max_retries=3)

# or per request
client.atoms.agents.get_agent(id="<agent-id>", request_options={"max_retries": 1})
```

### Timeouts

Defaults to 60 seconds. Configure at the client or per request.

```python
client = SmallestAI(api_key="<your-api-key>", timeout=20.0)

# or per request
client.atoms.agents.get_agent(id="<agent-id>", request_options={"timeout_in_seconds": 5})
```

### Custom client

Override the `httpx` client for proxies, custom transports, and similar.

```python
import httpx
from smallestai import SmallestAI

client = SmallestAI(
    api_key="<your-api-key>",
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Reference and docs

- Full API reference: [reference.md](./reference.md)
- Product docs: https://smallest.ai/docs

## Telemetry

The SDK sends anonymous, aggregated usage telemetry (which CLI commands run, deploy
outcomes) so we can see what to improve. It never includes personal data or secrets:
no API keys, agent ids, prompts, transcripts, phone numbers, file paths, or error
messages. Only the event name, SDK / Python / OS version, and a random anonymous
install id. It is fire-and-forget and never blocks your program.

Opt out any time:

```bash
export SMALLESTAI_TELEMETRY=0    # or DO_NOT_TRACK=1
```

## Contributing

Most of `src/` is generated from an API spec and gets overwritten on regeneration,
so hand edits there will not stick. If you spot a bug or a gap, open an issue.
