"""CLI for managing Atoms agent swarms — build, deploy, and chat with multi-node agent swarms."""

import typer
from rich.console import Console

from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.auth import initialise_auth_app
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


def main():
    app()


if __name__ == "__main__":
    main()
