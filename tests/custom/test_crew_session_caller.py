"""Public accessors for the connect handshake's caller context (PRO-3560).

A crew reads who is on the call via ``session.caller`` / ``session.session_context``
/ ``session.initial_variables`` — the ergonomic surface Balto needs for an ANI
lookup, instead of reaching into the private ``_init_event``.
"""

import asyncio
from unittest.mock import MagicMock

import pytest

from smallestai.atoms.crew import CallerContext, SessionContext
from smallestai.atoms.crew.events import SDKSystemInitEvent
from smallestai.atoms.crew.session import CrewSession


@pytest.fixture(autouse=True)
def _ensure_event_loop():
    # CrewSession.__init__ (and the nodes it builds) bind to the current loop;
    # guarantee one for these sync construction tests on py3.9 (asyncio_mode=auto).
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    yield


async def _noop_setup(_session: CrewSession) -> None:
    pass


def _session() -> CrewSession:
    return CrewSession(websocket=MagicMock(), session_id="test-session", setup_handler=_noop_setup)


def _init(**ctx) -> SDKSystemInitEvent:
    return SDKSystemInitEvent(version="1.0", session_context=SessionContext(**ctx))


def test_accessors_are_empty_before_the_handshake():
    s = _session()
    assert s.session_context is None
    assert s.caller is None
    assert s.initial_variables == {}


def test_caller_and_variables_surface_from_the_init_event():
    s = _session()
    s._init_event = _init(
        conversation_type="telephonyInbound",
        initial_variables={"account_id": "42"},
        caller=CallerContext(
            user_number="+14155550000",
            agent_number="+18005550000",
            direction="inbound",
            call_id="c-1",
        ),
    )
    assert s.caller is not None
    assert s.caller.user_number == "+14155550000"  # the ANI
    assert s.caller.agent_number == "+18005550000"  # the number dialed
    assert s.caller.direction == "inbound"
    assert s.caller.call_id == "c-1"
    assert s.initial_variables == {"account_id": "42"}
    assert s.session_context is not None


def test_a_webcall_has_a_context_but_no_caller():
    s = _session()
    s._init_event = _init(conversation_type="webcall", initial_variables={}, caller=None)
    assert s.session_context is not None  # context present
    assert s.caller is None  # but no caller identity to look up
    assert s.initial_variables == {}
