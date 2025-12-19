import asyncio

import typer
from rich.console import Console
from rich.prompt import Prompt

from smallestai.cli.lib.atoms import AtomsAPIClient
from smallestai.cli.lib.auth import AuthClient

console = Console()


def initialise_auth_app(auth_client: AuthClient, atoms_client: AtomsAPIClient):
    auth_app = typer.Typer(name="auth")

    @auth_app.command()
    def login():
        asyncio.run(async_login())

    async def async_login():
        console.print("[bold cyan]Smallest API Key[/bold cyan]")
        console.print(
            "[dim]Enter your Smallest API key from https://console.smallest.ai/apikeys[/dim]"
        )
        api_key = Prompt.ask("> ", password=True)

        try:
            account_details = await atoms_client.get_account_details(api_key)
        except Exception:
            console.print("[red]Invalid API key[/red]")
            return

        auth_client.login(api_key)
        console.print(
            f"[bold green]Login successful [bold green]{account_details.userEmail}[/bold green]"
        )

    @auth_app.command()
    def logout():
        auth_client.logout()
        console.print("[bold green]Logout successful[/bold green]")

    return auth_app
