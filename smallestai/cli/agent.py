import asyncio

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.chat import ChatClient, chat_loop
from smallestai.cli.lib.project_config import ProjectConfig

console = Console()


def initialise_agent_app(
    project_config: ProjectConfig, auth_client: AuthClient, atoms_client: AtomsAPIClient
):
    app = typer.Typer(name="agent")

    @app.command()
    def init():
        """Initialize the agent configuration in the current directory."""
        asyncio.run(async_init())

    async def async_init():
        """Async implementation of init command."""
        agent_id = project_config.get_agent_id()

        if agent_id:
            console.print(
                f"[green]Agent already initialized with ID: [bold]{agent_id}[/bold][/green]"
            )
            return

        # Check if user is logged in
        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print(
                "[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]"
            )
            raise typer.Exit(1)

        access_token = credentials["access_token"]

        console.print("[dim]Fetching agents...[/dim]")
        try:
            agent_data = await atoms_client.get_agents(access_token)
        except Exception as e:
            console.print(f"[red]Error fetching agents: {e}[/red]")
            return

        if not agent_data.agents:
            console.print(
                "[yellow]No agents found. Create an agent first at https://console.smallest.ai[/yellow]"
            )
            return

        choices = [
            questionary.Choice(
                title=f"{agent.name} - ID: {agent.id}",
                value=agent.id,
            )
            for agent in agent_data.agents
        ]

        # Interactive selector
        selected_agent = await questionary.select(
            message="Select an agent to link",
            choices=choices,
            pointer="> ",
        ).ask_async()

        if not selected_agent:
            console.print("[red]No agent selected[/red]")
            return

        project_config.set_agent_id(selected_agent)
        console.print("[green]Agent initialized successfully![/green]")

    @app.command()
    def chat(
        port: int = typer.Argument(8080, help="WebSocket server port"),
        host: str = typer.Option(
            "localhost", "--host", "-h", help="WebSocket server host"
        ),
    ):
        """
        Start a chat session with an Atoms SDK agent.

        Connect to a WebSocket server running an Atoms SDK agent and chat interactively.
        """
        ws_url = f"ws://{host}:{port}/ws"

        console.print(
            Panel(
                f"[bold]SmallestAI agent Chat Client[/bold]\n\nConnecting to: [cyan]{ws_url}[/cyan]",
                border_style="blue",
            )
        )

        async def run():
            client = ChatClient(ws_url)

            if await client._connect():
                try:
                    await chat_loop(client)
                finally:
                    await client._disconnect()
            else:
                console.print("[red]Failed to connect to agent[/red]")

        asyncio.run(run())

    return app
