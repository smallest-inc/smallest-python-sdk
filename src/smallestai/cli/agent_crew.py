from __future__ import annotations

import asyncio
import base64
import json as _json
import sys
from collections import deque
from io import BytesIO
from pathlib import Path
from typing import Optional

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from smallestai.cli.lib.atoms import AgentBuildStatus, AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.chat import ChatClient, chat_loop
from smallestai.cli.lib.client import make_client
from smallestai.cli.lib.ownership import SUMMARY as OWNERSHIP_SUMMARY
from smallestai.cli.lib.ownership import render_ownership
from smallestai.cli.lib.project_config import ProjectConfig
from smallestai.cli.lib.scrub import scrub_internal
from smallestai.cli.utils import create_zip_from_directory, find_required_env_vars

AGENT_BUILD_STATUS_COLORS = {
    AgentBuildStatus.SUCCEEDED: "green",
    AgentBuildStatus.BUILD_FAILED: "red",
    AgentBuildStatus.DEPLOY_FAILED: "red",
    AgentBuildStatus.QUEUED: "yellow",
    AgentBuildStatus.BUILDING: "yellow",
    AgentBuildStatus.DEPLOYING: "yellow",
}

console = Console()


def _print_error(prefix: str, err: object) -> None:
    """Single choke-point for crew error output. Always scrubs cluster-internal
    topology out of the message, regardless of the exception type that produced
    it (httpx errors, orchestrator 5xx bodies, raw tracebacks all flow through
    here), so no error path can leak infra."""
    console.print(f"[red]{prefix}: {scrub_internal(str(err))}[/red]")


def initialise_agent_crew_app(project_config: ProjectConfig, auth_client: AuthClient, atoms_client: AtomsAPIClient):
    app = typer.Typer(name="agent-crew")

    def _resolve_agent_id(arg: Optional[str]) -> str:
        """Explicit --agent-id wins; otherwise fall back to the linked project agent."""
        agent_id = arg or project_config.get_agent_id()
        if not agent_id:
            console.print(
                "[red]No agent linked. Run [bold]smallestai agent-crew init[/bold] in this "
                "directory, or pass [bold]--agent-id <id>[/bold].[/red]"
            )
            raise typer.Exit(1)
        return agent_id

    @app.command()
    def init(
        agent_id: Optional[str] = typer.Option(
            None,
            "--agent-id",
            help="Link this agent id directly, skipping the interactive picker (required in non-TTY environments like CI).",
        ),
    ):
        """Initialize the agent-crew configuration in the current directory."""
        asyncio.run(async_init(agent_id))

    async def async_init(agent_id_arg: Optional[str] = None):
        """Async implementation of init command."""
        agent_id = project_config.get_agent_id()

        if agent_id:
            console.print(f"[green]Agent already initialized with ID: [bold]{agent_id}[/bold][/green]")
            return

        # Non-interactive path: link the provided id directly, no picker.
        if agent_id_arg:
            project_config.set_agent_id(agent_id_arg)
            console.print(f"[green]Agent initialized successfully with ID: [bold]{agent_id_arg}[/bold][/green]")
            _print_ownership_hint()
            return

        # Without an id, the picker needs a real TTY — fail clearly instead of crashing.
        if not sys.stdin.isatty():
            console.print("[red]init requires an interactive terminal. Pass --agent-id <id> to skip the picker.[/red]")
            raise typer.Exit(1)

        # Check if user is logged in
        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print("[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]")
            raise typer.Exit(1)

        access_token = credentials["access_token"]

        console.print("[dim]Fetching agents...[/dim]")
        try:
            agent_data = await atoms_client.get_agents(access_token)
        except Exception as e:
            _print_error("Error fetching agents", e)
            return

        if not agent_data.agents:
            console.print(
                "[yellow]No agents found. Create an agent first at https://app.smallest.ai/dashboard[/yellow]"
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
        _print_ownership_hint()

    def _print_ownership_hint():
        console.print(
            Panel(
                OWNERSHIP_SUMMARY + "\n\n[dim]Run [bold]smallestai agent-crew doctor[/bold] to check this "
                "agent's config for common gotchas.[/dim]",
                title="What your crew controls vs the platform",
                border_style="cyan",
            )
        )

    @app.command()
    def deploy(
        entry_point: str = typer.Option(
            "server.py",
            "--entry-point",
            "-e",
            help="Entry point file name (e.g., server.py)",
        ),
        agent_id: Optional[str] = typer.Option(
            None, "--agent-id", help="Agent id to deploy to (defaults to the linked project agent)."
        ),
    ):
        """
        Deploy an agent crew to the Atoms platform.

        Packages the agent-crew code directory into a zip file and deploys it to the backend.
        """
        asyncio.run(async_deploy(".", entry_point, agent_id))

    async def async_deploy(directory: str, entry_point: str, agent_id_arg: Optional[str] = None):
        """Deploy an agent crew asynchronously."""
        agent_id = _resolve_agent_id(agent_id_arg)

        # Check if user is logged in
        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print("[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]")
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
            console.print(f"[red]Error: Entry point file '{entry_point}' not found in '{directory}'.[/red]")
            return

        console.print(f"[bold cyan]Deploying agent from: {dir_path.absolute()}[/bold cyan]")
        console.print(f"[dim]Entry point: {entry_point}[/dim]")
        console.print(f"[dim]Agent ID: {agent_id}[/dim]\n")

        # Pre-flight layout note. Both a flat directory (server.py +
        # requirements.txt at the root) and a src/ layout with a pyproject.toml
        # build and run in the cloud. Flat + requirements.txt is what the cookbook
        # examples ship and the best-tested path, so nudge toward it without
        # blocking anything. One gotcha for pyproject projects: all runtime deps
        # must be declared there (smallestai already pulls in the crew server's
        # deps, so this is usually covered).
        has_pyproject = (dir_path / "pyproject.toml").exists()
        has_requirements = (dir_path / "requirements.txt").exists()
        has_src_dir = (dir_path / "src").is_dir()
        nested_entry = ("/" in entry_point) or ("\\" in entry_point)
        if has_src_dir or nested_entry or (has_pyproject and not has_requirements):
            console.print(
                "[dim]Note: src/ + pyproject.toml layouts deploy fine. The simplest, "
                "best-tested path is a flat directory with server.py + a "
                "requirements.txt at the root (what the cookbook getting_started "
                "example ships). If you use a pyproject with no requirements.txt, make "
                "sure every runtime dependency is declared in it.[/dim]\n"
            )

        # Scan user code for env var references and warn — the deploy pipeline
        # does not yet propagate `.env` values into the pod, so any env var
        # the code reads must either be baked into the image or the call will
        # fail at runtime with the cryptic "Missing credentials" message most
        # client libraries produce.
        required_env_vars = find_required_env_vars(dir_path)
        # SMALLEST_API_KEY is set by the platform; ignore from the warning list.
        required_env_vars.discard("SMALLEST_API_KEY")
        if required_env_vars:
            console.print("[yellow]⚠  Your code references these environment variables:[/yellow]")
            for var in sorted(required_env_vars):
                console.print(f"    [yellow]• {var}[/yellow]")
            console.print(
                "[dim]Platform-level env injection isn't available yet, but there is a "
                "working path: put these in a `.env` file at your project root and call "
                "`load_dotenv()` at startup (the cookbook examples already do). The `.env` "
                "ships with your deploy and is loaded in the pod, so your code reads them "
                "via `os.getenv(...)`. Without it, calls fail at first use "
                "(e.g. `openai.OpenAIError: Missing credentials`).[/dim]\n"
            )

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

            console.print("[bold green]✓ Deployment uploaded![/bold green]")
            console.print(f"[dim]Build ID: {result.build_id}[/dim]")

            # Poll the build to a terminal state instead of returning at "queued".
            # The build has to reach SUCCEEDED before you can Make Live, so
            # surfacing the real status here saves guessing.
            console.print("[yellow]Building (this usually takes 1-2 min)...[/yellow]")
            terminal = {"SUCCEEDED", "BUILD_FAILED", "DEPLOY_FAILED", "FAILED"}
            last = None
            status = None
            for _ in range(60):  # ~5 min cap at 5s intervals
                try:
                    build = await atoms_client.get_agent_build(
                        agent_id=agent_id,
                        build_id=result.build_id,
                        api_key=access_token,
                    )
                    status = str(getattr(build.status, "value", build.status))
                except Exception:
                    status = None
                if status and status != last:
                    console.print(f"[dim]  {status}[/dim]")
                    last = status
                if status in terminal:
                    break
                await asyncio.sleep(5)

            if status == "SUCCEEDED":
                console.print("[bold green]✓ Build succeeded.[/bold green]")
                console.print(
                    "[dim]Next: `smallestai agent-crew builds` -> Make Live, then "
                    "wait for it to show Live before placing your first call.[/dim]"
                )
            elif status in terminal:
                console.print(
                    f"[red]Build ended with status: {status}. Check `smallestai agent-crew logs` for details.[/red]"
                )
            else:
                console.print(
                    "[yellow]Still building. Check `smallestai agent-crew builds` for the final status.[/yellow]"
                )

        except Exception as e:
            # Scrub cluster-internal topology out of transport/API errors.
            _print_error("Error deploying agent", e)

    @app.command()
    def chat(
        url: Optional[str] = typer.Option(
            None,
            "--url",
            help="WebSocket URL to connect to. Defaults to ws://localhost:8080/ws.",
        ),
    ):
        """
        Start a chat session with an Atoms agent crew.

        Connect to a WebSocket server running an Atoms agent crew (e.g. `python app.py`)
        and chat interactively. Use --url to target a non-default host/port or a remote
        deployment (e.g. --url wss://staging.smallest.ai/ws/agent/<id>).
        """
        ws_url = url or "ws://localhost:8080/ws"

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
        build_id: str = typer.Argument(None, help="Optional build ID to manage directly"),
        agent_id: Optional[str] = typer.Option(
            None, "--agent-id", help="Agent id (defaults to the linked project agent)."
        ),
        limit: int = typer.Option(50, "--limit", "-l", help="Number of builds to fetch"),
        offset: int = typer.Option(0, "--offset", help="Offset for pagination"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON (non-interactive)"),
    ):
        """
        List all builds for the current agent crew and manage them interactively.

        If a build_id is provided, directly manage that specific build. With --json
        or in a non-interactive terminal, list and exit without the picker.
        """
        asyncio.run(async_list_builds(build_id, agent_id, limit, offset, as_json))

    async def async_list_builds(
        build_id: str | None, agent_id_arg: Optional[str], limit: int, offset: int, as_json: bool
    ):
        """Async implementation of list builds command."""
        agent_id = _resolve_agent_id(agent_id_arg)

        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print("[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]")
            raise typer.Exit(1)

        access_token = credentials["access_token"]

        try:
            if build_id:
                build = await atoms_client.get_agent_build(
                    agent_id=agent_id,
                    build_id=build_id,
                    api_key=access_token,
                )
                if as_json:
                    console.print_json(
                        _json.dumps(
                            {
                                "id": build.id,
                                "status": build.status.value,
                                "is_live": build.is_live,
                                "created_at": build.created_at,
                            },
                            default=str,
                        )
                    )
                    return
                await _manage_build(agent_id, build, access_token)
                return

            result = await atoms_client.list_agent_builds(
                agent_id=agent_id,
                api_key=access_token,
                limit=limit,
                offset=offset,
            )

            if as_json:
                console.print_json(
                    _json.dumps(
                        [
                            {"id": b.id, "status": b.status.value, "is_live": b.is_live, "created_at": b.created_at}
                            for b in result.builds
                        ],
                        default=str,
                    )
                )
                return

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
                status_text = f"[{status_color}]{build.status.value.upper()}[/{status_color}]"

                live_indicator = "[green]✓ LIVE[/green]" if build.is_live else "-"

                table.add_row(
                    build.id,
                    status_text,
                    live_indicator,
                    build.created_at,
                )

            console.print(table)
            console.print(f"[dim]Showing {len(result.builds)} of {result.pagination.total} builds[/dim]\n")

            # No interactive picker outside a real terminal (would hang in CI).
            if not sys.stdin.isatty():
                console.print(
                    "[dim]Manage a build directly: [bold]smallestai agent-crew builds <build-id>[/bold] "
                    "(add [bold]--agent-id[/bold] outside a project dir).[/dim]"
                )
                return

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
            _print_error("Error", e)

    async def _manage_build(agent_id: str, build, access_token: str):
        """Show action menu and manage a specific build."""
        status_color = AGENT_BUILD_STATUS_COLORS[build.status]
        status_text = f"[{status_color}]{build.status.value.upper()}[/{status_color}]"
        is_live = getattr(build, "is_live", None)
        live_text = "[green]✓ LIVE[/green]" if is_live else "-"

        # Mask cluster-internal topology (svc URLs, pod names) out of the raw
        # error message. If the failure is purely internal infra (nothing left
        # after scrubbing), show a clean support line instead of a bare mask.
        raw_err = getattr(build, "error_message", None)
        if raw_err:
            scrubbed = scrub_internal(raw_err).strip()
            if scrubbed in ("", "[internal]"):
                err_text = f"build failed to start (id {build.id}); contact support"
            else:
                err_text = scrubbed
        else:
            err_text = "-"

        console.print(
            Panel(
                f"[bold]Build ID:[/bold] {build.id}\n"
                f"[bold]Agent ID:[/bold] {build.agent_id}\n"
                f"[bold]Status:[/bold] {status_text}\n"
                f"[bold]Live:[/bold] {live_text}\n"
                f"[bold]Error Message:[/bold] {err_text}\n"
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
                console.print(f"[bold green]✓ Build {build.id[:12]}... is now LIVE![/bold green]")
            elif selected_action == "take_down":
                confirmed = await questionary.confirm(
                    f"Take build {build.id[:12]}... offline? This stops the agent serving calls."
                ).ask_async()
                if not confirmed:
                    console.print("[dim]Left the build live.[/dim]")
                    return
                console.print("[yellow]Taking down build...[/yellow]")
                await atoms_client.update_agent_build(
                    agent_id=agent_id,
                    build_id=build.id,
                    api_key=access_token,
                    is_live=False,
                )
                console.print(f"[bold green]✓ Build {build.id[:12]}... has been taken down.[/bold green]")

    @app.command("logs")
    def build_logs(
        build_id: str = typer.Argument(None, help="Build ID to stream logs for (defaults to the latest build)"),
        agent_id: Optional[str] = typer.Option(
            None, "--agent-id", help="Agent id (defaults to the linked project agent)."
        ),
        verbose: bool = typer.Option(
            False, "--verbose", "-v", help="Stream every log line (full build log), not just status."
        ),
    ):
        """Stream a build's status (compile + deploy) in real time.

        With no build ID, streams the most recent build for the current agent.
        By default this shows the status progression (queued -> building ->
        deploying -> succeeded/failed) and, if the build fails, the last few log
        lines so you can see why. Pass --verbose to stream every log line as it
        arrives. Cluster-internal infra (pod names, service URLs, IPs) is masked
        either way; the CLI never prints raw topology.
        """
        asyncio.run(async_build_logs(build_id, agent_id, verbose))

    async def async_build_logs(build_id: str | None, agent_id_arg: Optional[str] = None, verbose: bool = False):
        agent_id = _resolve_agent_id(agent_id_arg)

        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print("[red]Error: You must be logged in first. Run 'smallestai auth login'[/red]")
            raise typer.Exit(1)
        access_token = credentials["access_token"]

        if not build_id:
            result = await atoms_client.list_agent_builds(agent_id=agent_id, api_key=access_token, limit=1, offset=0)
            if not result.builds:
                console.print("[yellow]No builds found. Run 'smallestai agent-crew deploy' first.[/yellow]")
                raise typer.Exit(1)
            build_id = result.builds[0].id
            console.print(f"[dim]Latest build: {build_id}[/dim]")

        console.print(f"[bold cyan]Streaming build {build_id[:12]}...[/bold cyan]  [dim](Ctrl+C to stop)[/dim]\n")

        terminal = {"SUCCEEDED", "BUILD_FAILED", "DEPLOY_FAILED"}
        failed = {"BUILD_FAILED", "DEPLOY_FAILED"}
        # Every log line is scrubbed before it is ever printed, in both modes, so
        # no CLI invocation can leak cluster-internal topology. --verbose only
        # controls volume: stream every (scrubbed) line vs. status + a bounded
        # tail shown on failure.
        TAIL_LINES = 25
        tail: deque[str] = deque(maxlen=TAIL_LINES)

        def _flush_tail() -> None:
            if verbose or not tail:
                return
            console.print(f"\n[dim]── last {len(tail)} log lines ──[/dim]")
            for line in tail:
                console.print(line, highlight=False)

        if not verbose:
            console.print(
                "[dim]Showing build status. The full build log is shown on failure "
                "(last 25 lines) or with --verbose. Internal infra is always masked.[/dim]\n"
            )

        try:
            async for event in atoms_client.stream_agent_build(
                agent_id=agent_id, build_id=build_id, access_token=access_token
            ):
                etype = event.get("type")
                if etype == "log":
                    msg = scrub_internal(event.get("message", ""))
                    if verbose:
                        console.print(msg, highlight=False)
                    else:
                        tail.append(msg)
                elif etype == "status":
                    status = str(event.get("status", ""))
                    color = {"SUCCEEDED": "green", "BUILD_FAILED": "red", "DEPLOY_FAILED": "red"}.get(status, "yellow")
                    console.print(f"[bold {color}]● {status}[/bold {color}]")
                    if status in failed:
                        _flush_tail()
                    if status in terminal:
                        break
                elif etype == "error":
                    msg = event.get("message", "")
                    console.print(f"[red]error:[/red] {scrub_internal(msg)}")
                    _flush_tail()
                    break
        except KeyboardInterrupt:
            console.print("\n[yellow]Stopped.[/yellow]")
        except Exception as e:
            _print_error("Error streaming build logs", e)
            raise typer.Exit(1)

    @app.command()
    def doctor(
        agent_id: Optional[str] = typer.Option(
            None,
            "--agent-id",
            help="Agent id to inspect. Defaults to the agent linked in this project.",
        ),
    ):
        """Check a crew agent's config for common gotchas (live build, redaction, dashboard tools)."""
        asyncio.run(async_doctor(agent_id))

    async def async_doctor(agent_id_arg: Optional[str]):
        agent_id = agent_id_arg or project_config.get_agent_id()
        if not agent_id:
            console.print("[red]No agent id. Pass --agent-id <id>, or run `init` first.[/red]")
            raise typer.Exit(1)

        credentials = auth_client.get_credentials()
        if not credentials or not credentials.get("access_token"):
            console.print("[red]You must be logged in. Run 'smallestai auth login'.[/red]")
            raise typer.Exit(1)
        token = credentials["access_token"]

        console.print(f"[dim]Inspecting agent {agent_id}...[/dim]")
        try:
            # Use the published SDK client (API-key auth), the same path as
            # `smallestai agents get`. The single-agent endpoint rejects the
            # session bearer token with a 400, so the hand-rolled fetch failed.
            dto = make_client(auth_client).atoms.agents.get_agent(id=agent_id).data
            # .json() serializes by alias -> the camelCase shape used below.
            agent = _json.loads(dto.json()) if dto is not None else {}
        except Exception as e:
            _print_error("Could not fetch agent", e)
            raise typer.Exit(1)
        try:
            builds = await atoms_client.list_agent_builds(agent_id, token)
            build_items = builds.builds
        except Exception:
            build_items = []

        oks: list[str] = []
        warns: list[str] = []

        live = [b for b in build_items if b.is_live]
        if live:
            oks.append(f"A crew build is live ({live[0].id[:12]}...).")
        else:
            warns.append(
                "No live crew build. Run `agent-crew deploy`, then make the build live, "
                "or your crew code will not serve."
            )

        wft = agent.get("workflowType")
        if wft and wft != "single_prompt":
            warns.append(f"workflowType is '{wft}'. A crew attaches to single_prompt agents.")

        if (agent.get("redactionConfig") or {}).get("isEnabled"):
            warns.append(
                "PII redaction is ON. It rewrites emails/names/numbers in the transcript "
                "(and can trim leading words like 'my email address is'). Set "
                "redactionConfig.isEnabled off if you don't want it."
            )
        else:
            oks.append("PII redaction is off.")

        sp = (agent.get("workflow") or {}).get("singlePromptConfig") or agent.get("singlePromptConfig") or {}
        tools = sp.get("tools") or []
        tool_repr = " ".join(str(t).lower() for t in tools)
        if "transfer" in tool_repr:
            warns.append(
                "The dashboard Tools panel has transfer_call enabled. For a crew agent that "
                "panel is ignored (your code-side @function_tool is used). Leave it off to "
                "avoid confusion."
            )

        console.print()
        for m in oks:
            console.print(f"[green]OK[/green]   {m}")
        for m in warns:
            console.print(f"[yellow]WARN[/yellow] {m}")
        if not warns:
            console.print("[bold green]No issues found.[/bold green]")
        console.print()
        render_ownership(console)

    return app
