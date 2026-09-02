# Call logs & recordings

After a call, read what happened through `client.atoms.calls` (or the
`smallestai calls` CLI).

## One call

```python
call = client.atoms.calls.get(id="CALL-...").data
print(call.status, call.duration, call.recording_url)
for turn in call.transcript or []:
    print(turn.role, ":", turn.content)
```

Fields on `.data`: `status`, `type`, `duration`, `from_`, `to`, `transcript`,
`events`, `recording_url`, `recording_dual_url`, `call_cost`,
`disconnection_reason`, `call_failure_reason`.

## Recent calls

```python
logs = client.atoms.calls.list(agent_ids=agent_id, limit=20).data.logs
for item in logs:
    print(item.call_id, item.type, item.status, item.duration)
```

## CLI

```bash
smallestai calls list --agent-id <id> --limit 20
smallestai calls get CALL-...
smallestai calls transcript CALL-...
smallestai calls recording CALL-...
```

## Live events (while a call is in progress)

Stream a call's events as they happen — transcript turns, per-turn latency, node
transitions, tool calls, and errors:

```bash
smallestai calls events CALL-...               # full live event stream
smallestai calls transcript CALL-... --follow  # just the conversation, live
```

The call must be in progress; for a finished call use `calls transcript` (no
`--follow`) or `calls get`. Add `--json` to emit one raw event per line.

## Reading a transfer from the logs

A transfer produces a second **transfer leg**. If that leg shows
`status: no_answer` / `timeout` with `duration: 0`, the transfer **fired** but the
destination did not pick up — dial a number a human or agent will answer. Crew
calls are recorded too (`recording_url` on the call).
