"""`smallestai calls …` — inspect call logs, details, transcripts, and recordings.

Read-only, on top of the published SDK (`client.agents.calls`). To place a call use
`smallestai agents call`.
"""

import json as _json

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client

console = Console()


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
        call_type: str = typer.Option(
            None, "--type", help="telephony_inbound | telephony_outbound | webcall"
        ),
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
        data = _data(make_client(auth_client).agents.calls.list(**kw))
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
        d = _data(make_client(auth_client).agents.calls.get(id=call_id))
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

    @calls_app.command("transcript")
    def transcript(
        call_id: str,
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Print a call's transcript, one turn per line."""
        d = _data(make_client(auth_client).agents.calls.get(id=call_id))
        turns = getattr(d, "transcript", None) or []
        if as_json:
            console.print_json(
                _json.dumps(
                    [{"role": getattr(t, "role", None), "content": getattr(t, "content", None),
                      "timestamp": getattr(t, "timestamp", None)} for t in turns],
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
        d = _data(make_client(auth_client).agents.calls.get(id=call_id))
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
