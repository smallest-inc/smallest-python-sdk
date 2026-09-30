"""Live integration test for the realtime register-call -> websocket flow.

This is the flow a customer follows and the one they reported broken with a 401:
mint a short-lived token with the SDK's ``register_call``, open the documented
websocket URL with ``?token=``, and confirm the session comes up and the agent
produces a spoken turn.

It is skipped unless ``SMALLEST_API_KEY`` is set, so the normal WireMock CI run
(no live credentials) skips it. Run it against the live API with::

    SMALLEST_API_KEY=sk_... poetry run pytest tests/custom/test_realtime_integration.py -m integration -s

Optionally set ``SMALLEST_AGENT_ID`` to reuse a specific agent; otherwise the test
picks the first agent on the account.
"""

import asyncio
import json
import os
import ssl

import pytest

pytestmark = pytest.mark.integration

API_KEY = os.environ.get("SMALLEST_API_KEY")

pytest.importorskip("websockets")
import websockets  # noqa: E402


def _first_agent_id(client) -> str:
    override = os.environ.get("SMALLEST_AGENT_ID")
    if override:
        return override
    page = client.atoms.agents.list_agents()
    data = getattr(page, "data", page)
    agents = getattr(data, "agents", None) or getattr(data, "data", None) or []
    assert agents, "no agents on this account; set SMALLEST_AGENT_ID"
    first = agents[0]
    return getattr(first, "id", None) or getattr(first, "_id", None) or first["id"]


@pytest.mark.skipif(not API_KEY, reason="SMALLEST_API_KEY not set; live test skipped")
def test_register_call_then_connect_and_hear_the_agent():
    from smallestai import SmallestAI

    client = SmallestAI(api_key=API_KEY)
    agent_id = _first_agent_id(client)

    # 1. SDK mints a short-lived, single-use access token.
    token = client.atoms.realtime.register_call(agent_id=agent_id).data.access_token
    assert token.startswith("wct_"), f"expected a wct_ token, got {token[:8]!r}"

    # 2. Open the documented websocket URL with ?token= and drive a turn.
    url = f"wss://api.smallest.ai/atoms/v1/agent/connect?token={token}"

    async def run():
        types = []
        got_audio = False
        async with websockets.connect(url, ssl=ssl.create_default_context(), open_timeout=20) as ws:
            # Collect frames for up to 15s: the session, then the agent's first spoken turn.
            # asyncio.wait_for (not asyncio.timeout) so this runs on Python 3.9+.
            loop = asyncio.get_event_loop()
            deadline = loop.time() + 15
            try:
                while True:
                    remaining = deadline - loop.time()
                    if remaining <= 0:
                        break
                    raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
                    msg = json.loads(raw) if isinstance(raw, (str, bytes)) else {}
                    t = msg.get("type", "")
                    types.append(t)
                    # audio arrives as base64 payloads on audio/response events
                    if "audio" in t or msg.get("audio") or "audio" in msg.get("data", {}):
                        got_audio = True
                    if got_audio and len(types) >= 3:
                        break
            except (asyncio.TimeoutError, websockets.ConnectionClosed):
                pass
        return types, got_audio

    types, got_audio = asyncio.run(run())

    # 3. The handshake the customer said failed with 401: the session must come up.
    assert "session.created" in types, f"session never established; frames={types}"
    # 4. The pipeline is live end to end: the agent produced at least one spoken turn.
    assert got_audio, f"no audio from the agent; frames seen={types}"
