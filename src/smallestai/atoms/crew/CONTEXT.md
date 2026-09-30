# Agent Crew — CONTEXT

Domain model and invariants for the code-first agent framework (`smallestai.atoms.crew`).
Read this before writing tests or changing crew code, so names and seams match the domain.

## Premise (what must work, end to end)

A developer writes a crew agent in Python, brings their own LLM, and it runs a real voice
call correctly: STT to their LLM turn to TTS to telephony, with tools firing, background
observer nodes, interruptions, and the node graph. Deployable via `agent-crew deploy` and
testable locally via `agent-crew chat`. This premise working is the priority. Feature gaps
come after it is proven.

## Domain vocabulary

- **CrewApp** (`AtomsCrewApp`) — the entrypoint. `get_agent(env, call_request)` builds a
  `CrewSession` graph for one call. `app.run()` is the FastAPI + WebSocket harness.
- **CrewSession** — one per live call. Owns the node graph, wired `RootNode` to your nodes
  to `SinkNode` (all leaf nodes connect to the sink). API `add_node`, `add_edge`.
- **CrewNode** (base) — a processing unit. Lifecycle `start` / `stop`, event flow
  `process_event` / `queue_event` / `send_event`, graph `add_child` / `add_parent` /
  `children` / `parents`, plus `is_interruptible` and `task_manager`.
- **OutputCrewNode** — produces user-facing speech. Subclass implements
  `generate_response()` (async iterator of text). Also `speak(text)` and the `on_event` hook.
- **BackgroundCrewNode** — observes silently (sentiment, compliance), no user output.
- **Events** — typed `SDKEvent`. `EventType` covers `system.init`, `system.llm.request`,
  `system.user.started_speaking` / `stopped_speaking`, `system.control.interrupt`,
  `agent.ready`. `EventDirection` is downstream / upstream. `ConversationType` is telephony
  inbound / outbound, chat, webcall, supervisor_agent. `EventCodec` encodes / decodes the wire.
- **Tools** — `@function_tool` + `ToolRegistry`. Tool calls raise `tool_call` events; results
  route back to the LLM; parallel tool calls keep their `call_id`.
- **LLM** — `OpenAIClient`, bring-your-own against any OpenAI-compatible endpoint.
- **Deploy** — `agent-crew deploy` (build then Make Live), `agent-crew chat` (local run).

## Seams (test only here — public boundaries)

1. Imports — every documented crew import resolves.
2. `AtomsCrewApp` / `get_agent` / `app.run()`.
3. `CrewSession` graph — `add_node` / `add_edge`, root to nodes to sink.
4. `CrewNode` lifecycle — start/stop, event flow, graph edges, `is_interruptible`.
5. `OutputCrewNode` — `generate_response` streams, `speak` voices, `on_event`.
6. `BackgroundCrewNode` — observes without producing output.
7. Event model — `EventType`, `EventDirection`, `ConversationType`, `EventCodec` round-trip.
8. `OpenAIClient` — BYO-LLM streaming.
9. `@function_tool` / `ToolRegistry` — register, call, result routing, param passing.
10. Deploy / local — `agent-crew deploy`, `agent-crew chat`.
11. Live E2E — full pipeline on a real call.

## Invariants (must not break)

- Every documented import resolves (short and long paths). Regression: crew `__init__`
  once exported nothing.
- `generate_response` streams text; `speak()` actually voices. Regression: `speak()` not voiced.
- Session is ready before nodes start (startup ordering); no spurious startup ERROR logs.
- An interrupt cancels output when the node `is_interruptible`.
- A tool call routes its result back to the LLM; a parallel tool failure keeps its `call_id`.
- `EventCodec.encode` then `decode` round-trips every `EventType`.
- No hallucinated symbols: names, signatures, and params match the public API exactly.

## Edge cases to force red

tool raises, tool returns None/garbage, LLM empty or partial stream, barge-in mid-turn,
socket drop / reconnect, malformed inbound event, duplicate node name, unknown import
attribute, terminal handoff guard, wrong param type into a tool.
