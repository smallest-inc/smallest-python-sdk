"""`smallestai agents …` — manage Atoms agents from the CLI, on top of the published SDK.

Dogfoods the Fern-generated `SmallestAI` client (not a parallel REST client), so the CLI
and the SDK stay in lockstep automatically. Auth resolves from SMALLEST_API_KEY, else the
key stored by `smallestai auth login` (~/.smallestai/credentials.json). SMALLEST_BASE_URL
overrides the endpoint (dev rig).
"""

import json as _json

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client as _client
from smallestai.cli.lib.client import resolve_key as _resolve_key

console = Console()

DASHBOARD = "https://app.smallest.ai/dashboard/agents"
RENT_NUMBERS = "https://app.smallest.ai/dashboard/phone-numbers/rent-numbers"

__all__ = ["initialise_agents_app", "_client", "_resolve_key"]

# Fields split by where the platform accepts the write:
#   update_agent: non-versioned metadata (name, description, ...)
#   draft write : versioned config (prompt, firstMessage, voice, model, ...), set
#                 on a branch draft via update_draft + publish.
# See AgentsClient.update_agent docstring: a versioned agent rejects config fields
# on PATCH /agent/{id} with "Config changes must be made through drafts."


def _resolve_write_branch_id(client, agent_id: str) -> str:
    """Return the branch to write config into: the live branch, else the default
    `main` branch, else the first listed branch. Config edits on a versioned agent
    go through a branch draft, never through update_agent."""
    branches = client.atoms.agent_versioning_branches.list(id=agent_id)
    summaries = getattr(getattr(branches, "data", None), "branches", None) or []
    live = next((s for s in summaries if getattr(s, "is_live", False)), None)
    default = next((s for s in summaries if getattr(getattr(s, "branch", None), "is_default", False)), None)
    chosen = live or default or (summaries[0] if summaries else None)
    branch = getattr(chosen, "branch", None) if chosen is not None else None
    bid = getattr(branch, "id", None) if branch is not None else None
    if not bid:
        console.print("[red]No writable branch found for this agent.[/red]")
        raise typer.Exit(1)
    return bid


def _build_config_fields(
    *,
    first_message=None,
    prompt=None,
    language=None,
    voice_id=None,
    model=None,
    redaction=None,
    allow_interruptions=None,
    background_sound=None,
) -> dict:
    """Map CLI flags to the versioned-config kwargs shared by create_agent and the
    draft write. Only provided (non-None) flags are included."""
    fields: dict = {}
    if first_message is not None:
        fields["first_message"] = first_message
    if prompt is not None:
        fields["global_prompt"] = prompt
    if language is not None:
        fields["language"] = {"default": language, "supported": [language]}
    if voice_id is not None:
        fields["synthesizer"] = {"voiceConfig": {"voiceId": voice_id}}
    if model is not None:
        fields["slm_model"] = model
    if redaction is not None:
        fields["redaction_config"] = {"isEnabled": redaction}
    if allow_interruptions is not None:
        fields["allow_interruptions"] = allow_interruptions
    if background_sound is not None:
        fields["background_sound"] = background_sound
    return fields


def initialise_agents_app(auth_client: AuthClient):
    agents_app = typer.Typer(name="agents", help="Create, inspect, and call Atoms agents.")

    @agents_app.command("list")
    def list_agents(as_json: bool = typer.Option(False, "--json", help="Emit raw JSON")):
        """List agents in your org."""
        from smallestai.atoms.helpers import as_page

        pg = as_page(_client(auth_client).atoms.agents.list_agents())
        if as_json:
            console.print_json(
                _json.dumps(
                    [
                        {"id": getattr(a, "id", None) or getattr(a, "_id", None), "name": getattr(a, "name", None)}
                        for a in pg.items
                    ],
                    default=str,
                )
            )
            return
        table = Table("ID", "Name", title=f"Agents ({len(pg.items)})")
        for a in pg.items:
            table.add_row(getattr(a, "id", None) or getattr(a, "_id", "?"), getattr(a, "name", "—"))
        console.print(table)

    @agents_app.command("get")
    def get_agent(agent_id: str, as_json: bool = typer.Option(False, "--json", help="Emit raw JSON")):
        """Show one agent's config."""
        a = _client(auth_client).atoms.agents.get_agent(id=agent_id).data
        if as_json:
            console.print_json(a.json() if hasattr(a, "json") else _json.dumps(a, default=str))
            return
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
        language: str = typer.Option(None, "--language", help="Default/supported language, e.g. 'en'"),
        voice_id: str = typer.Option(None, "--voice-id", help="Synthesizer voiceId"),
        model: str = typer.Option(None, "--model", help="LLM model, e.g. 'gpt-4o'"),
        redaction: bool = typer.Option(None, "--redaction/--no-redaction", help="Toggle PII redaction"),
        allow_interruptions: bool = typer.Option(
            None, "--allow-interruptions/--no-allow-interruptions", help="Toggle barge-in"
        ),
        background_sound: str = typer.Option(
            None, "--background-sound", help="Ambient sound: '', office, cafe, call_center, static"
        ),
    ):
        """Create an agent with the common config fields.

        New agents are created with all config inline. The platform accepts the
        versioned fields (prompt/voice/model/…) on create. Use `agents update` to
        change them later (that path goes through a branch draft).
        """
        kw = {"name": name}
        if description:
            kw["description"] = description
        if allow_inbound:
            kw["allow_inbound_call"] = True
        kw.update(
            _build_config_fields(
                first_message=first_message,
                prompt=prompt,
                language=language,
                voice_id=voice_id,
                model=model,
                redaction=redaction,
                allow_interruptions=allow_interruptions,
                background_sound=background_sound,
            )
        )
        agent_id = _client(auth_client).atoms.agents.create_agent(**kw).data
        console.print(f"[green]Created agent[/green] {agent_id}")
        console.print(f"  dashboard: {DASHBOARD}/{agent_id}")

    @agents_app.command("update")
    def update(
        agent_id: str,
        name: str = typer.Option(None, "--name"),
        first_message: str = typer.Option(None, "--first-message"),
        prompt: str = typer.Option(None, "--prompt", help="Global system prompt"),
        description: str = typer.Option(None, "--description"),
        language: str = typer.Option(None, "--language", help="Default/supported language, e.g. 'en'"),
        voice_id: str = typer.Option(None, "--voice-id", help="Synthesizer voiceId"),
        model: str = typer.Option(None, "--model", help="LLM model, e.g. 'gpt-4o'"),
        redaction: bool = typer.Option(None, "--redaction/--no-redaction", help="Toggle PII redaction"),
        allow_interruptions: bool = typer.Option(
            None, "--allow-interruptions/--no-allow-interruptions", help="Toggle barge-in"
        ),
        background_sound: str = typer.Option(
            None, "--background-sound", help="Ambient sound: '', office, cafe, call_center, static"
        ),
    ):
        """Update an agent's config. Only the flags you pass are changed.

        Metadata (--name, --description) goes through update_agent. Versioned config
        (prompt, first message, language, voice, model, redaction, interruptions,
        background sound) is written to the live branch's draft and published. The
        platform rejects those fields on the plain agent update for versioned agents.
        """
        client = _client(auth_client)
        changed: list[str] = []

        meta: dict = {}
        if name is not None:
            meta["name"] = name
        if description is not None:
            meta["description"] = description
        if meta:
            client.atoms.agents.update_agent(agent_id, **meta)
            changed.extend(sorted(meta))

        config = _build_config_fields(
            first_message=first_message,
            prompt=prompt,
            language=language,
            voice_id=voice_id,
            model=model,
            redaction=redaction,
            allow_interruptions=allow_interruptions,
            background_sound=background_sound,
        )
        if config:
            from smallestai.atoms.helpers import Versioning

            branch_id = _resolve_write_branch_id(client, agent_id)
            Versioning(client).edit_and_publish(agent_id, branch_id, **config)
            changed.extend(sorted(config))

        if not changed:
            console.print("[yellow]Nothing to update. Pass at least one field flag.[/yellow]")
            raise typer.Exit(1)
        console.print(f"[green]Updated agent[/green] {agent_id}")
        console.print(f"  changed: {', '.join(changed)}")
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
