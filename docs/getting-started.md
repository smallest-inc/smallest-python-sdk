# Getting started

## Install

```bash
pip install "smallestai>=5.4.0"
```

## Authenticate

Get an API key from [app.smallest.ai](https://app.smallest.ai) (Settings → API keys).

```python
import os
from smallestai import SmallestAI

client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])
```

The CLI (`smallestai`) reads `SMALLEST_API_KEY`, or the key stored by
`smallestai auth login`. Set `SMALLEST_BASE_URL` to target a non-prod host.

## Your first agent

```python
agent_id = client.atoms.agents.create_agent(
    name="Front desk",
    workflow_type="single_prompt",  # the default; the other type is workflow_graph
    first_message="Hi, thanks for calling. How can I help?",
).data
print(agent_id)  # NOTE: .data here is the agent id string, not an object
```

Two things worth knowing up front:

- There are exactly **two** agent types: `single_prompt` (default) and
  `workflow_graph` (needs org access). There is no "conversation" type.
- Some create/id endpoints return a **bare id string** in `.data`, not an object.

## Place a call

```python
client.atoms.calls.start_outbound_call(
    agent_id=agent_id,
    phone_number="+15559990000",
    from_product_id="<telephony_product_id>",  # a number you own; see client.atoms.phone_numbers.list()
)
```

## Next

- Add a transfer: [Transfer calls](guides/transfer-call.md)
- Custom LLM: [Agent crew](guides/crew.md)
- See what happened: [Call logs & recordings](guides/calls.md)
