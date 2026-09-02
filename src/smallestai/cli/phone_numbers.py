"""`smallestai phone-numbers …` — list, search, rent, release, and import numbers.

Thin CLI over `client.atoms.phone_numbers`, matching the style of `smallestai calls`.
Rent/release/import are billable/stateful and prompt for confirmation.
"""

import json as _json
import typing

import typer
from rich.console import Console
from rich.table import Table

from smallestai.cli.lib.auth import AuthClient
from smallestai.cli.lib.client import make_client

console = Console()


def _data(resp):
    return getattr(resp, "data", resp)


def _items(data, key):
    """Pull a list off a response payload: either `data.<key>` or `data` itself
    when the payload is already a list."""
    return getattr(data, key, None) or (data if isinstance(data, list) else [])


def _attr_get(obj, key):
    """Read a field whether the SDK returned a model object or a plain dict."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def initialise_phone_numbers_app(auth_client: AuthClient):
    app = typer.Typer(name="phone-numbers", help="List, search, rent, release, and import numbers.")

    @app.command("list")
    def list_numbers(
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """List your phone numbers."""
        resp = make_client(auth_client).atoms.phone_numbers.list()
        data = _data(resp)
        items = _items(data, "phone_numbers")
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(items, default=str))
            return
        table = Table("ID", "Number", "Provider", "Active", "Agent", title=f"Phone numbers ({len(items)})")
        for x in items:
            attrs = _attr_get(x, "attributes")
            table.add_row(
                str(_attr_get(x, "id") or _attr_get(x, "product_id") or "—"),
                str(_attr_get(attrs, "phone_number") or "—"),
                str(_attr_get(attrs, "provider") or "—"),
                "yes" if _attr_get(x, "is_active") else "no",
                str(_attr_get(x, "agent_id") or "—"),
            )
        console.print(table)

    @app.command("search")
    def search_rentable(
        country_code: str = typer.Option(..., "--country-code", help="e.g. US, IN"),
        provider: str = typer.Option("twilio", "--provider", help="plivo | twilio"),
        area_code: str = typer.Option(None, "--area-code"),
        as_json: bool = typer.Option(False, "--json", help="Emit raw JSON"),
    ):
        """Search for rentable numbers."""
        kw: typing.Dict[str, typing.Any] = {"country_code": country_code, "provider": provider}
        if area_code:
            kw["area_code"] = area_code
        resp = make_client(auth_client).atoms.phone_numbers.search_rentable(**kw)
        data = _data(resp)
        items = _items(data, "phone_numbers")
        if as_json:
            console.print_json(resp.json() if hasattr(resp, "json") else _json.dumps(items, default=str))
            return
        table = Table("Number", "Provider", title=f"Rentable ({len(items)})")
        for x in items:
            num = x if isinstance(x, str) else (getattr(x, "phone_number", None) or getattr(x, "number", None))
            table.add_row(str(num or "—"), provider)
        console.print(table)

    @app.command("rent")
    def rent_number(
        phone_number: str = typer.Option(..., "--phone-number"),
        provider: str = typer.Option("twilio", "--provider", help="plivo | twilio"),
        yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    ):
        """Rent a phone number (billable)."""
        if not yes:
            typer.confirm(f"Rent {phone_number} via {provider}? This is billable.", abort=True)
        d = _data(make_client(auth_client).atoms.phone_numbers.rent(phone_number=phone_number, provider=provider))
        console.print(f"[green]Rented[/green] {phone_number} ({getattr(d, 'product_id', None) or d})")

    @app.command("release")
    def release_number(
        product_id: str = typer.Option(..., "--product-id"),
        yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    ):
        """Release a rented number."""
        if not yes:
            typer.confirm(f"Release number {product_id}?", abort=True)
        make_client(auth_client).atoms.phone_numbers.release(product_id=product_id)
        console.print(f"[red]Released[/red] {product_id}")

    @app.command("import-sip")
    def import_sip(
        phone_number: str = typer.Option(..., "--phone-number"),
        sip_termination_url: str = typer.Option(..., "--sip-termination-url"),
        name: str = typer.Option(None, "--name"),
        sip_username: str = typer.Option(None, "--sip-username"),
        sip_password: str = typer.Option(None, "--sip-password"),
    ):
        """Import an external SIP number."""
        kw: typing.Dict[str, typing.Any] = {"phone_number": phone_number, "sip_termination_url": sip_termination_url}
        if name:
            kw["name"] = name
        if sip_username:
            kw["sip_username"] = sip_username
        if sip_password:
            kw["sip_password"] = sip_password
        make_client(auth_client).atoms.phone_numbers.import_sip(**kw)
        console.print(f"[green]Imported SIP number[/green] {phone_number}")

    return app
