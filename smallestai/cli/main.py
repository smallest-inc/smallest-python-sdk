"""CLI chat application for communicating with Atoms SDK agents via WebSocket."""

import typer
from rich.console import Console

from smallestai.cli.agent import initialise_agent_app
from smallestai.cli.auth import initialise_auth_app
from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.project_config import ProjectConfig

console = Console()

app = typer.Typer(help="SmallestAI CLI")

auth_client = AuthClient()
atoms_client = AtomsAPIClient()
project_config = ProjectConfig()

agent_app = initialise_agent_app(project_config, auth_client, atoms_client)
app.add_typer(agent_app)

auth_app = initialise_auth_app(auth_client, atoms_client)
app.add_typer(auth_app)


def main():
    app()


if __name__ == "__main__":
    main()
