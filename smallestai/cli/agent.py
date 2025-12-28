import asyncio
import base64
from io import BytesIO
from pathlib import Path

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from smallestai.cli.lib.atoms import AgentBuildStatus, AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.chat import ChatClient, chat_loop
from smallestai.cli.lib.project_config import ProjectConfig
from smallestai.cli.utils import create_zip_from_directory

AGENT_BUILD_STATUS_COLORS = {
    AgentBuildStatus.SUCCEEDED: "green",
    AgentBuildStatus.BUILD_FAILED: "red",
    AgentBuildStatus.DEPLOY_FAILED: "red",
    AgentBuildStatus.QUEUED: "yellow",
    AgentBuildStatus.BUILDING: "yellow",
    AgentBuildStatus.DEPLOYING: "yellow",
}

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
    def chat():
        """
        Start a chat session with an Atoms SDK agent.

        Connect to a WebSocket server running an Atoms SDK agent and chat interactively.
        """
        host = "localhost"
        port = 8080
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

    @app.command("builds")
    def list_builds(
        build_id: str = typer.Argument(
            None, help="Optional build ID to manage directly"
        ),
        limit: int = typer.Option(
            50, "--limit", "-l", help="Number of builds to fetch"
        ),
        offset: int = typer.Option(0, "--offset", "-o", help="Offset for pagination"),
    ):
        """
        List all builds for the current agent and manage them interactively.

        If a build_id is provided, directly manage that specific build.
        """
        asyncio.run(async_list_builds(build_id, limit, offset))

    async def async_list_builds(build_id: str | None, limit: int, offset: int):
        """Async implementation of list builds command."""
        agent_id = project_config.get_agent_id()

        if not agent_id:
            console.print(
                "[red]Agent not initialized. Run 'smallestai agent init' first.[/red]"
            )
            return

        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print(
                "[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]"
            )
            raise typer.Exit(1)

        access_token = credentials["access_token"]

        try:
            if build_id:
                console.print(f"[dim]Fetching build: {build_id}[/dim]")
                build = await atoms_client.get_agent_build(
                    agent_id=agent_id,
                    build_id=build_id,
                    api_key=access_token,
                )
                await _manage_build(agent_id, build, access_token)
                return

            console.print(f"[dim]Fetching builds for agent: {agent_id}[/dim]")

            result = await atoms_client.list_agent_builds(
                agent_id=agent_id,
                api_key=access_token,
                limit=limit,
                offset=offset,
            )

            if not result.builds:
                console.print("[yellow]No builds found for this agent.[/yellow]")
                return

            table = Table(title="Agent Builds")
            table.add_column("Build ID", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Live", style="green")
            table.add_column("Created At", style="dim")

            for build in result.builds:
                status_color = AGENT_BUILD_STATUS_COLORS[build.status]
                status_text = (
                    f"[{status_color}]{build.status.value.upper()}[/{status_color}]"
                )

                live_indicator = "[green]✓ LIVE[/green]" if build.is_live else "-"

                table.add_row(
                    build.id,
                    status_text,
                    live_indicator,
                    build.created_at,
                )

            console.print(table)
            console.print(
                f"[dim]Showing {len(result.builds)} of {result.pagination.total} builds[/dim]\n"
            )

            choices = [
                questionary.Choice(
                    title=f"{build.id[:12]}... | {build.status.value} | {'LIVE' if build.is_live else '-'} | {build.created_at}",
                    value=build,
                )
                for build in result.builds
            ]
            choices.append(questionary.Choice(title="Cancel", value="cancel"))

            selected_build = await questionary.select(
                message="Select a build to manage (or Cancel to exit)",
                choices=choices,
                pointer="> ",
            ).ask_async()

            if not selected_build:
                console.print("[dim]No build selected.[/dim]")
                return

            if selected_build == "cancel":
                console.print("[dim]Exiting...[/dim]")
                return

            await _manage_build(agent_id, selected_build, access_token)

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    async def _manage_build(agent_id: str, build, access_token: str):
        """Show action menu and manage a specific build."""
        status_color = AGENT_BUILD_STATUS_COLORS[build.status]
        status_text = f"[{status_color}]{build.status.value.upper()}[/{status_color}]"
        is_live = getattr(build, "is_live", None)
        live_text = "[green]✓ LIVE[/green]" if is_live else "-"

        console.print(
            Panel(
                f"[bold]Build ID:[/bold] {build.id}\n"
                f"[bold]Agent ID:[/bold] {build.agent_id}\n"
                f"[bold]Status:[/bold] {status_text}\n"
                f"[bold]Live:[/bold] {live_text}\n"
                f"[bold]Error Message:[/bold] {getattr(build, 'error_message', None) or '-'}\n"
                f"[bold]Created At:[/bold] {build.created_at}\n"
                f"[bold]Updated At:[/bold] {build.updated_at}",
                title="Build Details",
                border_style="blue",
            )
        )

        if build.status == AgentBuildStatus.SUCCEEDED:
            if is_live:
                action_choices = [
                    questionary.Choice(title="Take Down", value="take_down"),
                    questionary.Choice(title="Cancel", value=None),
                ]
            else:
                action_choices = [
                    questionary.Choice(title="Make Live", value="live"),
                    questionary.Choice(title="Cancel", value=None),
                ]

            selected_action = await questionary.select(
                message=f"What would you like to do with build {build.id[:12]}...?",
                choices=action_choices,
                pointer="> ",
            ).ask_async()

            if not selected_action:
                console.print("[dim]No action selected.[/dim]")
                return

            if selected_action == "live":
                console.print("[yellow]Setting build as live...[/yellow]")
                await atoms_client.update_agent_build(
                    agent_id=agent_id,
                    build_id=build.id,
                    api_key=access_token,
                    is_live=True,
                )
                console.print(
                    f"[bold green]✓ Build {build.id[:12]}... is now LIVE![/bold green]"
                )
            elif selected_action == "take_down":
                console.print("[yellow]Taking down build...[/yellow]")
                await atoms_client.update_agent_build(
                    agent_id=agent_id,
                    build_id=build.id,
                    api_key=access_token,
                    is_live=False,
                )
                console.print(
                    f"[bold green]✓ Build {build.id[:12]}... has been taken down.[/bold green]"
                )

    # @app.command("logs")
    # def stream_build(
    #     build_id: str = typer.Argument(..., help="The build ID to stream logs for"),
    # ):
    #     """
    #     Stream build logs in real-time using Server-Sent Events.
    #     """
    #     asyncio.run(async_stream_build(build_id))

    # async def async_stream_build(build_id: str):
    #     """Async implementation of stream build command."""
    #     agent_id = project_config.get_agent_id()

    #     if not agent_id:
    #         console.print(
    #             "[red]Agent not initialized. Run 'smallestai agent init' first.[/red]"
    #         )
    #         return

    #     credentials = auth_client.get_credentials()
    #     if not credentials or not credentials.get("access_token"):
    #         console.print(
    #             "[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]"
    #         )
    #         raise typer.Exit(1)

    #     access_token = credentials["access_token"]

    #     console.print(f"[bold cyan]Streaming logs for build: {build_id}[/bold cyan]")
    #     console.print("[dim]Press Ctrl+C to stop streaming[/dim]\n")

    #     try:
    #         async for event in atoms_client.stream_agent_build(
    #             agent_id=agent_id,
    #             build_id=build_id,
    #             api_key=access_token,
    #         ):
    #             event_type = event.get("type")

    #             if event_type == "log":
    #                 console.print(f"[dim]LOG:[/dim] {event.get('message', '')}")
    #             elif event_type == "status":
    #                 status = event.get("status", "")
    #                 status_style = {
    #                     "SUCCEEDED": "[green]SUCCEEDED[/green]",
    #                     "BUILD_FAILED": "[red]BUILD_FAILED[/red]",
    #                     "DEPLOY_FAILED": "[red]DEPLOY_FAILED[/red]",
    #                     "PENDING": "[yellow]PENDING[/yellow]",
    #                     "BUILDING": "[yellow]BUILDING[/yellow]",
    #                     "DEPLOYING": "[yellow]DEPLOYING[/yellow]",
    #                 }.get(status, status)
    #                 console.print(f"[bold]STATUS:[/bold] {status_style}")

    #                 if status in ["SUCCEEDED", "BUILD_FAILED", "DEPLOY_FAILED"]:
    #                     console.print("\n[bold]Build stream ended.[/bold]")
    #                     break
    #             elif event_type == "error":
    #                 console.print(f"[red]ERROR:[/red] {event.get('message', '')}")
    #                 break

    #     except KeyboardInterrupt:
    #         console.print("\n[yellow]Streaming stopped by user.[/yellow]")
    #     except Exception as e:
    #         console.print(f"[red]Error streaming build logs: {e}[/red]")

    return app
