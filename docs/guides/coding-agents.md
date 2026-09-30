# Build with a coding agent

If you drive this SDK through a coding agent (Claude Code, Cursor, etc.), paste the
prompt below as context. It encodes the things that are easy to get wrong so the
agent does not fall into them.

## Paste-ready context

````markdown
You are building a voice agent with the `smallestai` Python SDK. Follow these rules.

INSTALL & AUTH
- `pip install smallestai`
- Client: `from smallestai import SmallestAI; client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])`
- Everything Atoms (voice agents) is under `client.atoms.*`; everything Waves
  (TTS/STT) is under `client.waves.*`.

AGENT TYPES (there are exactly two — do not invent others)
- `single_prompt` (default): a prompt + tools. This is what `create_agent` makes.
- `workflow_graph`: a node graph. Requires org access (403 otherwise).
- There is no "conversation" agent type.

CREATING AN AGENT
- `client.atoms.agents.create_agent(name=..., workflow_type="single_prompt", first_message=...)`
- `.data` on the create response is the **agent id string** (not an object).

TOOLS / TRANSFER (single-prompt agents)
- Do NOT try to set tools via `create_agent`/`update_agent` — there is no tools
  param there.
- Do NOT write the legacy workflow doc (`PATCH /workflow/{id}`) — serving ignores
  it under the branch/revision versioning model.
- Use the helper: `from smallestai.atoms.helpers import AgentTools`
  `AgentTools(api_key=...).add_transfer_call(agent_id, number="+1...", transfer_type="cold_transfer", on_hold_music="relaxing_sound")`
  It goes through the branch flow (draft → publish → make-live) so the tool takes
  effect on the next call.

TRANSFER (agent crew)
- In a crew, the transfer is code: emit
  `SDKAgentTransferConversationEvent(transfer_call_number=..., transfer_options=TransferOption(type=TransferOptionType.COLD_TRANSFER), on_hold_music="relaxing_sound")`
  from a node. `on_hold_music` is optional.

HOLD MUSIC
- Valid `on_hold_music` values: `ringtone`, `relaxing_sound`, `uplifting_beats`, `none`.
- Unset = silence during the bridge. If a transfer "sounds broken" but connects,
  set `on_hold_music`.

CALLS
- Start outbound: `client.atoms.calls.start_outbound_call(agent_id=..., phone_number="+1...", from_product_id=<telephony product id>)`
- Read a call: `client.atoms.calls.get(id="CALL-...")` → `.data` has `transcript`,
  `events`, `status`, `recording_url`, `disconnectionReason`.
- List calls: `client.atoms.calls.list(agent_ids=..., limit=...)` → `.data.logs`.
- A transfer that shows `no_answer`/`timeout` on the transfer leg fired correctly
  but the destination did not pick up — that is not an SDK bug.

VERSIONING
- Config edits go through the branch API (`client.atoms.agent_versioning_branches`).
  The v1 drafts/versions endpoints are deprecated (return 409).

DON'T
- Don't guess method names — list them: `[m for m in dir(client.atoms.agents) if not m.startswith("_")]`.
- Don't assume `.data` is an object; some endpoints return a bare id string.
- Don't set tools and expect them live without publishing + making the revision live.
````

## Two flows a coding agent will commonly build

### Build a platform voice agent

```python
import os
from smallestai import SmallestAI
from smallestai.atoms.helpers import AgentTools

client = SmallestAI(api_key=os.environ["SMALLEST_API_KEY"])

agent_id = client.atoms.agents.create_agent(
    name="Front desk",
    workflow_type="single_prompt",
    first_message="Hi, thanks for calling. How can I help?",
).data

# add a transfer-to-human tool (goes live)
AgentTools(api_key=os.environ["SMALLEST_API_KEY"]).add_transfer_call(
    agent_id, number="+15551234567", transfer_type="cold_transfer", on_hold_music="relaxing_sound"
)

# place a call
client.atoms.calls.start_outbound_call(
    agent_id=agent_id, phone_number="+15559990000", from_product_id="<telephony_product_id>"
)
```

### Use a custom LLM in a crew

See [Agent crew](crew.md) for the full node/server layout. The transfer is emitted
from node code as shown in [Transfer calls](transfer-call.md).
