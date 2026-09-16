"""`smallestai calls …` — inspect call logs, details, transcripts, and recordings.

Read-only, on top of the published SDK (`client.atoms.calls`). To place a call use
`smallestai agents call`.
"""

import asyncio
import json as _json

import httpx
import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client

console = Console()


def _session_token(auth_client: AuthClient) -> str:
    """Session access token for live endpoints (events SSE) that need it."""
    creds = auth_client.get_credentials()
    token = (creds or {}).get("access_token")
    if not token:
        console.print("[red]You must be logged in. Run 'smallestai auth login'.[/red]")
        raise typer.Exit(1)
    return token


def _render_event(ev: dict) -> None:
    """Pretty-print one live call event."""
    et = ev.get("event_type")
    if et == "call_start":
        console.print("[dim]● call started[/dim]")
    elif et == "user_transcription":
        console.print(f"[cyan]user[/cyan]: {ev.get('user_transcription_text', '')}")
    elif et == "tts_completed":
        console.print(f"[green]agent[/green]: {ev.get('tts_text', '')}")
    elif et == "turn_latency":
        console.print(f"[dim]  latency: {ev.get('turn_latency')}[/dim]")
    elif et == "agent_node_state":
        console.print(f"[dim]  node: {ev.get('node_name')} ({ev.get('node_type')})[/dim]")
    elif et == "hopping":
        console.print(f"[dim]  hop: {ev.get('from_node_id')} -> {ev.get('to_node_id')}[/dim]")
    elif et in ("tool_call_start", "tool_call_end", "tool_call_error"):
        console.print(
            f"[magenta]  {et}[/magenta]: {_json.dumps({k: v for k, v in ev.items() if k != 'event_type'}, default=str)}"
        )
    elif et in ("agent_error", "generic_call_error"):
        console.print(f"[red]  error: {ev.get('error') or ev.get('message') or ev}[/red]")
    else:
        rest = {k: v for k, v in ev.items() if k != "event_type"}
        console.print(f"[dim]  {et}{': ' + _json.dumps(rest, default=str) if rest else ''}[/dim]")


def _render_transcript_event(ev: dict) -> None:
    """Print only the conversation turns from a live event stream."""
    et = ev.get("event_type")
    if et == "user_transcription" and ev.get("user_transcription_text"):
        console.print(f"[cyan]user[/cyan]: {ev['user_transcription_text']}")
    elif et == "tts_completed" and ev.get("tts_text"):
        console.print(f"[green]agent[/green]: {ev['tts_text']}")


async def _stream_call_events(call_id: str, token: str, as_json: bool, transcript_only: bool) -> None:
    client = AtomsAPIClient()
    try:
        async for ev in client.stream_call_events(call_id, token):
            et = ev.get("event_type")
            if et == "sse_init":
                if not as_json and not transcript_only:
                    console.print("[dim]connected — waiting for events…[/dim]")
                continue
            if as_json:
                console.print_json(_json.dumps(ev, default=str))
            elif transcript_only:
                _render_transcript_event(ev)
            else:
                _render_event(ev)
            if et in ("sse_close", "call_end"):
                if not as_json and not transcript_only:
                    console.print("[dim]— call ended —[/dim]")
                break
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 400:
            console.print(
                f"[yellow]This call is not live (already finished). "
                f"Run 'smallestai calls transcript {call_id}' for the final transcript.[/yellow]"
            )
        elif code == 404:
            console.print("[yellow]Call not found.[/yellow]")
        else:
            console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped.[/yellow]")


def _data(resp):
    """Unwrap `.data` from an SDK response (or return the object itself)."""
    return getattr(resp, "data", resp)


def _fmt_dur(seconds) -> str:
    try:
        s = float(seconds)
    except (TypeError, ValueError):
        return "—"
    return f"{int(s // 60)}m{int(s % 60):02d}s" if s >= 60 else f"{s:.1f}s"


def initialise_calls_app(auth_client: AuthClient):
    calls_app = typer.Typer(name="calls", help="Inspect call logs, transcripts, and recordings.")

    @calls_app.command("list")
    def list_calls(
        agent_id: str = typer.Option(None, "--agent-id", help="Filter by agent id"),
        limit: int = typer.Option(20, "--limit", help="Max rows"),
        call_type: str = typer.Option(None, "--type", help="telephony_inbound | telephony_outbound | webcall"),
        status: str = typer.Option(None, "--status", help="Filter by status"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """List recent calls (most recent first)."""
        kw = {"limit": limit}
        if agent_id:
            kw["agent_ids"] = agent_id
        if call_type:
            kw["call_types"] = call_type
        if status:
            kw["status_filter"] = status
        data = _data(make_client(auth_client).atoms.calls.list(**kw))
        logs = getattr(data, "logs", None) or []
        if as_json:
            console.print_json(_json.dumps([_row_dict(x) for x in logs], default=str))
            return
        table = Table("Call ID", "Type", "Status", "Dur", "From", "To", "When", title=f"Calls ({len(logs)})")
        for x in logs:
            table.add_row(
                getattr(x, "call_id", None) or "—",
                (getattr(x, "type", None) or "—").replace("telephony_", ""),
                getattr(x, "status", None) or "—",
                _fmt_dur(getattr(x, "duration", None)),
                getattr(x, "from_", None) or "—",
                getattr(x, "to", None) or "—",
                str(getattr(x, "created_at", None) or "—")[:19],
            )
        console.print(table)

    @calls_app.command("get")
    def get_call(
        call_id: str,
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Show one call's details (status, duration, cost, recording, turn count)."""
        d = _data(make_client(auth_client).atoms.calls.get(id=call_id))
        if as_json:
            console.print_json(d.json() if hasattr(d, "json") else _json.dumps(d, default=str))
            return
        transcript = getattr(d, "transcript", None) or []
        console.print(f"[bold]{call_id}[/bold]")
        console.print(f"  status        : {getattr(d, 'status', None)}")
        console.print(f"  type          : {getattr(d, 'type', None)}")
        console.print(f"  duration      : {_fmt_dur(getattr(d, 'duration', None))}")
        console.print(f"  from -> to    : {getattr(d, 'from_', None)} -> {getattr(d, 'to', None)}")
        console.print(f"  turns         : {len(transcript)}")
        cost = getattr(d, "call_cost", None)
        if cost is not None:
            console.print(f"  cost          : {cost}")
        fail = getattr(d, "call_failure_reason", None)
        if fail:
            console.print(f"  failure       : [yellow]{fail}[/yellow]")
        rec = getattr(d, "recording_url", None)
        console.print(f"  recording     : {rec or '[dim]none[/dim]'}")
        console.print("  [dim]transcript: smallestai calls transcript " + call_id + "[/dim]")

    @calls_app.command("events")
    def events(
        call_id: str,
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON, one event per line"),
    ):
        """Stream a live call's events as they happen.

        Shows transcript turns, per-turn latency, node transitions, tool calls,
        and errors while the call is in progress. For a finished call use
        `smallestai calls transcript`.
        """
        token = _session_token(auth_client)
        asyncio.run(_stream_call_events(call_id, token, as_json, transcript_only=False))

    @calls_app.command("transcript")
    def transcript(
        call_id: str,
        follow: bool = typer.Option(
            False, "--follow", "-f", help="Stream the transcript live (call must be in progress)"
        ),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Print a call's transcript, one turn per line.

        With --follow, streams turns live while the call is in progress.
        """
        if follow:
            token = _session_token(auth_client)
            asyncio.run(_stream_call_events(call_id, token, as_json, transcript_only=True))
            return
        d = _data(make_client(auth_client).atoms.calls.get(id=call_id))
        turns = getattr(d, "transcript", None) or []
        if as_json:
            console.print_json(
                _json.dumps(
                    [
                        {
                            "role": getattr(t, "role", None),
                            "content": getattr(t, "content", None),
                            "timestamp": getattr(t, "timestamp", None),
                        }
                        for t in turns
                    ],
                    default=str,
                )
            )
            return
        if not turns:
            console.print("[yellow]No transcript for this call.[/yellow]")
            return
        for t in turns:
            role = getattr(t, "role", "?")
            colour = "cyan" if role == "user" else "green"
            console.print(f"[{colour}]{role}[/{colour}]: {getattr(t, 'content', '')}")

    @calls_app.command("recording")
    def recording(call_id: str):
        """Print a call's recording URL(s)."""
        d = _data(make_client(auth_client).atoms.calls.get(id=call_id))
        url = getattr(d, "recording_url", None)
        dual = getattr(d, "recording_dual_url", None)
        if not url and not dual:
            console.print("[yellow]No recording available for this call.[/yellow]")
            raise typer.Exit(0)
        if url:
            console.print(url)
        if dual and dual != url:
            console.print(f"[dim]dual-channel:[/dim] {dual}")

    return calls_app


def _row_dict(x):
    return {
        "call_id": getattr(x, "call_id", None),
        "type": getattr(x, "type", None),
        "status": getattr(x, "status", None),
        "duration": getattr(x, "duration", None),
        "from": getattr(x, "from_", None),
        "to": getattr(x, "to", None),
        "recording_url": getattr(x, "recording_url", None),
        "created_at": getattr(x, "created_at", None),
    }
