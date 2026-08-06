"""CLI for managing Atoms agent swarms — build, deploy, and chat with multi-node agent swarms."""

import typer
from rich.console import Console

from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.agents import initialise_agents_app
from smallestai.cli.auth import initialise_auth_app
from smallestai.cli.calls import initialise_calls_app
from smallestai.cli.campaigns import initialise_campaigns_app
from smallestai.cli.phone_numbers import initialise_phone_numbers_app
from smallestai.cli.waves import initialise_waves_app
from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.project_config import ProjectConfig

console = Console()

app = typer.Typer(help="SmallestAI CLI")

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
