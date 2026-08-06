# Migrating to smallestai 6.0.0

6.0.0 renames the two product surfaces to industry-standard names:

- `atoms` → **`agents`** (the voice-agent platform)
- `waves` → **`speech`** (TTS / STT / voices)

The wire API, auth, method signatures, and observability are all unchanged. The
old names keep working as **deprecated aliases** that emit a `DeprecationWarning`,
so existing code runs untouched. The aliases are removed in the next major
(7.0.0) — do the rename at your convenience before then.

## What to change

| Before (≤5.x) | After (6.0.0) |
|---|---|
| `client.atoms.agents.list_agents()` | `client.agents.agents.list_agents()` |
| `client.atoms.calls.start_outbound_call(...)` | `client.agents.calls.start_outbound_call(...)` |
| `client.waves.text_to_speech(...)` | `client.speech.text_to_speech(...)` |
| `from smallestai.atoms.helpers import AgentTools` | `from smallestai.agents.helpers import AgentTools` |
| `from smallestai.waves.helpers import synthesize_to_file` | `from smallestai.speech.helpers import synthesize_to_file` |
| `import smallestai.atoms.crew` | `import smallestai.agents.crew` |

A blunt find-and-replace across your codebase is safe:

```bash
# client attributes and imports
grep -rl 'smallestai\.atoms\|\.atoms\.\|smallestai\.waves\|\.waves\.' . \
  | xargs sed -i '' -e 's/smallestai\.atoms/smallestai.agents/g' \
                    -e 's/smallestai\.waves/smallestai.speech/g' \
                    -e 's/\.atoms\./.agents./g' \
                    -e 's/\.waves\./.speech./g'
```

To find remaining deprecated usage, run Python with warnings visible:

```bash
python -W error::DeprecationWarning your_script.py
```

## Not affected

- `SmallestAI(api_key=...)` construction and the `SMALLEST_API_KEY` env var.
- Error types (`PlanNotEntitledError`, `BadRequestError`, …) and their import paths.
- Observability headers (`X-Source`, `X-Fern-SDK-Version`).
- The `SmallestAIEnvironment` fields (`atoms`, `waves`, `waves_ws`, `payment`) — these
  are wire/URL config, not the SDK surface, and are unchanged.

---

# Migrating to smallestai 5.0.0

5.0.0 makes the Atoms client surface consistent and discoverable. The wire API is
unchanged — these are **SDK-surface** renames plus packaging fixes. Most code that
authenticates via the `SMALLEST_API_KEY` env var and uses the documented methods needs
only the method-name updates below.

## Breaking — Atoms method renames (operationId leakage → verb-noun)
| Before (≤4.4.x) | After (5.0.0) |
|---|---|
| `client.atoms.agents.create_a_new_agent(...)` | `client.atoms.agents.create_agent(...)` |
| `client.atoms.agents.get_agent_by_id(id=...)` | `client.atoms.agents.get_agent(id=...)` |
| `client.atoms.agents.get_all_agents()` | `client.atoms.agents.list_agents()` |
| `client.atoms.agents.update_agent_metadata(...)` | `client.atoms.agents.update_agent(...)` |
| `client.atoms.calls.start_an_outbound_call(...)` | `client.atoms.calls.start_outbound_call(...)` |
| `client.atoms.agent_templates.get_agent_templates()` | `client.atoms.agent_templates.list_agent_templates()` |
| (no retrieval) | `client.atoms.calls.get(...)`, `client.atoms.calls.list(...)`, `client.atoms.calls.search(...)` |

Conversation cancel/retry/recording now live under `client.atoms.conversations.*`
(`cancel`, `cancel_queued`, `list_retry_attempts`). `update_workflow_configuration`
is marked **deprecated** (use the drafts flow).

## Breaking — helper rename
`from smallestai.atoms.helpers import Call` → **`CallAnalytics`** (it is analytics-only).
`Call` still works as a deprecated alias (emits `DeprecationWarning`) and will be removed in 6.0.0.

## Behavior changes (safer defaults)
- `OpenAIClient(api_key=None)` now **raises `ValueError`** at construction instead of
  warning and producing a silent, non-speaking agent. New: `OpenAIClient.electron()` factory.
- `smallestai.atoms.helpers` now imports cleanly on a fresh install (`requests` is a declared dependency).
- CLI: `agent-crew init --agent-id <id>` (non-TTY safe), `agent-crew chat --url <ws>`,
  `auth login` reads `SMALLEST_API_KEY` from env (no prompt).

## Auth
Construct with `SmallestAI(api_key=...)` or rely on the `SMALLEST_API_KEY` env var
(read automatically). No change from 4.4.x.
