"""Shared SmallestAI client construction for the CLI.

Dogfoods the published `SmallestAI` client so the CLI and SDK stay in lockstep.
Auth resolves from SMALLEST_API_KEY, else the key stored by `smallestai auth
login`. SMALLEST_BASE_URL overrides the endpoint (dev rig).
"""

import os

import typer
from rich.console import Console

from smallestai.cli.lib.auth import AuthClient

console = Console()


def resolve_key(auth_client: AuthClient) -> str:
    key = os.environ.get("SMALLEST_API_KEY")
    if not key:
        creds = auth_client.get_credentials()
        key = (creds or {}).get("access_token")
    if not key:
        console.print("[red]No API key. Set SMALLEST_API_KEY or run `smallestai auth login`.[/red]")
        raise typer.Exit(1)
    return key


def make_client(auth_client: AuthClient):
    from smallestai import SmallestAI

    key = resolve_key(auth_client)
    base = os.environ.get("SMALLEST_BASE_URL")
    if base:
        from smallestai.environment import SmallestAIEnvironment

        base = base.rstrip("/")
        ws = base.replace("https://", "wss://").replace("http://", "ws://")
        env = SmallestAIEnvironment(atoms=f"{base}/atoms/v1", waves=base, waves_ws=ws, payment=base)
        return SmallestAI(api_key=key, environment=env)
    return SmallestAI(api_key=key)
