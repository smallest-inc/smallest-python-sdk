"""Deterministic routing logic for DeterministicRouter (PRO-3271).

Covers the transition engine (the deterministic part) without the LLM turn: default
edges, data-dependent predicates, skip, terminal, and graph validation.
"""

import asyncio

import pytest

from smallestai.atoms.crew import DeterministicRouter, SubAgent


@pytest.fixture(autouse=True)
def _ensure_event_loop():
    """Guarantee a current event loop for the sync construction tests.

    A ``DeterministicRouter`` (via ``CrewNode.__init__``) builds an ``asyncio.Queue``,
    which binds to the current loop on py3.9. These sync tests construct the router off
    any running loop, so with ``asyncio_mode=auto`` a prior test may leave no current
    loop and construction raises ``RuntimeError: no current event loop``. In production
    nodes are always built under the crew's running loop, so this is a test-only concern.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield


def _collections() -> DeterministicRouter:
    r = DeterministicRouter(name="collections", llm=object(), start="intake")
    r.add_sub_agent(SubAgent("intake", "collect account id"))
    r.add_sub_agent(SubAgent("verify", "verify identity"))
    r.add_sub_agent(SubAgent("resolve", "discuss balance"))
    r.add_transition("intake", "resolve", when=lambda s: s.get("prior_verified"))  # skip verify
    r.add_transition("intake", "verify")  # default
    r.add_transition("verify", "resolve")
    r.validate()
    return r


def test_default_transition_when_no_predicate_matches():
    r = _collections()
    assert r._active == "intake"
    assert r._next_active() == "verify"  # default out of intake


def test_data_dependent_skip():
    r = _collections()
    r.set_state(prior_verified=True)
    assert r._next_active() == "resolve"  # predicate passes -> skips verify


def test_conditional_takes_precedence_over_default_in_order():
    r = _collections()
    r.set_state(prior_verified=False)
    assert r._next_active() == "verify"  # predicate false -> falls through to default


def test_terminal_sub_agent_stays_put():
    r = _collections()
    r._active = "resolve"
    assert r._next_active() is None  # no outgoing edges


def test_predicate_exception_is_swallowed_and_falls_through():
    r = DeterministicRouter(name="x", llm=object(), start="a")
    r.add_sub_agent(SubAgent("a", "p"))
    r.add_sub_agent(SubAgent("b", "p"))

    def boom(_state):
        raise RuntimeError("bad predicate")

    r.add_transition("a", "b", when=boom)
    r.add_transition("a", "b")  # default still routes
    assert r._next_active() == "b"


def test_duplicate_sub_agent_id_rejected():
    r = DeterministicRouter(name="x", llm=object(), start="a")
    r.add_sub_agent(SubAgent("a", "p"))
    with pytest.raises(ValueError, match="duplicate"):
        r.add_sub_agent(SubAgent("a", "p2"))


def test_validate_rejects_unknown_start_and_targets():
    with pytest.raises(ValueError, match="start"):
        DeterministicRouter(name="x", llm=object(), start="missing").add_sub_agent(SubAgent("a", "p")).validate()

    bad = DeterministicRouter(name="x", llm=object(), start="a")
    bad.add_sub_agent(SubAgent("a", "p"))
    bad.add_transition("a", "ghost")
    with pytest.raises(ValueError, match="target"):
        bad.validate()


def test_per_sub_agent_tools_are_isolated():
    from smallestai.atoms.crew import function_tool

    @function_tool
    async def only_intake(x: str):
        """intake tool.

        Args:
            x: a value
        """
        return x

    r = DeterministicRouter(name="x", llm=object(), start="a")
    r.add_sub_agent(SubAgent("a", "p", tools=[only_intake]))
    r.add_sub_agent(SubAgent("b", "p"))
    # a has its tool; b has none
    assert len(r._registries["a"].get_schemas()) == 1
    assert r._registries["b"].get_schemas() == []


@pytest.mark.asyncio
async def test_tool_less_sub_agent_streams_directly():
    """A sub-agent with no tools must stream straight to TTS (no non-streaming
    detection turn first), so the voice path gets incremental first tokens."""
    from smallestai.atoms.crew import function_tool
    from smallestai.atoms.crew.clients.types import ChatChunk, ChatResponse, ToolCall

    calls = {"stream": 0, "non_stream": 0}

    class _FakeLLM:
        async def chat(self, messages, stream=False, tools=None, **kw):
            if stream:
                calls["stream"] += 1

                async def _gen():
                    yield ChatChunk(content="hel")
                    yield ChatChunk(content="lo.")

                return _gen()
            calls["non_stream"] += 1
            return ChatResponse(content="should-not-be-used")

    r = DeterministicRouter(name="flow", llm=_FakeLLM(), start="a")
    r.add_sub_agent(SubAgent("a", "greeter"))  # no tools
    r.context.add_message({"role": "user", "content": "hi"})

    reply = "".join([chunk async for chunk in r.generate_response()])
    assert reply == "hello."
    assert calls["stream"] == 1  # streamed directly
    assert calls["non_stream"] == 0  # no detection turn for a tool-less sub-agent


@pytest.mark.asyncio
async def test_generate_response_tool_loop_and_transition():
    """The per-turn loop (caught two live bugs): the stream chat is awaited, and the
    tool-result message is preceded by the assistant-with-tool_calls turn (else the
    provider 400s). After the tool sets state, the router transitions."""
    from smallestai.atoms.crew import function_tool
    from smallestai.atoms.crew.clients.types import ChatChunk, ChatResponse, ToolCall

    class _FakeLLM:
        async def chat(self, messages, stream=False, tools=None, **kw):
            if stream:  # must be awaited by the node, then async-iterated

                async def _gen():
                    yield ChatChunk(content="all set.")

                return _gen()
            if any(m.get("role") == "tool" for m in messages):
                return ChatResponse(content="all set.")
            return ChatResponse(content=None, tool_calls=[ToolCall(id="call_1", name="mark", arguments="{}")])

    class Flow(DeterministicRouter):
        def __init__(self):
            super().__init__(name="flow", llm=_FakeLLM(), start="a")
            self.add_sub_agent(SubAgent("a", "intake", tools=[self.mark]))
            self.add_sub_agent(SubAgent("b", "resolve"))
            self.add_transition("a", "b", when=lambda s: s.get("done"))

        @function_tool
        async def mark(self):
            """mark done."""
            self.set_state(done=True)
            return {"ok": True}

    r = Flow()
    r.context.add_message({"role": "user", "content": "hi"})
    reply = "".join([chunk async for chunk in r.generate_response()])

    assert reply == "all set."
    roles = [m["role"] for m in r.context.messages]
    # assistant(tool_calls) must come before the tool result
    assert "assistant" in roles and "tool" in roles
    assert roles.index("assistant") < roles.index("tool")
    assert any(m["role"] == "assistant" and m.get("tool_calls") for m in r.context.messages)
    assert r.state.get("done") is True
    assert r._active == "b"  # transitioned after the tool set state
