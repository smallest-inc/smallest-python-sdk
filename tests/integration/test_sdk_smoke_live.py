"""Fully-automated live smoke suite — the "nothing is broken" baseline.

Runs real SDK calls against a real environment (no telephony, no human), so every
SDK change can prove the core surface still works before layering a new feature on
top. All through the SDK, no raw HTTP.

    SMALLEST_API_KEY=sk_... poetry run pytest tests/integration/test_sdk_smoke_live.py -m integration -s
"""

import os
import time

import pytest

pytestmark = pytest.mark.integration

API_KEY = os.environ.get("SMALLEST_API_KEY")
BASE = os.environ.get("SMALLEST_BASE", "https://api.smallest.ai").rstrip("/")


def _client():
    from smallestai import SmallestAI
    from smallestai.environment import SmallestAIEnvironment

    if "dev" in BASE:
        env = SmallestAIEnvironment(
            atoms=f"{BASE}/atoms/v1", waves=BASE, waves_ws=BASE.replace("http", "ws"), payment=BASE
        )
        return SmallestAI(api_key=API_KEY, environment=env)
    return SmallestAI(api_key=API_KEY)


def _data(resp):
    d = getattr(resp, "data", resp)
    return d.model_dump() if hasattr(d, "model_dump") else d


pytestmark = [pytest.mark.integration, pytest.mark.skipif(not API_KEY, reason="set SMALLEST_API_KEY")]


def test_agent_create_read_roundtrip_and_archive():
    client = _client()
    stamp = str(int(time.time()))[-6:]
    created = _data(client.atoms.agents.create_agent(name=f"zzz-smoke-{stamp}", global_prompt="smoke"))
    agent_id = created if isinstance(created, str) else created.get("_id") or created.get("id")
    assert agent_id, f"create_agent returned no id: {created}"
    try:
        got = _data(client.atoms.agents.get_agent(agent_id))
        got_id = got.get("_id") or got.get("id") if isinstance(got, dict) else agent_id
        assert str(got_id) == str(agent_id), "get_agent did not round-trip the agent id"
    finally:
        client.atoms.agents.archive_agent(agent_id)


def test_phone_numbers_list():
    client = _client()
    nums = _data(client.atoms.phone_numbers.list())
    assert isinstance(nums, list), f"phone_numbers.list() should return a list, got {type(nums)}"
    # Shape check on the first entry, if any.
    if nums:
        p = nums[0] if isinstance(nums[0], dict) else _data(nums[0])
        assert "_id" in p and "attributes" in p, f"unexpected phone-number shape: {list(p)[:6]}"
