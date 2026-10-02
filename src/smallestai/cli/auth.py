import asyncio
import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt

from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient

console = Console()


def initialise_auth_app(auth_client: AuthClient, atoms_client: AtomsAPIClient):
    auth_app = typer.Typer(name="auth")

    @auth_app.command()
    def login(
        base_url: Optional[str] = typer.Option(
            None,
            "--base-url",
            help=(
                "Regional API host to pin, e.g. https://api.india.smallest.ai. "
                "Persisted so you don't need to set SMALLEST_BASE_URL on every command."
            ),
        ),
    ):
        asyncio.run(async_login(base_url))

    async def async_login(base_url: Optional[str] = None):
        # Validate the key against the chosen regional host (if any), and reuse it below.
        if base_url:
            atoms_client.base_url = base_url.rstrip("/")

        # Prefer the env var so `SMALLEST_API_KEY=... smallestai auth login` is non-interactive.
        api_key = os.environ.get("SMALLEST_API_KEY")
        if not api_key:
            if sys.stdin.isatty():
                console.print("[bold cyan]Smallest API Key[/bold cyan]")
                console.print("[dim]Enter your Smallest API key from https://app.smallest.ai/dashboard/api-keys[/dim]")
                api_key = Prompt.ask("> ", password=True)
            else:
                # Piped stdin (e.g. `echo $KEY | smallestai auth login`): read directly
                # instead of getpass, which emits a GetPassWarning on a non-TTY.
                api_key = sys.stdin.readline().strip()

        if not api_key:
            console.print("[red]No API key provided. Set SMALLEST_API_KEY or run in an interactive terminal.[/red]")
            raise typer.Exit(1)

        try:
            account_details = await atoms_client.get_account_details(api_key)
        except Exception:
            console.print("[red]Invalid API key[/red]")
            return

        auth_client.login(api_key, base_url=base_url)
        console.print(f"[bold green]Login successful [bold green]{account_details.userEmail}[/bold green]")
        if base_url:
            console.print(f"[dim]Region host pinned: {base_url.rstrip('/')}[/dim]")

    @auth_app.command()
    def logout():
        auth_client.logout()
        console.print("[bold green]Logout successful[/bold green]")

    return auth_app
