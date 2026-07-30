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

## Reference and docs

- Full API reference: [reference.md](./reference.md)
- Product docs: https://smallest.ai/docs

The client also supports response streaming, automatic retries, per-request
timeouts, and access to raw response data. See the reference for details.

## Contributing

Most of `src/` is generated from an API spec and gets overwritten on regeneration,
so hand edits there will not stick. If you spot a bug or a gap, open an issue.
