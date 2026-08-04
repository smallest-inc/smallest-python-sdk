# Method cheatsheet

The names you'll actually call. When unsure, list them:
`[m for m in dir(client.atoms.agents) if not m.startswith("_")]`.

## Agents — `client.atoms.agents`

| Do this | Call |
|---|---|
| Create an agent | `create_agent(name=..., workflow_type="single_prompt", first_message=...)` → `.data` is the **id string** |
| Get one | `get_agent(id=...)` → `.data` |
| List | `list_agents()` (wrap with `helpers.as_page`) |
| Archive | `archive_agent(id=...)` |
| Duplicate | `duplicate_agent(id=...)` |
| Create from a brief | `create_with_ai(description=...)` |
| Call logs for an agent | `list_call_logs(id=...)` |

## Tools / transfer — `atoms.helpers.AgentTools`

| Do this | Call |
|---|---|
| Add a transfer | `add_transfer_call(agent_id, number=..., transfer_type="cold_transfer"|"warm_transfer", on_hold_music=...)` |
| Set/merge tools | `set_tools(agent_id, [...], replace=False, make_live=True)` |
| Read live tools | `get_tools(agent_id)` |
| Remove a tool | `remove_tool(agent_id, name)` |

Do **not** set tools via `create_agent`/`update_agent` (no tools param) or the
legacy workflow doc (ignored on live calls).

## Calls — `client.atoms.calls`

| Do this | Call |
|---|---|
| Place outbound | `start_outbound_call(agent_id=..., phone_number=..., from_product_id=...)` |
| Get one | `get(id="CALL-...")` |
| List | `list(agent_ids=..., limit=..., call_types=...)` → `.data.logs` |
| Search | `search(...)` |

## Versioning — `client.atoms.agent_versioning_branches` / `...revisions`

Branch/revision model (v2). The v1 `agent_versioning_drafts` /
`agent_versioning_versions` are deprecated (return 409). For tools/prompt, prefer
`AgentTools` / the versioning helper.

## Crew — `smallestai.atoms.crew`

| Thing | Import |
|---|---|
| Node base | `from smallestai.atoms.crew.nodes import OutputCrewNode` |
| Transfer event | `from smallestai.atoms.crew.events import SDKAgentTransferConversationEvent, TransferOption, TransferOptionType` |

## Waves (speech) — `client.waves`

| Do this | Call |
|---|---|
| Text to speech | `waves.text_to_speech.*` |
| Speech to text (file) | `waves.speech_to_text.transcribe(...)` |
| Speech to text (stream) | `waves.speech_to_text.stream(...)` |
| Voice cloning | `waves.create_voice_clone(...)` / `list_voice_clones()` |
