import httpx
import pytest

from smallestai import AsyncSmallestAI, SmallestAI
from smallestai.atoms.realtime.types.register_call_realtime_response_data import RegisterCallRealtimeResponseData


@pytest.mark.parametrize("websocket_url", [None, "wss://us.example.com/atoms/v1/agent/connect"])
def test_register_call_parses_optional_regional_websocket_url(websocket_url):
    payload = {"access_token": "wct_test", "expires_in": 30}
    if websocket_url is not None:
        payload["websocket_url"] = websocket_url
    with httpx.Client(
        transport=httpx.MockTransport(lambda _: httpx.Response(201, json={"status": True, "data": payload}))
    ) as http:
        client = SmallestAI(api_key="test", httpx_client=http)
        result = client.atoms.realtime.register_call(agent_id="agent")
    assert result.data.websocket_url == websocket_url
    assert result.data.access_token == "wct_test"


@pytest.mark.asyncio
async def test_async_register_call_preserves_regional_websocket_url():
    target = "wss://us.example.com/atoms/v1/agent/connect"
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(201, json={"data": {"websocket_url": target}}))
    ) as http:
        client = AsyncSmallestAI(api_key="test", httpx_client=http)
        result = await client.atoms.realtime.register_call(agent_id="agent")
    assert result.data.websocket_url == target


def test_websocket_url_is_a_declared_optional_response_field():
    # Extra-field parsing alone would hide a missing generated contract.
    fields = getattr(RegisterCallRealtimeResponseData, "model_fields", None)
    if fields is None:
        fields = RegisterCallRealtimeResponseData.__fields__
    assert "websocket_url" in fields
    assert RegisterCallRealtimeResponseData().websocket_url is None
