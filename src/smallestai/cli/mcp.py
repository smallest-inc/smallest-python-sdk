"""`smallestai mcp` - set up or run the Smallest AI MCP server.

The MCP server (github.com/smallest-inc/mcp-server, npm ``@smallest-ai/mcp-server``) gives
Cursor, Claude, and other MCP clients native access to Waves + Atoms. It runs on Node via
npx; this command prints the client config and can launch it for you.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess

import typer
from rich.console import Console
from rich.syntax import Syntax

console = Console()

_NPM_PKG = "@smallest-ai/mcp-server"


def _config_snippet() -> str:
    return json.dumps(
        {
            "mcpServers": {
                "smallest-ai": {
                    "command": "npx",
                    "args": ["-y", _NPM_PKG],
                    "env": {"SMALLEST_API_KEY": "your-api-key-here"},
                }
            }
        },
        indent=2,
    )


def initialise_mcp_app() -> typer.Typer:
    app = typer.Typer(
        name="mcp",
        help="Set up or run the Smallest AI MCP server (for Cursor, Claude, etc.).",
        no_args_is_help=False,
    )

    @app.callback(invoke_without_command=True)
    def _root(ctx: typer.Context) -> None:
        if ctx.invoked_subcommand is not None:
            return
        console.print(
            "[bold]Smallest AI MCP server[/bold] gives Cursor, Claude, and other MCP "
            "clients native access to Waves + Atoms.\n"
        )
        console.print("[dim]Requires Node.js 18+ and a SMALLEST_API_KEY.[/dim]\n")
        console.print("Claude Code:")
        console.print(f"  [cyan]claude mcp add smallest-ai -- npx -y {_NPM_PKG}[/cyan]\n")
        console.print("Cursor / Claude Desktop - add to your mcp.json:")
        console.print(Syntax(_config_snippet(), "json", theme="ansi_dark"))
        console.print("\n  [dim]Or run it directly: [bold]smallestai mcp run[/bold][/dim]")

    @app.command("run")
    def run() -> None:
        """Run the MCP server locally via npx (Node.js 18+ required)."""
        if not shutil.which("npx"):
            console.print("[red]npx not found. Install Node.js 18+ from https://nodejs.org.[/red]")
            raise typer.Exit(1)
        if not os.getenv("SMALLEST_API_KEY"):
            console.print("[yellow]SMALLEST_API_KEY is not set; the MCP server needs it.[/yellow]")
        console.print(f"[dim]Launching {_NPM_PKG} via npx (Ctrl-C to stop)...[/dim]")
        try:
            subprocess.run(["npx", "-y", _NPM_PKG], check=False)
        except KeyboardInterrupt:
            pass

    @app.command("config")
    def config() -> None:
        """Print the mcp.json config snippet."""
        console.print(Syntax(_config_snippet(), "json", theme="ansi_dark"))

    return app
