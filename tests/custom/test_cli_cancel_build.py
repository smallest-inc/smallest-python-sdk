"""Cancellation must never report success for an unperformed request."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
from typer.testing import CliRunner

from smallestai.cli.agent_crew import initialise_agent_crew_app
from smallestai.cli.lib.atoms import AtomsAPIClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,body,error",
    [
        (200, {"data": {"message": "Build cancelled"}}, None),
        (409, {"errors": ["Build already terminal"]}, "Build already terminal"),
        (500, None, "HTTP 500"),
        (307, None, "HTTP 307"),
        (302, {"data": {"message": "Build cancelled"}}, "HTTP 302"),
        (200, None, "invalid success response"),
        (200, {"data": {}}, "invalid success response"),
        (200, {"data": {"message": 42}}, "invalid success response"),
    ],
)
async def test_cancel_response(monkeypatch, status, body, error):
    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(status, json=body, headers={"Location": "https://other.example/cancel"})

    real_client = httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient", lambda: real_client(transport=httpx.MockTransport(respond)))
    api = AtomsAPIClient()
    api.base_url = "https://api.example"
    if error:
        with pytest.raises(Exception, match=error):
            await api.cancel_agent_build("agent", "build", "test-key")
    else:
        assert await api.cancel_agent_build("agent", "build", "test-key") == "Build cancelled"
    assert len(seen) == 1
    assert seen[0].method == "POST"
    assert str(seen[0].url) == "https://api.example/atoms/v1/sdk/agents/agent/builds/build/cancel"
    assert seen[0].headers["Authorization"] == "Bearer test-key"


@pytest.mark.parametrize("error", [None, "Build already terminal", "cancel failed (HTTP 307)."])
def test_cancel_cli_exit_status(error):
    cancel = AsyncMock(return_value="Build cancelled", side_effect=RuntimeError(error) if error else None)
    app = initialise_agent_crew_app(
        SimpleNamespace(get_agent_id=lambda: "agent"),
        SimpleNamespace(get_credentials=lambda: {"access_token": "test-key"}),
        SimpleNamespace(cancel_agent_build=cancel),
    )
    result = CliRunner().invoke(app, ["cancel", "build", "--yes"])
    assert result.exit_code == (1 if error else 0)
    assert ("Could not cancel" if error else "Build cancelled") in result.stdout
    cancel.assert_awaited_once_with(agent_id="agent", build_id="build", api_key="test-key")
