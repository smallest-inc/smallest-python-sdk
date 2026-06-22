"""`smallestai agents …` — manage Atoms agents from the CLI, on top of the published SDK.

Dogfoods the Fern-generated `SmallestAI` client (not a parallel REST client), so the CLI
and the SDK stay in lockstep automatically. Auth resolves from SMALLEST_API_KEY, else the
key stored by `smallestai auth login` (~/.smallestai/credentials.json). SMALLEST_BASE_URL
overrides the endpoint (dev rig).
"""
import os

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient

console = Console()

DASHBOARD = "https://app.smallest.ai/dashboard/agents"
RENT_NUMBERS = "https://app.smallest.ai/dashboard/phone-numbers/rent-numbers"


def _resolve_key(auth_client: AuthClient) -> str:
    key = os.environ.get("SMALLEST_API_KEY")
    if not key:
        creds = auth_client.get_credentials()
        key = (creds or {}).get("access_token")
    if not key:
        console.print("[red]No API key. Set SMALLEST_API_KEY or run `smallestai auth login`.[/red]")
        raise typer.Exit(1)
    return key


def _client(auth_client: AuthClient):
    from smallestai import SmallestAI

    key = _resolve_key(auth_client)
    base = os.environ.get("SMALLEST_BASE_URL")
    if base:
        from smallestai.environment import SmallestAIEnvironment

        base = base.rstrip("/")
        ws = base.replace("https://", "wss://").replace("http://", "ws://")
        env = SmallestAIEnvironment(atoms=f"{base}/atoms/v1", waves=base, waves_ws=ws)
        return SmallestAI(api_key=key, environment=env)
    return SmallestAI(api_key=key)


def initialise_agents_app(auth_client: AuthClient):
    agents_app = typer.Typer(name="agents", help="Create, inspect, and call Atoms agents.")

    @agents_app.command("list")
    def list_agents():
        """List agents in your org."""
        from smallestai.atoms.helpers import as_page

        pg = as_page(_client(auth_client).atoms.agents.list_agents())
        table = Table("ID", "Name", title=f"Agents ({len(pg.items)})")
        for a in pg.items:
            table.add_row(getattr(a, "id", None) or getattr(a, "_id", "?"), getattr(a, "name", "—"))
        console.print(table)

    @agents_app.command("get")
    def get_agent(agent_id: str):
        """Show one agent's config."""
        a = _client(auth_client).atoms.agents.get_agent(id=agent_id).data
        console.print(f"[bold]{getattr(a, 'name', '—')}[/bold]  [dim]{agent_id}[/dim]")
        console.print(f"  first message : {getattr(a, 'first_message', None)!r}")
        console.print(f"  language      : {getattr(a, 'language', None)}")
        console.print(f"  dashboard     : {DASHBOARD}/{agent_id}")

    @agents_app.command("dashboard")
    def dashboard(agent_id: str):
        """Print the dashboard URL for an agent."""
        console.print(f"{DASHBOARD}/{agent_id}")

    @agents_app.command("phone-status")
    def phone_status(agent_id: str):
        """Show whether a phone number is configured for the agent."""
        a = _client(auth_client).atoms.agents.get_agent(id=agent_id).data
        number = getattr(a, "phone_number", None)
        if number:
            console.print(f"[green]Phone configured:[/green] {number}")
        else:
            console.print("[yellow]No phone number configured for this agent.[/yellow]")
            console.print(f"  Rent or assign one at: {RENT_NUMBERS}")

    @agents_app.command("create")
    def create(
        name: str,
        first_message: str = typer.Option(None, "--first-message"),
        prompt: str = typer.Option(None, "--prompt", help="Global system prompt"),
        description: str = typer.Option(None, "--description"),
        allow_inbound: bool = typer.Option(False, "--allow-inbound"),
    ):
        """Create an agent. (Voice/language/model config flags land in a follow-up.)"""
        kw = {"name": name}
        if first_message:
            kw["first_message"] = first_message
        if prompt:
            kw["global_prompt"] = prompt
        if description:
            kw["description"] = description
        if allow_inbound:
            kw["allow_inbound_call"] = True
        agent_id = _client(auth_client).atoms.agents.create_agent(**kw).data
        console.print(f"[green]Created agent[/green] {agent_id}")
        console.print(f"  dashboard: {DASHBOARD}/{agent_id}")

    @agents_app.command("call")
    def call(
        agent_id: str,
        to: str = typer.Option(..., "--to", help="Destination phone number (E.164)"),
        from_product_id: str = typer.Option(None, "--from-product-id", help="Acquired number's product id"),
    ):
        """Place an outbound call from an agent to a phone number."""
        kw = {"agent_id": agent_id, "phone_number": to}
        if from_product_id:
            kw["from_product_id"] = from_product_id
        r = _client(auth_client).atoms.calls.start_outbound_call(**kw)
        console.print(f"[green]Call started:[/green] {getattr(r, 'data', r)}")

    return agents_app
