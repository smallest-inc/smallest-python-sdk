import asyncio
import base64
from io import BytesIO
from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel

from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.chat import ChatClient, chat_loop
from smallestai.cli.lib.project_config import ProjectConfig
from smallestai.cli.utils import create_zip_from_directory

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
    def deploy(
        entry_point: str = typer.Option(
            "server.py",
            "--entry-point",
            "-e",
            help="Entry point file name (e.g., server.py)",
        ),
    ):
        """
        Deploy an agent to the Atoms platform.

        Packages the agent code directory into a zip file and deploys it to the backend.
        """
        asyncio.run(async_deploy(".", entry_point))

    async def async_deploy(directory: str, entry_point: str):
        """Deploy an agent asynchronously."""
        agent_id = project_config.get_agent_id()

        if not agent_id:
            console.print(
                "[red]Agent not initialized. Run 'smallestai agent init' first.[/red]"
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

        dir_path = Path(directory)
        if not dir_path.exists():
            console.print(f"[red]Error: Directory '{directory}' does not exist.[/red]")
            return

        if not dir_path.is_dir():
            console.print(f"[red]Error: '{directory}' is not a directory.[/red]")
            return

        # Check if entry point file exists
        entry_point_path = dir_path / entry_point
        if not entry_point_path.exists():
            console.print(
                f"[red]Error: Entry point file '{entry_point}' not found in '{directory}'.[/red]"
            )
            return

        console.print(
            f"[bold cyan]Deploying agent from: {dir_path.absolute()}[/bold cyan]"
        )
        console.print(f"[dim]Entry point: {entry_point}[/dim]")
        console.print(f"[dim]Agent ID: {agent_id}[/dim]\n")

        # Create zip file in memory
        console.print("[yellow]Packaging agent code...[/yellow]")
        zip_buffer: BytesIO = create_zip_from_directory(dir_path)

        zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
        zip_size_mb = len(zip_buffer.getvalue()) / (1024 * 1024)
        console.print(f"[green]✓[/green] Package created ({zip_size_mb:.2f} MB)")

        # Deploy to backend
        console.print("[yellow]Uploading to Atoms platform...[/yellow]")
        try:
            result = await atoms_client.create_agent_build(
                agent_id=agent_id,
                entry_point_file_name=entry_point,
                agent_code_zip=zip_base64,
                api_key=access_token,
            )

            console.print("[bold green]✓ Deployment successful![/bold green]")
            console.print(f"[dim]Build ID: {result.build_id}[/dim]")
            console.print(f"[dim]Status: {result.message}[/dim]")

        except Exception as e:
            console.print(f"[red]Error deploying agent {e}[/red]")

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
