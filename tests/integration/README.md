# SDK live integration suite

Real calls against a real environment — the common baseline we run on every SDK
change so we know the core surface still works, plus a feature test for the thing
we just shipped. No mocks, no WireMock. Gated by env vars, so the normal unit CI
skips it.

Everything uses the **SDK** (not raw HTTP) wherever an SDK method exists. The two
spots that have no SDK method yet are flagged inline as gaps: crew code deploy
(only the `smallestai agent-crew` CLI) and making a crew build live
(`PATCH /sdk/agents/{id}/builds/{bid}`).

## Setup

```bash
export SMALLEST_API_KEY=sk_...              # required
export SMALLEST_BASE=https://api.smallest.ai   # optional; use https://api.dev.smallest.ai for dev
export SMALLEST_TEST_NUMBER=+91XXXXXXXXXX   # a phone YOU can answer (caller-context test only)
```

## Run

```bash
# Fast, fully automated — "nothing is broken" baseline (no telephony, no human):
poetry run pytest tests/integration/test_sdk_smoke_live.py -m integration -s

# Caller context end-to-end (PRO-3560) — you must ANSWER the call it places:
poetry run pytest tests/integration/test_caller_context_live.py -m integration -s
# or just run it and watch the payload print:
poetry run python tests/integration/test_caller_context_live.py
```

## What each covers

- **test_sdk_smoke_live.py** — create agent → get round-trip → archive; list phone
  numbers. Catches a broken client / auth / response-shape regression. Add a case
  here whenever a new core surface ships.
- **test_caller_context_live.py** — the full caller-context chain on a real call:
  orchestrator forwards the caller block into `system.init` → SDK exposes it as
  `session.caller` / `session.initial_variables` → crew reads it. The crew emits
  what it read as a structured `caller.probe` event; the test reads that event's
  **payload** (raw `session.caller` data, not the spoken/transcribed line) off the
  conversation and asserts `user_number` / `agent_number` / `direction` / `call_id`.

## Convention for a new SDK change

1. Smoke stays green (nothing broke).
2. Add a focused live test for the new feature next to it (mirror the pattern:
   gate on env, use the SDK, assert the observable behavior, clean up after).
