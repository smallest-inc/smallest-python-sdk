# Transfer calls

There are two ways an agent can transfer a live call to another number. Pick by
how you built the agent.

| You built the agent as… | Transfer is configured by… |
|---|---|
| A **single-prompt** agent (prompt + tools) | A `transfer_call` **tool** on the agent — set it from code with `AgentTools` |
| An **agent crew** (custom node code / custom LLM) | Your node **emits a transfer event** (`SDKAgentTransferConversationEvent`) |

Both end up at the same place on the platform: the call bridges to the number
you gave, optionally with hold music while it connects.

## Cold vs warm

- **Cold transfer** (`cold_transfer`) — a **direct connect**. The destination is
  dialed and the caller is bridged straight through, with **no debrief**. The
  agent drops off. There is **no hold-music / whisper / three-way** step (nothing
  to fill — it connects directly). Use for "send them to the front desk".
- **Warm transfer** (`warm_transfer`) — the agent **debriefs the destination**
  before bridging. This handover window is where the extra features apply:
    - **On-hold music** — audio to the caller while the handover happens.
    - **Whisper message** (private handoff) — spoken only to the destination agent
      (e.g. "summarize the caller's issue").
    - **Three-way message** (public handoff) — spoken to both parties once connected.

!!! warning "Hold music applies to warm transfer, not cold"
    Cold transfer is a direct connect with no window for audio, so `on_hold_music`
    has no effect on it. If you want the caller to hear music (and the agent to
    brief the destination), use `warm_transfer`. Setting `on_hold_music` on a cold
    transfer is silently ignored — a common cause of "the transfer sounded blank".

Supported `on_hold_music` values (warm): `ringtone` · `relaxing_sound` ·
`uplifting_beats` · `none`.

---

## Single-prompt agents: `AgentTools`

Agent config lives in the branch/revision versioning model, and serving reads the
live branch's head revision. `AgentTools` handles that whole flow for you
(open a draft → publish → make live), so a tool you add actually takes effect on
the next call.

```python
from smallestai.atoms.helpers import AgentTools

tools = AgentTools(api_key="sk_...")  # or SMALLEST_API_KEY env var

tools.add_transfer_call(
    "AGENT_ID",
    number="+15551234567",
    transfer_type="cold_transfer",  # or "warm_transfer"
    on_hold_music="relaxing_sound",  # audio while bridging
)
```

That one call:

1. resolves the agent's live branch,
2. merges a `transfer_call` tool into a draft (your prompt and other tools are
   untouched — config is section-based),
3. publishes and waits for the security scan,
4. makes the new revision live.

Inspect or remove:

```python
for t in tools.get_tools("AGENT_ID"):
    print(t.type, t.name)

tools.remove_tool("AGENT_ID", "transfer_call")
```

Stage a change without activating it (make it live later from the dashboard):

```python
tools.add_transfer_call("AGENT_ID", number="+1555...", make_live=False)
```

!!! warning "Writing the legacy workflow doc does nothing on live calls"
    Under the branch model, serving ignores the legacy `PATCH /workflow/{id}`
    document. Always go through the branch flow (which `AgentTools` does). The v1
    drafts/versions endpoints are deprecated and return 409.

---

## Agent crew: emit a transfer event

In a crew, the transfer is code. From a node (for example, a `@function_tool`),
emit `SDKAgentTransferConversationEvent`:

```python
from smallestai.atoms.crew.events import (
    SDKAgentTransferConversationEvent,
    TransferOption,
    TransferOptionType,
)


@function_tool(name="transfer_call")
async def transfer_call(self) -> None:
    await self.send_event(
        SDKAgentTransferConversationEvent(
            transfer_call_number="+15551234567",
            transfer_options=TransferOption(type=TransferOptionType.COLD_TRANSFER),
            on_hold_music="relaxing_sound",  # optional; omit for platform default
        )
    )
```

`on_hold_music` is optional (defaults to `None`). Pass a value to avoid a silent
hold.

---

## Steps to get a transfer working end to end

1. **Set a real, reachable destination number** (E.164, e.g. `+15551234567`). The
   transfer only completes when the destination **answers** — a number that goes
   to voicemail or does not pick up shows up as `no_answer` / `timeout` on the
   transfer leg.
2. **Choose cold or warm** (`transfer_type` / `TransferOptionType`).
3. **Set `on_hold_music`** if you want audio during the bridge.
4. **Make sure the tool/event actually fires** — the LLM has to decide to call
   `transfer_call`. Put a clear instruction in the prompt: "If the caller asks for
   a human, an agent, or a specialist, call the `transfer_call` tool immediately."
5. **Verify from the call logs** (see [Call logs](calls.md)): the parent call and
   the transfer leg. A transfer leg with `status: no_answer` means it fired but the
   destination did not pick up — not an SDK problem.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Agent says "I can't transfer calls" | The `transfer_call` tool is not on the live config. For single-prompt agents, set it with `AgentTools` (the legacy workflow doc does not take effect). |
| Transfer leg is `no_answer` / `timeout`, dur 0 | The destination number did not answer (or the caller hung up first). Use a number a human/agent will pick up. |
| Bridge connects but is silent | You are using **cold** transfer (direct connect, no music). For hold music during the handover, use **warm** transfer and set `on_hold_music`. |
| Tool never fires | The prompt does not tell the LLM when to transfer. Add an explicit instruction. |
