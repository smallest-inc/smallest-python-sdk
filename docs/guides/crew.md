# Agent crew (custom LLM)

An **agent crew** is your own node code — bring any LLM (any OpenAI-compatible
endpoint, e.g. Claude via Anthropic) and full control over the turn. You subclass
`OutputCrewNode`, implement `generate_response`, deploy with the CLI.

## The node

```python
from smallestai.atoms.crew.nodes import OutputCrewNode


class Assistant(OutputCrewNode):
    def __init__(self):
        super().__init__(name="assistant")
        self.llm = OpenAIClient(
            model="claude-haiku-4-5",
            api_key=os.environ["ANTHROPIC_API_KEY"],
            base_url="https://api.anthropic.com/v1/",
        )
        self.context.add_message({"role": "system", "content": "You are Acme support. ..."})

    async def generate_response(self):
        response = await self.llm.chat(messages=self.context.messages, stream=True, tools=self.tool_schemas)
        async for chunk in response:
            if chunk.content:
                yield chunk.content
```

`self.context.messages` is what you send to the LLM. As of **5.4.0** the SDK seeds
it from the platform's authoritative message list on each LLM request, so the node
always has the latest user turn (your system prompt is preserved). This fixed a
class of "the agent greets once then goes silent" bugs — make sure you're on 5.4.0.

!!! tip "System prompt"
    Set your system prompt in `__init__` via `self.context.add_message({"role": "system", ...})`.
    It is preserved across the per-turn context sync.

## Deploy

A crew project is a directory with your node(s), a `server.py` that registers the
crew, and a `requirements.txt`. Deploy with:

```bash
smallestai agent-crew deploy --entry-point server.py
smallestai agent-crew builds        # watch build status; Make Live when SUCCEEDED
```

Pin the SDK in `requirements.txt`:

```
smallestai>=5.4.0
```

Environment variables (LLM keys etc.): put them in a `.env` at the project root and
`load_dotenv()` at startup — the `.env` ships with the deploy and is read in the pod.

## Transferring from a crew

The transfer is code — emit an event from a tool. See [Transfer calls](transfer-call.md#agent-crew-emit-a-transfer-event).

## Method names (don't guess)

- Node base class: `OutputCrewNode` (in `smallestai.atoms.crew.nodes`).
- Override `generate_response` (async generator). Override `on_event` to react to
  events — you do **not** need `super()` there; the framework routing already ran.
- `self.speak(text)` sends a one-off utterance; `self.send_event(...)` emits an event.
