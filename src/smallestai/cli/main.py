"""CLI for building, deploying, and running Smallest AI voice agents and speech models."""

import sys

import typer
from rich.console import Console
from rich.table import Table

from smallestai import __version__
from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.agents import initialise_agents_app
from smallestai.cli.auth import initialise_auth_app
from smallestai.cli.banner import print_banner
from smallestai.cli.calls import initialise_calls_app
from smallestai.cli.campaigns import initialise_campaigns_app
from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client
from smallestai.cli.lib.project_config import ProjectConfig
from smallestai.cli.mcp import initialise_mcp_app
from smallestai.cli.phone_numbers import initialise_phone_numbers_app
from smallestai.cli.waves import initialise_waves_app

console = Console()

DASHBOARD_URL = "https://app.smallest.ai/dashboard"
DOCS_URL = "https://docs.smallest.ai"

app = typer.Typer(
    help="Build, deploy, and run Smallest AI voice agents and speech models.",
    no_args_is_help=False,
    rich_markup_mode="rich",
)

# Grouped command list shown on the bare `smallestai` welcome screen.
_GROUPS = [
    (
        "BUILD & DEPLOY",
        [
            ("agent-crew init", "Link a crew (custom-LLM) agent to this project"),
            ("agent-crew deploy", "Package and deploy your crew code"),
            ("agent-crew builds", "List builds; make live, take down, or manage"),
            ("agent-crew logs", "Stream a build's compile + deploy logs"),
            ("agent-crew doctor", "Check a crew agent's config for gotchas"),
        ],
    ),
    (
        "VOICE AGENTS",
        [
            ("agents", "Create, inspect, and call voice agents"),
        ],
    ),
    (
        "TELEPHONY",
        [
            ("calls", "Inspect call logs, transcripts, and recordings"),
            ("campaigns", "Manage outbound calling campaigns"),
            ("phone-numbers", "Search, rent, and manage phone numbers"),
        ],
    ),
    (
        "SPEECH",
        [
            ("models", "Text-to-speech, speech-to-text, and voices"),
        ],
    ),
    (
        "SETUP",
        [
            ("auth", "Log in and manage credentials"),
            ("mcp", "Set up the Smallest AI MCP server for Cursor / Claude"),
            ("status", "Show login, account, and linked agent"),
            ("doctor", "Diagnose your environment and connectivity"),
        ],
    ),
]


def _print_welcome() -> None:
    print_banner()
    console.print("\n  [dim]Build, deploy, and run voice agents and speech models.[/dim]\n")
    for header, rows in _GROUPS:
        console.print(f"  [bold #3B82F6]{header}[/bold #3B82F6]")
        table = Table(show_header=False, box=None, padding=(0, 2, 0, 4))
        table.add_column(style="bold cyan", no_wrap=True)
        table.add_column(style="white")
        for name, desc in rows:
            table.add_row(name, desc)
        console.print(table)
        console.print()
    console.print(
        "  [dim]Run [bold]smallestai <command> --help[/bold] for details.[/dim]\n"
        "  [dim][bold]smallestai version[/bold]  |  [bold]smallestai docs[/bold]  |  "
        "[bold]smallestai --help[/bold][/dim]\n"
    )


def _version_string() -> str:
    return f"smallestai {__version__}"


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    version_flag: bool = typer.Option(False, "--version", "-V", help="Show the version and exit", is_eager=True),
) -> None:
    """Build, deploy, and run Smallest AI voice agents and speech models.

    Auth reads SMALLEST_API_KEY (or `smallestai auth login`); SMALLEST_BASE_URL
    overrides the API host.
    """
    if version_flag:
        console.print(_version_string())
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        _print_welcome()
        raise typer.Exit()


auth_client = AuthClient()
atoms_client = AtomsAPIClient()
project_config = ProjectConfig()

agent_crew_app = initialise_agent_crew_app(project_config, auth_client, atoms_client)
app.add_typer(agent_crew_app, name="agent-crew")

auth_app = initialise_auth_app(auth_client, atoms_client)
app.add_typer(auth_app, name="auth")

agents_app = initialise_agents_app(auth_client)
app.add_typer(agents_app, name="agents")

calls_app = initialise_calls_app(auth_client)
app.add_typer(calls_app, name="calls")

models_app = initialise_waves_app(auth_client)
app.add_typer(models_app, name="models")
# Back-compat: keep the old `waves` name working, hidden from help.
app.add_typer(models_app, name="waves", hidden=True)

campaigns_app = initialise_campaigns_app(auth_client)
app.add_typer(campaigns_app, name="campaigns")

phone_numbers_app = initialise_phone_numbers_app(auth_client)
app.add_typer(phone_numbers_app, name="phone-numbers")

app.add_typer(initialise_mcp_app(), name="mcp")


# ------------------------------------------------------------------ convenience commands


@app.command()
def version() -> None:
    """Show the installed smallestai version."""
    console.print(_version_string())


def _account():
    """(email, name, org) for the logged-in user, or None if not logged in."""
    creds = auth_client.get_credentials()
    if not creds or not creds.get("access_token"):
        return None
    try:
        d = make_client(auth_client).atoms.user.get_user_details()
        u = getattr(d, "data", d)
        name = " ".join(x for x in [getattr(u, "first_name", None), getattr(u, "last_name", None)] if x)
        return {
            "email": getattr(u, "user_email", None),
            "name": name or None,
            "organization_id": getattr(u, "organization_id", None),
        }
    except Exception:
        return {"email": None, "name": None, "organization_id": None}


@app.command()
def whoami(as_json: bool = typer.Option(False, "--json", help="Emit raw JSON")) -> None:
    """Show the currently authenticated account."""
    acct = _account()
    if acct is None:
        console.print("[yellow]Not logged in. Run [bold]smallestai auth login[/bold].[/yellow]")
        raise typer.Exit(1)
    if as_json:
        import json as _json

        console.print_json(_json.dumps(acct, default=str))
        return
    console.print(f"  {acct.get('name') or '—'}  <{acct.get('email') or '—'}>")
    console.print(f"  org: {acct.get('organization_id') or '—'}")


@app.command()
def status(as_json: bool = typer.Option(False, "--json", help="Emit raw JSON")) -> None:
    """Show login, account, linked agent, and version — handy for bug reports."""
    import os

    creds = auth_client.get_credentials()
    logged_in = bool(creds and creds.get("access_token"))
    if os.environ.get("SMALLEST_API_KEY"):
        key_source = "env (SMALLEST_API_KEY)"
    elif logged_in:
        key_source = "stored"
    else:
        key_source = "none"
    acct = _account() if logged_in else None
    linked_agent = project_config.get_agent_id()
    info = {
        "version": __version__,
        "logged_in": logged_in,
        "key_source": key_source,
        "email": (acct or {}).get("email"),
        "organization_id": (acct or {}).get("organization_id"),
        "linked_agent_id": linked_agent,
    }
    if as_json:
        import json as _json

        console.print_json(_json.dumps(info, default=str))
        return
    console.print(f"  smallestai   : {__version__}")
    console.print(f"  logged in    : {'yes' if logged_in else 'no'} ({key_source})")
    console.print(f"  account      : {(acct or {}).get('email') or '—'}")
    console.print(f"  organization : {(acct or {}).get('organization_id') or '—'}")
    console.print(f"  linked agent : {linked_agent or '[dim]none (not in a crew project)[/dim]'}")


@app.command("open")
def open_dashboard(
    agent_id: str = typer.Argument(None, help="Open a specific agent (defaults to the dashboard root)"),
) -> None:
    """Open the Smallest AI dashboard in your browser."""
    url = f"{DASHBOARD_URL}/agents/{agent_id}" if agent_id else DASHBOARD_URL
    if sys.stdout.isatty():
        typer.launch(url)
    else:
        console.print(url)


@app.command()
def docs(topic: str = typer.Argument(None, help="Open a docs topic path (optional)")) -> None:
    """Open the Smallest AI docs in your browser."""
    url = f"{DOCS_URL}/{topic.lstrip('/')}" if topic else DOCS_URL
    if sys.stdout.isatty():
        typer.launch(url)
    else:
        console.print(url)


@app.command()
def doctor() -> None:
    """Diagnose your environment and connectivity (like `fly doctor`)."""
    import os
    import shutil

    ok, warn = [], []

    if os.environ.get("SMALLEST_API_KEY"):
        ok.append("SMALLEST_API_KEY is set")
    else:
        creds = auth_client.get_credentials()
        if creds and creds.get("access_token"):
            ok.append("stored credentials present")
        else:
            warn.append("not logged in — set SMALLEST_API_KEY or run `smallestai auth login`")

    acct = _account()
    if acct and acct.get("email"):
        ok.append(f"reached api.smallest.ai as {acct['email']}")
    elif acct is not None:
        warn.append("logged in but could not fetch account (API unreachable or key invalid)")

    # best-effort: compare installed vs latest on PyPI (skip silently on no network)
    try:
        import httpx

        latest = httpx.get("https://pypi.org/pypi/smallestai/json", timeout=5).json()["info"]["version"]
        if latest == __version__:
            ok.append(f"smallestai {__version__} (latest)")
        else:
            warn.append(f"smallestai {__version__} installed; {latest} available (pip install -U smallestai)")
    except Exception:
        ok.append(f"smallestai {__version__}")

    if shutil.which("npx"):
        ok.append("npx present (needed for `smallestai mcp run`)")
    else:
        warn.append("npx not found — needed for `smallestai mcp run` (install Node.js)")

    for line in ok:
        console.print(f"  [green]✓[/green] {line}")
    for line in warn:
        console.print(f"  [yellow]![/yellow] {line}")
    if warn:
        raise typer.Exit(1)


def main():
    from smallestai import telemetry

    telemetry.maybe_show_first_run_notice()
    # Coarse command group only (e.g. "agent-crew", "auth"); never args or their values.
    command = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ""
    telemetry.capture("cli_invoked", {"command": command})
    app()


if __name__ == "__main__":
    main()
