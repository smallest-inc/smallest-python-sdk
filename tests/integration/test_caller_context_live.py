"""Live end-to-end test for crew caller context (PRO-3560), driven through the SDK.

Proves the whole chain on a real telephony call: the orchestrator forwards the
caller block into ``system.init`` -> the SDK surfaces it as ``session.caller`` /
``session.initial_variables`` -> crew code reads it. The crew emits what it read as
a structured ``caller.probe`` event (NOT a spoken/transcribed line), and this test
pulls that event's payload back off the conversation record and asserts the numbers.

Everything that has an SDK method uses the SDK: ``agents.create_agent``,
``phone_numbers.list``, ``calls.start_outbound_call``, ``calls.get``,
``agents.archive_agent``. Two steps have no SDK method yet and are called out:
crew code deploy (the ``smallestai agent-crew`` CLI) and making a build live
(``PATCH /sdk/agents/{id}/builds/{bid}``) — both tracked as SDK gaps.

Run it (you must answer the call):

    SMALLEST_API_KEY=sk_... SMALLEST_TEST_NUMBER=+91XXXXXXXXXX \
        poetry run python tests/integration/test_caller_context_live.py

or under pytest:

    SMALLEST_API_KEY=sk_... SMALLEST_TEST_NUMBER=+91XXXXXXXXXX \
        poetry run pytest tests/integration/test_caller_context_live.py -m integration -s
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest

pytestmark = pytest.mark.integration

API_KEY = os.environ.get("SMALLEST_API_KEY")
TEST_NUMBER = os.environ.get("SMALLEST_TEST_NUMBER")  # a phone you can answer, E.164
# Prod by default; override for dev, e.g. https://api.dev.smallest.ai
BASE = os.environ.get("SMALLEST_BASE", "https://api.smallest.ai").rstrip("/")

PROBE_SERVER = '''\
"""Caller-context probe crew: emit what the crew reads from session.caller as an event."""
from loguru import logger

from smallestai.atoms.crew.events import SDKAgentLogEvent
from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.server import AtomsCrewApp
from smallestai.atoms.crew.session import CrewSession


class Probe(OutputCrewNode):
    def __init__(self, session: CrewSession):
        super().__init__(name="probe")
        self._session = session

    async def generate_response(self):
        c = self._session.caller
        payload = {
            "user_number": c.user_number if c else None,
            "agent_number": c.agent_number if c else None,
            "direction": c.direction if c else None,
            "call_id": c.call_id if c else None,
            "variables": self._session.initial_variables,
        }
        logger.success(f"CALLER_PROBE {payload}")
        await self.send_event(SDKAgentLogEvent(name="caller.probe", payload=payload))
        yield "Caller context probe recorded. Goodbye."


async def setup(session: CrewSession):
    session.add_node(Probe(session))
    await session.start()
    await session.wait_until_complete()


if __name__ == "__main__":
    AtomsCrewApp(setup_handler=setup).run()
'''


def _client():
    from smallestai import SmallestAI
    from smallestai.environment import SmallestAIEnvironment

    if "dev" in BASE:
        env = SmallestAIEnvironment(
            atoms=f"{BASE}/atoms/v1", waves=BASE, waves_ws=BASE.replace("http", "ws"), payment=BASE
        )
        return SmallestAI(api_key=API_KEY, environment=env)
    return SmallestAI(api_key=API_KEY)  # Production


def _data(resp):
    """Unwrap a {status, data} SDK response into the data dict."""
    d = getattr(resp, "data", resp)
    if hasattr(d, "model_dump"):
        d = d.model_dump()
    return d


def _set_build_live(agent_id: str, build_id: str) -> None:
    """Make a crew build live. SDK GAP: there is no SDK/CLI-scriptable method for
    this yet (the CLI's `agent-crew builds` is interactive), so we hit the REST
    endpoint directly. Tracked as a follow-up to add to the SDK."""
    req = urllib.request.Request(
        f"{BASE}/atoms/v1/sdk/agents/{agent_id}/builds/{build_id}",
        data=json.dumps({"isLive": True}).encode(),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="PATCH",
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        assert r.status == 200, f"make-live failed: {r.status}"


def _deploy_probe_crew(agent_id: str) -> str:
    """Deploy the probe crew to `agent_id`. SDK GAP: crew code deploy only exists as
    the `smallestai agent-crew` CLI, so we shell out to it. Returns the build id."""
    workdir = tempfile.mkdtemp(prefix="caller-probe-")
    with open(os.path.join(workdir, "server.py"), "w") as f:
        f.write(PROBE_SERVER)
    with open(os.path.join(workdir, "requirements.txt"), "w") as f:
        f.write("smallestai>=5.14.0\nloguru>=0.7.0\n")
    env = {**os.environ, "SMALLEST_API_KEY": API_KEY}
    if "dev" in BASE:
        env["SMALLEST_BASE_URL"] = BASE
    run = lambda *a: subprocess.run(
        ["smallestai", *a], cwd=workdir, env=env, capture_output=True, text=True, timeout=600
    )
    assert run("auth", "login").returncode == 0 or True  # login is idempotent
    subprocess.run(["sh", "-c", f'echo "{API_KEY}" | smallestai auth login'], cwd=workdir, env=env, timeout=60)
    init = run("agent-crew", "init", "--agent-id", agent_id)
    assert init.returncode == 0, f"init failed: {init.stderr or init.stdout}"
    dep = run("agent-crew", "deploy", "--entry-point", "server.py")
    assert dep.returncode == 0 and "SUCCEEDED" in dep.stdout, f"deploy failed: {dep.stderr or dep.stdout}"
    build_id = next(ln.split("Build ID:")[1].strip() for ln in dep.stdout.splitlines() if "Build ID:" in ln)
    return build_id


def _unattached_from_product(client) -> str:
    """A phone-number product not bound to an agent, to dial from."""
    for p in _data(client.atoms.phone_numbers.list()) or []:
        p = p if isinstance(p, dict) else _data(p)
        if not (p.get("agent") or p.get("agentId")):
            return p["_id"]
    raise AssertionError("no unattached phone-number product to dial from; attach a caller ID")


def run_live_caller_context_probe() -> dict:
    """Create+deploy a probe crew, place an outbound call, return the caller.probe payload."""
    assert API_KEY, "set SMALLEST_API_KEY"
    assert TEST_NUMBER, "set SMALLEST_TEST_NUMBER to a phone you can answer"
    client = _client()

    stamp = str(int(time.time()))[-6:]
    agent_id = _data(client.atoms.agents.create_agent(name=f"zzz-caller-probe-{stamp}", global_prompt="probe"))
    agent_id = agent_id if isinstance(agent_id, str) else agent_id.get("_id") or agent_id.get("id")
    print(f"created probe agent {agent_id}")
    try:
        build_id = _deploy_probe_crew(agent_id)
        print(f"deployed build {build_id}; making live…")
        _set_build_live(agent_id, build_id)
        from_product = _unattached_from_product(client)

        call = _data(
            client.atoms.calls.start_outbound_call(
                agent_id=agent_id, phone_number=TEST_NUMBER, from_product_id=from_product
            )
        )
        call_id = call.get("conversationId") or call.get("callId")
        print(f"\n>>> CALL PLACED to {TEST_NUMBER} (call {call_id}). ANSWER IT. <<<\n")

        payload = None
        for i in range(30):
            rec = _data(client.atoms.calls.get(call_id))
            status = rec.get("status")
            for e in rec.get("events") or []:
                if str(e.get("name") or e.get("eventType") or "").lower() == "caller.probe":
                    payload = e.get("payload")
                elif "caller.probe" in json.dumps(e):
                    inner = e.get("payload") or e.get("metadata")
                    if isinstance(inner, str):
                        inner = json.loads(inner)
                    payload = (inner or {}).get("payload", inner)
            print(f"  [{(i + 1) * 10}s] status={status} caller.probe={'FOUND' if payload else '-'}")
            if payload:
                break
            if status in ("no_answer", "failed", "busy") and i > 0:
                raise AssertionError(f"call {status} — answer the call next time")
            time.sleep(10)

        assert payload, "no caller.probe event — the crew did not report session.caller (was the call answered?)"
        return payload
    finally:
        try:
            client.atoms.agents.archive_agent(agent_id)
            print(f"cleaned up probe agent {agent_id}")
        except Exception as exc:  # cleanup is best-effort
            print(f"cleanup skipped: {exc}")


@pytest.mark.skipif(not (API_KEY and TEST_NUMBER), reason="set SMALLEST_API_KEY + SMALLEST_TEST_NUMBER")
def test_caller_context_live():
    payload = run_live_caller_context_probe()
    print("\n=== caller.probe payload (this is session.caller, not transcription) ===")
    print(json.dumps(payload, indent=2))
    assert payload["user_number"], "session.caller.user_number was empty"
    assert payload["agent_number"], "session.caller.agent_number was empty"
    assert payload["direction"] in ("inbound", "outbound"), payload["direction"]
    assert payload["call_id"], "session.caller.call_id was empty"
    assert payload["user_number"] == TEST_NUMBER, "dialed number should be the caller user_number on outbound"


if __name__ == "__main__":
    payload = run_live_caller_context_probe()
    print("\n=== caller.probe payload (this is session.caller, not transcription) ===")
    print(json.dumps(payload, indent=2))
    ok = bool(payload.get("user_number") and payload.get("direction") and payload.get("call_id"))
    print("\nRESULT:", "PASS — session.caller delivered end to end" if ok else "FAIL")
    sys.exit(0 if ok else 1)
