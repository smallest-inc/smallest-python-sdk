# smallestai Python SDK

Build, deploy, and operate Smallest AI voice agents from Python.

```bash
pip install "smallestai>=5.4.0"
```

```python
import os
from smallestai import SmallestAI

client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])

agent_id = client.atoms.agents.create_agent(
    name="Front desk",
    workflow_type="single_prompt",
    first_message="Hi, thanks for calling. How can I help?",
).data
```

## What's here

- **[Getting started](getting-started.md)** — install, auth, your first agent.
- **[Agents](guides/agents.md)** — create, inspect, configure single-prompt agents.
- **[Agent crew (custom LLM)](guides/crew.md)** — build a crew with your own LLM.
- **[Transfer calls](guides/transfer-call.md)** — cold vs warm, hold music, from code.
- **[Call logs & recordings](guides/calls.md)** — inspect what happened on a call.
- **[Build with a coding agent](guides/coding-agents.md)** — a paste-ready prompt so Claude Code / Cursor don't hit the traps.
- **[Method cheatsheet](reference/methods.md)** — the names you'll actually call.

## Two surfaces

- `client.atoms.*` — voice agents (agents, calls, crew, phone numbers, versioning).
- `client.waves.*` — speech (TTS, STT, voice cloning).

For the product + REST API reference, see [docs.smallest.ai](https://docs.smallest.ai).
This site is the Python-SDK companion: install, method names, guides, code.
