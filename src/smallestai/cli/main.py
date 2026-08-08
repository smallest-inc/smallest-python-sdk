"""CLI for managing Atoms agent swarms — build, deploy, and chat with multi-node agent swarms."""

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.agents import initialise_agents_app
from smallestai.cli.auth import initialise_auth_app
from smallestai.cli.calls import initialise_calls_app
from smallestai.cli.campaigns import initialise_campaigns_app
from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.project_config import ProjectConfig
from smallestai.cli.mcp import initialise_mcp_app
from smallestai.cli.phone_numbers import initialise_phone_numbers_app
from smallestai.cli.waves import initialise_waves_app

console = Console()

app = typer.Typer(help="SmallestAI CLI", no_args_is_help=False, rich_markup_mode="rich")

_BANNER = r"""[bold magenta]
  ███████╗███╗   ███╗ █████╗ ██╗     ██╗     ███████╗███████╗████████╗
  ██╔════╝████╗ ████║██╔══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝
  ███████╗██╔████╔██║███████║██║     ██║     █████╗  ███████╗   ██║
  ╚════██║██║╚██╔╝██║██╔══██║██║     ██║     ██╔══╝  ╚════██║   ██║
  ███████║██║ ╚═╝ ██║██║  ██║███████╗███████╗███████╗███████║   ██║
  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝[/bold magenta]"""

_COMMANDS = [
    ("agent-crew", "Init, deploy, and manage crew (custom-LLM) voice agents"),
    ("agents", "Create, inspect, and call voice agents"),
    ("calls", "Inspect call logs, transcripts, and recordings"),
    ("campaigns", "Manage outbound calling campaigns"),
    ("phone-numbers", "Search, rent, and manage phone numbers"),
    ("waves", "Text-to-speech, speech-to-text, and voices"),
    ("mcp", "Set up the Smallest AI MCP server for Cursor / Claude"),
    ("auth", "Log in and manage credentials"),
]


def _print_welcome() -> None:
    console.print(_BANNER)
    console.print("  [dim]Build, deploy, and run voice agents and speech models.[/dim]\n")
    table = Table(show_header=False, box=None, padding=(0, 2, 0, 2))
    table.add_column(style="bold cyan", no_wrap=True)
    table.add_column(style="white")
    for name, desc in _COMMANDS:
        table.add_row(name, desc)
    console.print(table)
    console.print(
        "\n  [dim]Run [bold]smallestai <command> --help[/bold] for details, "
        "or [bold]smallestai --help[/bold] for everything.[/dim]\n"
    )


@app.callback(invoke_without_command=True)
def _root(ctx: typer.Context) -> None:
    """SmallestAI CLI."""
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

waves_app = initialise_waves_app(auth_client)
app.add_typer(waves_app, name="waves")

campaigns_app = initialise_campaigns_app(auth_client)
app.add_typer(campaigns_app, name="campaigns")

phone_numbers_app = initialise_phone_numbers_app(auth_client)
app.add_typer(phone_numbers_app, name="phone-numbers")

app.add_typer(initialise_mcp_app(), name="mcp")


def main():
    import sys

    from smallestai import telemetry

    telemetry.maybe_show_first_run_notice()
    # Coarse command group only (e.g. "agent-crew", "auth"); never args or their values.
    command = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ""
    telemetry.capture("cli_invoked", {"command": command})
    app()


if __name__ == "__main__":
    main()
