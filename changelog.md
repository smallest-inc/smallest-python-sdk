## 5.4.2 - 2026-08-05

* **observability**: every request now sends `X-Source: smallest-python-sdk` so
  SDK-originated traffic is attributable in the backend, alongside other clients.
* **observability**: `X-Fern-SDK-Version` now reports the installed package
  version instead of a hardcoded `0.0.0`, making version adoption trackable.
* **fix**: `import smallestai; smallestai.__version__` no longer raises. The
  version lookup used the wrong distribution name (`smallest-ai` vs `smallestai`).
* **cli**: new `waves` commands — `tts`, `stt`, `voices`, `clones`.
* **cli**: new `campaigns` commands — `list`, `get`, `create`, `pause`,
  `resume`, `delete` — and `phone-numbers` commands — `list`, `search`, `rent`,
  `release`, `import-sip`. Billable/destructive actions prompt unless `--yes`.
* **fix**: `SMALLEST_BASE_URL` no longer crashes the CLI. The custom-endpoint
  path omitted the now-required `payment` url when building the environment.
* **docs**: corrected the text-to-speech method names in the reference
  (`synthesize_tts` / `tts.connect`, not the non-existent `text_to_speech`).

## 5.4.1 - 2026-08-04

* **crew**: stop generating after a handoff. Once a node emits a transfer or
  end-call event, `OutputCrewNode` latches and ignores further LLM requests. A
  fire-and-forget tool that emits the event records no tool_result, so the LLM
  would otherwise re-decide the same action on every subsequent request and
  re-fire it in a loop (e.g. a hold-message repeating for the whole transfer dial).

## 5.4.0 - 2026-08-04

Configure agent tools (transfer_call, end_call, ...) from code.

* **`atoms.helpers.AgentTools`**: new helper to read and write a single-prompt
  agent's tools by agentId, through the branch/revision versioning flow
  (draft -> publish -> make-live) so the change actually takes effect on live
  calls. Config is section-based, so the prompt and other tools are preserved
  (never wiped). `add_transfer_call(...)` configures a transfer, including
  `on_hold_music` so the caller hears audio while the transfer bridges instead of
  silence; `make_live=False` stages a revision without activating it. Optional-None
  fields are stripped (the API rejects nulls), and API error bodies are surfaced.
* Re-exported `Tool`, `SinglePromptConfig`, and `ToolTransferOption` from
  `smallestai.atoms.helpers` (they are not exported from `atoms.types`).
* **crew (silent agent fix)**: `OutputCrewNode` now seeds its context from the
  authoritative message list carried on the LLM-request event, instead of relying
  only on separately-accumulated transcript events. Those could race the request or
  be dropped, leaving the context empty — the custom LLM then errored on "no
  non-system message" and the agent went silent for the whole call (greeting once,
  never responding, never transferring). The node's own system prompt is preserved.
* **crew (greeting lifecycle)**: send `AgentReady` before starting nodes so a
  greeting emitted in `start()` works, and add an `on_event` hook so a subclass can
  react to events without accidentally silencing the framework routing.
* **crew**: `SDKAgentTransferConversationEvent.on_hold_music` is now optional
  (defaults to `None`). It was declared `Optional[...]` but without a default, so
  it was effectively required — every crew transfer had to pass it (even as
  `None`) or event construction raised a `ValidationError`. Callers that want
  audio during the transfer bridge still pass `ringtone` / `relaxing_sound` /
  `uplifting_beats`. Note: `on_hold_music` applies to warm transfers; cold transfer
  is a direct connect with no hold-music window.
* **CLI** (`smallestai calls`): new `list`, `get`, `transcript`, and `recording`
  subcommands to inspect call logs, details, transcripts, and recording URLs from
  the terminal (read-only, dogfoods `client.atoms.calls`). Each supports `--json`.

## 5.3.4 - 2026-07-31

Corrects the deploy message. No API changes.

* **CLI** (`smallestai agent-crew deploy`): drop the "first call can be silent, try
  again" line from the post-deploy message. The crew is engaged at call time on the
  current platform, so that guidance was misleading. The message now just says to
  wait for the build to show Live before the first call.

## 5.3.3 - 2026-07-30

CLI deploy now reports real build status, and a hand-written README. No API changes.

* **CLI** (`smallestai agent-crew deploy`): after upload, the command polls the build
  to a terminal state (SUCCEEDED / failed) instead of returning at "queued", and on
  success points to `agent-crew builds` -> Make Live with a note that the first call
  after Make Live can need a few seconds while the pod warms up.
* **README**: replaced the generated boilerplate with a hand-written front door
  (agents, Waves TTS/STT, agent crew with a custom LLM, CLI). Added to `.fernignore`
  so regeneration no longer overwrites it.

## 5.3.2 - 2026-07-30

Corrects the agent-crew deploy layout warning. No API or behaviour changes.

* **CLI** (`smallestai agent-crew deploy`): the pre-deploy check no longer claims a `src/`
  layout or a `pyproject.toml` project fails the cloud build. Both build and run (verified end
  to end). The check is now a short note: flat directory with `server.py` + `requirements.txt`
  at the root is the simplest, best-tested path; if you use a `pyproject.toml` with no
  `requirements.txt`, declare every runtime dependency in it.

## 5.3.1 - 2026-07-29

Billing read endpoints, a call-log type fix, and clearer agent-crew deploy warnings. Additive; no breaking changes.

* **Billing** (new `client.atoms.billing`): `get_balance`, `get_ledger`, `get_usage_breakdown`,
  `list_invoices`, `get_invoice_pdf` (read-only credit and invoice endpoints under `/payment/v1`).
* **Fix**: `calls.get` / `calls.list` transcript-turn `timestamp` is typed as a string (ISO-8601),
  matching what the API returns. Previously typed as a number, which triggered a deserialization
  warning.
* **CLI DevX** (`smallestai agent-crew deploy`): a pre-deploy layout check warns on a `src/` layout,
  a nested entry point, or a `pyproject.toml` with no `requirements.txt` (all fail the cloud build);
  and the environment-variable warning now points to the working path (ship a `.env` at the project
  root and call `load_dotenv()`; it deploys with your code) instead of just saying it is not propagated.

## 5.3.0 - 2026-07-28

Unified speech-to-text namespace (breaking), voice cloning, Electron LLM, webhook update.

* **Breaking — unified STT**: legacy `client.waves.transcribe_pulse(...)` and
  `client.waves.pulse_stt_streaming(...)` are removed. Use `client.waves.speech_to_text.transcribe(...)`
  (file/batch, typed `model` pulse|pulse-pro + `language`) and `client.waves.speech_to_text.stream(...)`
  (live WebSocket). The `smallestai.waves.types.transcribe_pulse_*` types are gone. No deprecation alias.
* **Fix — STT/Electron routing**: `speech_to_text.*` and `electron.complete` were generated against the
  atoms base and 404'd; both now resolve to the waves base. Live-verified against `api.smallest.ai`.
* **Typed streaming helper** (`from smallestai.waves.helpers import stream_speech_to_text`): typed
  handshake params for the full STT param set incl. keyword boosting (`keywords`), redaction, VAD,
  diarization; booleans and list params serialized for you; passthrough via `additional_query_parameters`.
* **Additive**: `waves.create_voice_clone` / `list_voice_clones`, `waves.electron.complete`,
  `atoms.webhooks.update`.
* Verified live end-to-end against `api.smallest.ai` (batch transcribe, live stream with keyword
  boosting, electron completion).

## 5.2.0 - 2026-07-24

Agent Versioning v2 (branch/revision API) + new namespaces, plus an ergonomic versioning helper.
Additive; generator pinned to 5.12.12.

* **Agent Versioning v2** — new `agent_versioning_branches` (`create_branch`, `list`, `get`,
  `rename`, `archive`, `make_live`, `get_draft`, `update_draft`, `discard_draft`, `publish_draft`,
  `cancel_publish`, `test_call`) and `agent_versioning_revisions` (`list`, `get`, `get_history`,
  `restore`, `diff`) clients. `update_draft` takes typed config kwargs (`global_prompt`,
  `first_message`, `synthesizer`, …). The v1 `agent_versioning_drafts`/`agent_versioning_versions`
  write endpoints are deprecated under the branch model (they return `409
  versioning_v2_migration_required`).
* **Versioning helper** (`from smallestai.atoms.helpers import Versioning`): `publish_and_wait` /
  `wait_for_commit` (publishing runs a security scan asynchronously — this polls until the revision
  is `published`), `edit_and_publish` (one-call config edit), and typed conflict handling
  (`DraftConflictError`, `MigrationRequiredError`, `BaseRevisionUnavailableError`).
* **New namespaces**: `call_actions`, `integrations`, `concurrency`, `disposition_metric_templates`,
  `realtime`.
* Generator: `exclude_types_from_init_exports` flipped to `false`.
* Verified live end-to-end against `api.smallest.ai` (fork → edit → publish → scan → test-call →
  make-live → restore), via both raw endpoints and the generated SDK.

## 5.1.1 - 2026-07-15

Patch — fix the streaming-TTS compat shim (`WavesStreamingTTS`/`TTSConfig`).

* The legacy per-model endpoint `wss://.../waves/v1/lightning-v3.1/get_speech/stream`
  **retired 2026-07-14**, which broke `WavesStreamingTTS` on 5.0.0/5.1.0. The shim now
  targets the unified `wss://api.smallest.ai/waves/v1/tts/live`.
* `TTSConfig` gains a `model` field (default `lightning_v3.1`; set `lightning_v3.1_pro`
  for the Pro pool) — the model was previously encoded in the URL path.
* Verified live end-to-end (streams PCM chunks from `/tts/live`). No other changes.

## 5.1.0 - 2026-06-22

Additive completeness, naming, and spec-correctness release (generator pinned to 5.12.12).
The only breaking changes are the verb-noun method renames below; the deprecated
model-lineup cleanup is deferred to a later release.

* **New endpoints**: `agents.create_with_ai`, `agents.list_call_logs`,
  `agents.get_widget_config`/`update_widget_config`, `agents.get_prompt_config`,
  `organization.get_account_details`/`update_name`, `user.get_subscription`,
  `campaigns.export_logs`, plus a new `dnc.list` namespace.
* **Method names** cleaned to verb-noun across more namespaces: `agent_versioning_drafts`
  (`create_draft`, `publish_draft`, `update_draft_config`, …), `agent_versioning_versions`
  (`activate_version`, `compare_version_metrics`, `update_version_metadata`),
  `campaigns`/`audience`/`webhooks`, and `knowledge_base`/`phone_numbers`
  (`list`/`create`/`get`/`delete`/`rent`/`release`/`search_rentable`/`import_sip`/
  `extract_sitemap_urls`/`scrape_urls`).
* **Agent schema completeness**: 18 previously-untyped config fields now typed on the agent
  (e.g. `allow_inbound_call`, `phone_number`, `voice_mail_detection_config`,
  `smart_turn_config`, `session_timeout_config`, `pronunciation_dicts`).
* **`agent_templates`**: `_id` (Mongo ObjectId) and `id` (slug) are now distinct fields —
  `.object_id` and `.id` (no data loss).
* **Live transcripts**: the `metrics` SSE event is typed as an array (was silently dropped).

Breaking: the verb-noun renames above remove the old operationId-style names. See MIGRATION.md.

## 5.0.0 - 2026-06-19

First release from the canonical `smallest-inc/smallest-python-sdk` repo. SDK-surface
consistency + packaging/correctness fixes. See MIGRATION.md.

* **Atoms method names** standardized to verb-noun (e.g. `create_agent`, `get_agent`,
  `list_agents`, `update_agent`, `start_outbound_call`, `list_agent_templates`).
* **`calls`** namespace gains `get` / `list` / `search`; conversation cancel/retry/recording
  under `conversations.*`. `update_workflow_configuration` deprecated.
* **`Call` → `CallAnalytics`** (deprecated alias kept).
* **`OpenAIClient`** raises on missing key; adds `.electron()` factory.
* **`requests`** is now a runtime dependency (helpers import cleanly).
* **CLI**: `init --agent-id`, `chat --url`, env-aware `auth login`.
* **New helpers** `smallestai.atoms.helpers.as_page(...)` (one shape for any list response) and `require_id(...)` (rejects empty ids) — #25 / #18.

## 4.4.7 - 2026-05-20

Two related additions: a customer-defined event for the call's Events
timeline, and a four-layer error propagation system that closes the
silent-failure hole where a deployed crew's user code (e.g.
`SentimentAnalyzer` with a missing `OPENAI_API_KEY`) raised inside
`process_event`, the exception was caught by `try/except`, and the
only signal was a loguru line in pod stdout that nobody read.

### Custom events on the call timeline

* **New event: `SDKAgentLogEvent`
  (`smallestai.atoms.crew.events.SDKAgentLogEvent`,
  `type="agent.log"`).** Customer-defined event for the call's Events
  timeline. Any crew node — background or output — emits these to
  publish arbitrary state to the orchestrator. The platform stores
  each one in ClickHouse via the relay (RabbitMQ → ClickHouse) and
  surfaces it in the Events tab of the call detail page, alongside
  transcripts, tool calls, and lifecycle markers. Two fields:
  `name: str`, `payload: Dict[str, Any]`.

  Example::

      from smallestai.atoms.crew.events import SDKAgentLogEvent
      from smallestai.atoms.crew.nodes import BackgroundCrewNode

      class SentimentAnalyzer(BackgroundCrewNode):
          async def process_event(self, event):
              ...  # classify
              await self.send_event(SDKAgentLogEvent(
                  name="sentiment",
                  payload={"sentiment": "frustrated", "frustration_count": 3},
              ))

  Output nodes can use it too — e.g. emitting `name="escalation.triggered"`
  when the agent decides to transfer the call.

### Error propagation (four layers)

* **`SDKAgentErrorEvent` schema extended.** New fields:
  `severity: Literal["warning", "fatal"]` (default `"warning"`) and
  `payload: Dict[str, Any]` (free-form). The orchestrator uses
  `severity="fatal"` to mark the call as failed and populate
  `failureReason` on the calllog; `"warning"` is recorded on
  `errors[]` without failing the call. The SDK auto-populates payload
  with `node_name`, `error_class`, and `traceback` when emitting on
  your behalf; manual emissions can add any custom keys (e.g.
  `customer_id`, `request_id`). Backward-compatible with the existing
  message-only emitter — both new fields have defaults.

* **Auto-emit on user-code exceptions in `nodes/base.py`.** The
  `__process_event_handler_loop` previously wrapped the entire `while`
  loop in one try/except — meaning a single exception killed all
  further event processing on that node. Now each `process_event`
  call is wrapped per-event, with the exception auto-emitting an
  `SDKAgentErrorEvent` upstream. Severity is auto-selected by node
  type: `BackgroundCrewNode` → `"warning"` (observer, call continues);
  every other node type → `"fatal"` (output node, call fails).
  Subclasses can override `_error_severity()` to change the default.

* **`OutputCrewNode._handle_llm_request` error emission enriched.**
  The existing try/except around `generate_response` already emitted
  `SDKAgentErrorEvent` but only set `message`. Now also sets
  `severity="fatal"` and a payload with `node_name`, `error_class`,
  `traceback`.

* **`/ready` endpoint + `_validate_startup()` in `AtomsCrewApp`.**
  New readiness probe at `GET /ready`. Returns 503 with a structured
  reason until the FastAPI startup hook has successfully dry-run the
  `setup_handler` against a no-op session. Catches `__init__` failures
  (missing env vars in `OpenAIClient.__init__`, bad imports, etc.)
  before the pod accepts WebSocket connections. `/health` stays as a
  liveness signal (always 200 if the process is up).

* **Pre-deploy env var scan in the CLI.** `smallestai agent-crew
  deploy` now AST-walks every `.py` file under the build directory
  before zipping and prints a warning listing every env var the code
  reads via `os.getenv("X")` / `os.environ["X"]` / `os.environ.get("X",
  …)`. `SMALLEST_API_KEY` is suppressed (the platform always sets it).

Companion: `smallest-inc/pipecat#762` (consolidated) — adds the
matching `agent.log` + `agent.error` handling, publishes both to the
event bus for relay → RabbitMQ → ClickHouse, and terminates the call
on `severity="fatal"`. Without that PR deployed, events reach the
orchestrator but the relay → ClickHouse → Events tab pipeline isn't
yet wired (UI integration is a separate atoms-platform PR).

## 4.4.6 - 2026-05-20

* **Follow-up cleanup after the 4.4.5 `token=` → `api_key=` rename.**
  The wire-test fixture (`tests/wire/conftest.py`) was still calling
  `SmallestAI(token="test_token")`, which broke the test suite on `main`
  immediately after 4.4.5 shipped. Switched to `api_key=`. Also
  refreshed the auto-generated `README.md` and `reference.md` so every
  example uses `api_key="<api_key>"` instead of `token="<token>"` —
  the next Fern regen will reproduce both files identically (after
  the companion `generators.yml` change in
  smallest-ai-documentation#156 lands).

## 4.4.5 - 2026-05-20

* **`SmallestAI()` / `AsyncSmallestAI()` now take `api_key=` (was `token=`)
  and read `SMALLEST_API_KEY` from the environment (was `SMALLEST_AI_TOKEN`).**
  Both names — the kwarg and the env var — were the odd ones out:
  - Hand-written helpers (`smallestai.atoms.helpers.{call,campaign,audience,kb}`)
    take `api_key=` and read `SMALLEST_API_KEY`
  - Every cookbook `.env.sample` exports `SMALLEST_API_KEY`
  - The dashboard UI calls the value an "API key" at
    `app.smallest.ai/dashboard/api-keys`

  Now the whole SDK speaks one language: `client = SmallestAI(api_key="sk_…")`
  or set `SMALLEST_API_KEY` in the environment.

  **Breaking:** `SmallestAI(token=…)` no longer works — the kwarg was renamed,
  not aliased. Same for `SMALLEST_AI_TOKEN` — it is no longer read. Both
  names shipped only in 4.4.x and were undocumented anywhere user-facing,
  so the dropped without a deprecation window.

  Companion docs/Fern PR (smallest-ai-documentation#156) updates
  `generators.yml` so the next Fern regen reproduces this naturally.
  This is a hand-patch on top of the Fern-generated `client.py` and
  will be replaced on that regen with an equivalent result.

## 4.4.4 - 2026-05-20

* **`smallestai.atoms.helpers` modules now use the new API host.**
  `DEFAULT_BASE_URL` in `helpers.{campaign,audience,kb,call}` updated
  from `https://atoms.smallest.ai/api/v1` to
  `https://api.smallest.ai/atoms/v1`, matching the CLI fix in 4.4.3.
  Verified all four helpers' actual paths (`/campaign`, `/audience`,
  `/knowledgebase`, `/conversation`) return 401 at the new host —
  routes exist, auth required, behavior matches the old host.
  Docstrings updated to reference the new default.

## 4.4.3 - 2026-05-20

* **CLI now talks to the new Atoms API host.** The CLI's HTTP client
  (`smallestai/cli/lib/atoms.py`) used to call
  `https://atoms-api.smallest.ai/api/v1/...`, which had started returning
  HTTP 400 on POSTs to `/sdk/agents/{id}/builds` (breaking `smallestai
  agent-crew deploy`). Updated to
  `https://api.smallest.ai/atoms/v1/...` — host + path-prefix change.
  All eight URLs in the file (`/agent`, `/user`, the five builds
  endpoints, and the streaming endpoint) updated consistently.

* **CLI display URLs updated to `app.smallest.ai`.** The login prompt now
  points to `https://app.smallest.ai/dashboard/api-keys` (was
  `console.smallest.ai/apikeys`), and the empty-agents message points
  to `https://app.smallest.ai/dashboard` (was `console.smallest.ai`).
  Two-line behavior-only change in `cli/auth.py` and `cli/agent_crew.py`.

* **`DEFAULT_BASE_URL` in `smallestai.atoms.helpers` (campaign, audience,
  kb, call) is unchanged at `https://atoms.smallest.ai/api/v1`** — those
  helpers still resolve correctly via that host (it 301-redirects to the
  new API for the helper routes). The CLI change above is specifically
  for the `/sdk/agents/...` endpoints which now require the new host.

## 4.4.2 - 2026-05-20

* **`agent-swarm` → `agent-crew` rename.** The framework name pivots
  from "swarm" to "crew" — the concept stays the same (multi-node
  orchestration that powers a platform agent's LLM brain), only the
  vocabulary changes. Hard rename, no backwards-compat shims:

  | Before | After |
  | --- | --- |
  | `smallestai.atoms.swarm.*` | `smallestai.atoms.crew.*` |
  | `SwarmNode` | `CrewNode` |
  | `OutputSwarmNode` | `OutputCrewNode` |
  | `BackgroundSwarmNode` | `BackgroundCrewNode` |
  | `SwarmSession` | `CrewSession` |
  | `AtomsSwarmApp` | `AtomsCrewApp` |
  | `smallestai agent-swarm {init,deploy,chat,builds}` | `smallestai agent-crew ...` |
  | `smallestai/cli/agent_swarm.py` + `initialise_agent_swarm_app` | `smallestai/cli/agent_crew.py` + `initialise_agent_crew_app` |

  Code on 4.4.1 must update imports + CLI invocations to upgrade.

* **Unchanged:** SDK event class names (`SDKAgent*Event`) — wire
  protocol shared with pipecat, deferred with the atoms-platform +
  pipecat side.

## 4.4.1 - 2026-05-19

* **CLI shipped in the published wheel for the first time.** Previous
  releases declared `smallestai = "smallestai.cli.main:main"` in
  `pyproject.toml` but the `smallestai.cli` subpackage was missing
  from the published wheel — `pip install smallestai` produced no
  working `smallestai` binary. The CLI module is now part of this
  repo (with `.fernignore` protection against Fern regen) and ships
  in 4.4.1. `pip install smallestai && smallestai --help` works.

* **`agent` → `agent-swarm` rename across the framework.** The word
  "agent" was overloaded between platform agents and the multi-node
  SDK construct. Hard rename across module path, classes, and CLI.
  (Superseded in 4.4.2 — see above.)

* **Python floor bumped to 3.9** for new CLI deps (`typer >= 0.20`,
  `tomli-w >= 1.2`).

* **New runtime dependencies** for the CLI: `typer`, `rich`,
  `questionary`, `tomli`, `tomli-w`.

## 4.4.0 - 2026-05-11

* **Restore `WavesStreamingTTS` and `TTSConfig` exports under
  `smallestai.waves`** that shipped in 4.3.1 but were dropped during
  the Fern migration. Customers on the legacy
  `from smallestai.waves import WavesStreamingTTS, TTSConfig` pattern
  no longer hit `ImportError` on upgrade.
* **WebSocket endpoint corrected to Lightning v3.1.** Previous 4.3.x
  releases that exposed `WavesStreamingTTS` hardcoded the deprecated
  Lightning v2 URL — that was a bug. The shim now connects to
  `wss://api.smallest.ai/waves/v1/lightning-v3.1/get_speech/stream`
  and supports 44.1 kHz output.
* `TTSConfig` adds `pronunciation_dicts: Optional[Sequence[str]]` so
  callers can pass per-call pronunciation dictionary IDs (Lightning
  v3.1 feature).
* `TTSConfig` drops `consistency` (v2-only — silently ignored on
  v3.1; kept as a keyword arg in the dataclass would mislead users).
* New dependency: `websocket-client >= 1.6.0` (used by the
  `WavesStreamingTTS` shim).
* New code should prefer the namespaced Fern client:
  `client.waves.lightning_v31tts.connect(...)` for streaming TTS and
  `client.waves.synthesize_lightning_v31(...)` for sync REST.

## 3.0.0 - 2026-03-17
* Multiple deprecated modules have been removed from the SDK, including `lightning`, `lightning_large`, `lightning_v2`, `pronunciation_dictionaries`, `speech_to_text`, `text_to_speech`, `voice_cloning`, and `voices`. Applications using these modules should migrate to the supported alternatives: `lightning_asr_streaming`, `lightning_v2tts`, `lightning_v31tts`, `pulse_stt_streaming`, `streaming_tts`, and `asr_streaming`.
* The Lightning Large API client has been removed entirely, including all speech synthesis methods. Applications using `RawLightningLargeClient` or `AsyncRawLightningLargeClient` will need to migrate to alternative speech synthesis APIs.
* The Lightning v2 client has been removed from the SDK. Applications using `client.lightning_v2.synthesize_lightningv2speech()` or `client.lightning_v2.stream_lightningv2speech()` will need to migrate to the newer Lightning API endpoints.
* The deprecated `lightning_v2.raw_client` module and `pronunciation_dictionaries` module have been removed. Applications using `RawLightningV2Client`, `AsyncRawLightningV2Client`, or pronunciation dictionary functionality should migrate to the updated API surface or contact support for migration guidance.
* The pronunciation dictionaries feature has been removed from the SmallestWaves SDK. The `client.pronunciation_dictionaries` attribute and all related methods (`get_pronunciation_dicts`, `create_pronunciation_dict`, `update_pronunciation_dict`, `delete_pronunciation_dict`) are no longer available in both sync and async clients.
* The `SpeechToTextClient` and `AsyncSpeechToTextClient` classes have been removed, including their `lightning()` and `pulse()` methods. Code using these clients will need to be updated to use the new consolidated speech processing API.
* The speech-to-text and text-to-speech modules have been removed from the SDK. Applications using RawSpeechToTextClient, AsyncRawSpeechToTextClient, or any related speech processing types will need to find alternative solutions or use a previous version of the SDK.
* The text-to-speech and voice-cloning modules have been removed from the SDK. Applications using `client.text_to_speech.synthesize_lightning_v31speech()`, `client.text_to_speech.stream_lightning_v31speech()`, or any voice cloning functionality will need to be updated to use alternative methods or API endpoints.
* The `voice_cloning` and `voices` modules have been removed. Applications using `client.voice_cloning.add_voice_to_model()`, `client.voice_cloning.get_cloned_voices()`, `client.voice_cloning.delete_voice_clone()`, or `client.voices.get_waves_voices()` will need to be updated to use alternative APIs or remove this functionality.
* The `send_asr_audio_request_message()` method has been renamed to `transcribe_streaming_asr()` in both synchronous and asynchronous ASR streaming socket clients. Replace existing calls to `send_asr_audio_request_message(message)` with `transcribe_streaming_asr(message)` - the method signature and behavior are otherwise identical.
* The SDK has been restructured with a new streamlined API. Instead of accessing functionality through nested client properties (like `client.pronunciation_dictionaries.get_all()`), all methods are now available directly on the main client (`client.get_pronunciation_dicts()`). The property-based clients (`pronunciation_dictionaries`, `lightning`, `lightning_large`, `lightning_v2`, `voices`, `voice_cloning`, `speech_to_text`, `text_to_speech`) have been removed. Update your code to use the new direct method names available on `SmallestWaves` and `AsyncSmallestWaves` clients.
* The SDK now includes a comprehensive raw client (RawSmallestWaves) providing direct access to the Waves API with text-to-speech synthesis, voice management, pronunciation dictionaries, and speech transcription capabilities. The client supports multiple Lightning models, both streaming and Server-Sent Events (SSE) synthesis modes, voice cloning, and advanced transcription features with speaker analysis.
* New transcribe Lightning and Pulse response types are now available, providing structured access to transcription results with optional age, gender, and emotion detection data.

## 2.0.0 - 2026-03-14
* The `stream_lightning_large_speech()` and `stream_lightningv2speech()` methods now return iterators that yield SSE events instead of simple HTTP responses. The return type has changed from `HttpResponse[None]` to `Iterator[HttpResponse[Iterator[Any]]]`. Existing code using these methods will need to be updated to handle the new iterator-based streaming interface with proper context manager usage.
* Streaming text-to-speech methods now return iterators that yield Server-Sent Events, enabling real-time processing of audio chunks. WebSocket connection methods now accept an optional authorization parameter for enhanced authentication control.

## 4.3.3 - 2026-03-11
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 1.1.0 - 2026-03-02
* feat: add RFC 2822 datetime parsing support
* Add comprehensive RFC 2822 datetime parsing capabilities to handle various datetime formats in API responses. This enhancement enables parsing of standard HTTP date headers and email-style date formats while maintaining backward compatibility.
* Key changes:
* Add parse_rfc2822_datetime function with fallback to ISO 8601 parsing
* Implement Rfc2822DateTime class with Pydantic V1 and V2 compatibility
* Support automatic conversion from RFC 2822 strings to datetime objects
* Include email.utils.parsedate_to_datetime for robust date parsing
* 🌿 Generated with Fern

## 1.0.0 - 2026-03-02
* feat: implement proper streaming support for speech synthesis APIs
* Refactor streaming methods across all Lightning models to return proper iterators with Server-Sent Events (SSE) support. This change transforms static placeholder methods into functional streaming APIs that yield audio chunks in real-time.
* Key changes:
* Update return types from None to Iterator/AsyncIterator for all stream methods
* Implement context manager pattern with proper resource cleanup
* Add SSE event parsing with robust error handling for malformed events
* Replace simple request calls with streaming context managers
* Update documentation examples to show proper iterator usage patterns
* 🌿 Generated with Fern

## 0.0.167 - 2026-02-27
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.1.1 - 2026-02-25
* chore: update Fern CLI version to 3.88.1
* This change updates the Fern CLI tooling version used for SDK generation from version 3.88.0 to 3.88.1, ensuring the project uses the latest patch release with potential bug fixes and improvements.
* Key changes:
* Update cliVersion from 3.88.0 to 3.88.1 in metadata.json
* Maintain existing generator configuration and versions
* Ensure compatibility with latest Fern CLI tooling
* 🌿 Generated with Fern

## 0.1.0 - 2026-02-25
* feat: add authorization support and fix websocket types
* Add optional authorization parameter to websocket connect methods across all TTS and STT clients to enable Bearer token authentication. Fix incorrect websocket response types and method names in socket clients.
* Key changes:
* Add optional authorization parameter to all connect() methods in client and raw_client classes
* Fix LightningV2TtsSocketClientResponse type from Request to Response message
* Fix LightningV31TtsSocketClientResponse type from Request to Response message
* Rename send methods from send_response_message to send_request_message
* Update sample rate documentation to specify supported values
* Update Fern CLI version from 3.85.2 to 3.88.0
* Update certifi dependency version
* 🌿 Generated with Fern

## 0.0.101 - 2026-02-24
* chore: update CLI version to 3.85.2
* Updates the Fern CLI version in metadata.json from 3.75.0 to 3.85.2. This is a routine dependency update that includes the latest CLI improvements and bug fixes, ensuring compatibility with the current Fern ecosystem.
* Key changes:
* Update cliVersion from 3.75.0 to 3.85.2 in .fern/metadata.json
* Maintains existing generator configuration settings
* Preserves all other metadata properties unchanged
* 🌿 Generated with Fern

## 0.0.100 - 2026-02-19
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.99 - 2026-02-18
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.98 - 2026-02-18
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.96 - 2026-02-13
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 1.0.2 - 2026-02-13
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 1.0.1 - 2026-02-13
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 1.0.0 - 2026-02-13
* fix: correct message type mappings in TTS socket clients
* Fix inconsistent message type usage in Lightning V2 and V31 TTS socket clients where request and response message types were incorrectly swapped in type hints and method signatures.
* Key changes:
* Fix LightningV2TtsSocketClientResponse type hint to use RequestMessage instead of ResponseMessage
* Rename send_lightning_v_2_tts_request_message to send_lightning_v_2_tts_response_message with correct parameter type
* Fix LightningV31TtsSocketClientResponse type hint to use RequestMessage instead of ResponseMessage
* Rename send_lightning_v_31_tts_request_message to send_lightning_v_31_tts_response_message with correct parameter type
* 🌿 Generated with Fern

## 0.0.94 - 2026-02-13
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.86 - 2026-02-12
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.58 - 2026-02-12
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.46 - 2026-02-05
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.43 - 2026-02-04
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.40 - 2026-02-04
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.0.31 - 2026-02-03
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.2.0 - 2026-01-30
* feat: update Lightning v3.1 output formats and add new model option
* Updates the Lightning v3.1 API to support revised audio output formats and introduces a new model variant for improved voice generation capabilities.
* Key changes:
* Replace "mp3" and "mulaw" with "ulaw" and "alaw" formats in Lightning v3.1 output options
* Add "lightning-v3.1" model option to GetWavesVoicesRequestModel for enhanced voice synthesis
* Maintain backward compatibility with existing model variants
* 🌿 Generated with Fern

## 0.1.2 - 2026-01-28
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.1.1 - 2026-01-28
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

## 0.1.0 - 2026-01-28
* feat: add Lightning V3.1 TTS model support and update ASR endpoint
* This update introduces support for the new Lightning V3.1 text-to-speech model with enhanced capabilities including multi-language support (English and Hindi), customizable audio output formats, and improved speech generation controls. Additionally, the ASR service has been migrated from Lightning to Pulse model for better performance.
* Key changes:
* Add complete Lightning V3.1 client implementation with synthesize and stream endpoints
* Support for multiple audio formats (PCM, MP3, WAV, μ-law) and customizable sample rates
* Multi-language number pronunciation support (English/Hindi)
* Speech speed control and pronunciation dictionary integration
* Migrate ASR service from Lightning model to Pulse model
* Update error response models with improved documentation
* Fix speech-to-text response field mapping for transcription data
* 🌿 Generated with Fern

## 0.0.7 - 2026-01-28
* SDK regeneration
* Unable to analyze changes with AI, incrementing PATCH version.

