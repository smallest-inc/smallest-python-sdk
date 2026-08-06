"""`smallestai campaigns …` — list, inspect, and control outbound campaigns.

Thin CLI over `client.agents.campaigns`, matching the style of `smallestai calls`.
"""

import json as _json
import typing
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client

console = Console()


def _data(resp):
    return getattr(resp, "data", resp)


def initialise_campaigns_app(auth_client: AuthClient):
    campaigns_app = typer.Typer(name="campaigns", help="List, inspect, and control campaigns.")

    @campaigns_app.command("list")
    def list_campaigns(
        status: str = typer.Option(
            None, "--status", help="draft|scheduled|processing|running|paused|completed|failed"
        ),
        search: str = typer.Option(None, "--search", help="Search by name"),
        page: int = typer.Option(None, "--page", help="Page number"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """List campaigns."""
        kw: typing.Dict[str, typing.Any] = {}
        if status:
            kw["status"] = status
        if search:
            kw["search"] = search
        if page is not None:
            kw["page"] = page
        resp = make_client(auth_client).agents.campaigns.list(**kw)
        data = _data(resp)
        items = getattr(data, "campaigns", None) or (data if isinstance(data, list) else [])
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(items, default=str))
            return
        table = Table("ID", "Name", "Status", "Agent", "Audience", title=f"Campaigns ({len(items)})")
        for x in items:
            table.add_row(
                str(getattr(x, "id", None) or getattr(x, "_id", None) or "—"),
                str(getattr(x, "name", None) or "—"),
                str(getattr(x, "status", None) or "—"),
                str(getattr(x, "agent_id", None) or "—"),
                str(getattr(x, "audience_id", None) or "—"),
            )
        console.print(table)

    @campaigns_app.command("get")
    def get_campaign(
        campaign_id: str,
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Show one campaign's details."""
        resp = make_client(auth_client).agents.campaigns.get(id=campaign_id)
        d = _data(resp)
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(d, default=str))
            return
        console.print(f"[bold]{campaign_id}[/bold]")
        for field in ("name", "status", "agent_id", "audience_id", "scheduled_at", "created_at"):
            console.print(f"  {field:<13}: {getattr(d, field, None)}")

    @campaigns_app.command("create")
    def create_campaign(
        name: str = typer.Option(..., "--name"),
        audience_id: str = typer.Option(..., "--audience-id"),
        agent_id: str = typer.Option(..., "--agent-id"),
        description: str = typer.Option(None, "--description"),
        phone_number_ids: str = typer.Option(None, "--phone-number-ids", help="Comma-separated ids"),
        scheduled_at: str = typer.Option(None, "--scheduled-at", help="ISO 8601 timestamp"),
        max_retries: int = typer.Option(None, "--max-retries"),
        retry_delay: int = typer.Option(None, "--retry-delay"),
    ):
        """Create a campaign."""
        kw: typing.Dict[str, typing.Any] = {"name": name, "audience_id": audience_id, "agent_id": agent_id}
        if description:
            kw["description"] = description
        if phone_number_ids:
            kw["phone_number_ids"] = [s.strip() for s in phone_number_ids.split(",") if s.strip()]
        if scheduled_at:
            try:
                kw["scheduled_at"] = datetime.fromisoformat(scheduled_at)
            except ValueError:
                typer.echo(
                    f"Invalid --scheduled-at {scheduled_at!r}: expected ISO 8601, "
                    "e.g. 2026-08-10T15:30:00",
                    err=True,
                )
                raise typer.Exit(2)
        if max_retries is not None:
            kw["max_retries"] = max_retries
        if retry_delay is not None:
            kw["retry_delay"] = retry_delay
        d = _data(make_client(auth_client).agents.campaigns.create(**kw))
        console.print(f"[green]Created campaign[/green] {getattr(d, 'id', None) or getattr(d, '_id', d)}")

    @campaigns_app.command("pause")
    def pause_campaign(campaign_id: str):
        """Pause a running campaign."""
        make_client(auth_client).agents.campaigns.pause(id=campaign_id)
        console.print(f"[yellow]Paused[/yellow] {campaign_id}")

    @campaigns_app.command("resume")
    def resume_campaign(campaign_id: str):
        """Start or resume a campaign."""
        make_client(auth_client).agents.campaigns.start_or_resume(id=campaign_id)
        console.print(f"[green]Started/resumed[/green] {campaign_id}")

    @campaigns_app.command("delete")
    def delete_campaign(
        campaign_id: str,
        yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    ):
        """Delete a campaign."""
        if not yes:
            typer.confirm(f"Delete campaign {campaign_id}?", abort=True)
        make_client(auth_client).agents.campaigns.delete(id=campaign_id)
        console.print(f"[red]Deleted[/red] {campaign_id}")

    return campaigns_app
