"""Deterministic multi-agent routing for crew (PRO-3271).

A first-class primitive for Balto-style workflows: define N sub-agents and
**code-defined, data-dependent transitions** between them (with explicit skip and
in-session agent-to-agent handoff), instead of hand-rolling a state machine inside
one ``OutputCrewNode``. Transitions are computed deterministically in Python off
tool results / accumulated state — *not* by an LLM classifier — so the routing is
reproducible and auditable.

It runs on the existing crew runtime (it is an ``OutputCrewNode``): the platform
drives STT/TTS/telephony and asks for an LLM turn; this node picks the active
sub-agent, runs that specialist's prompt + tool subset, then advances the active
sub-agent deterministically for the next turn.

Example::

    from smallestai.atoms.crew import DeterministicRouter, SubAgent, function_tool
    from smallestai.atoms.crew.clients import OpenAIClient

    class Collections(DeterministicRouter):
        def __init__(self):
            super().__init__(name="collections", llm=OpenAIClient(model="gpt-4o"), start="intake")
            self.add_sub_agent(SubAgent("intake", "Greet and collect the account id.", tools=[self.lookup]))
            self.add_sub_agent(SubAgent("verify", "Verify identity (DOB last 4)."))
            self.add_sub_agent(SubAgent("resolve", "Discuss the balance and a payment plan."))
            # data-dependent transitions, evaluated in order; a None predicate is the default.
            self.add_transition("intake", "resolve", when=lambda s: s.get("prior_verified"))  # skip verify
            self.add_transition("intake", "verify")                                           # default
            self.add_transition("verify", "resolve")

        @function_tool
        async def lookup(self, account_id: str, prior_verified: bool):
            self.set_state(account_id=account_id, prior_verified=prior_verified)
            return {"ok": True}
"""

import dataclasses
import typing

from loguru import logger

from smallestai.atoms.crew.events import SDKAgentLogEvent
from smallestai.atoms.crew.nodes.output_crew import OutputCrewNode
from smallestai.atoms.crew.tools.registry import ToolRegistry


@dataclasses.dataclass
class SubAgent:
    """One specialist in a :class:`DeterministicRouter`.

    Args:
        id: unique id, referenced by transitions.
        prompt: the system prompt used while this sub-agent is active.
        tools: ``@function_tool`` callables available only while this sub-agent is active.
    """

    id: str
    prompt: str
    tools: typing.List[typing.Callable] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Transition:
    source: str
    target: str
    when: typing.Optional[typing.Callable[[typing.Dict[str, typing.Any]], bool]] = None


class DeterministicRouter(OutputCrewNode):
    """Deterministic multi-agent: sub-agents + code-defined data-dependent transitions.

    The active sub-agent owns the turn (its prompt + tools). After each turn the
    router evaluates the transitions out of the active sub-agent, in registration
    order, and moves to the first whose predicate passes (a transition with no
    predicate is the unconditional default, tried last). A transition can target any
    sub-agent, so skipping a step is just a transition that jumps past it. Each move
    emits an ``SDKAgentLogEvent`` for the call's Events tab.
    """

    def __init__(self, name: str, llm: typing.Any, start: str):
        super().__init__(name=name)
        self.llm = llm
        self.start = start
        self.state: typing.Dict[str, typing.Any] = {}
        self._sub_agents: typing.Dict[str, SubAgent] = {}
        self._registries: typing.Dict[str, ToolRegistry] = {}
        self._transitions: typing.List[Transition] = []
        self._active: str = start
        self._entered = False

    # -- declaration -------------------------------------------------------------

    def add_sub_agent(self, sub: SubAgent) -> "DeterministicRouter":
        """Register a sub-agent and its (active-only) tool subset."""
        if sub.id in self._sub_agents:
            raise ValueError(f"duplicate sub-agent id: {sub.id!r}")
        self._sub_agents[sub.id] = sub
        registry = ToolRegistry()
        for tool in sub.tools:
            registry.register(tool)
        self._registries[sub.id] = registry
        return self

    def add_transition(
        self,
        source: str,
        target: str,
        when: typing.Optional[typing.Callable[[typing.Dict[str, typing.Any]], bool]] = None,
    ) -> "DeterministicRouter":
        """Add a transition ``source -> target``. ``when`` is a predicate on the
        router state; omit it for the unconditional default out of ``source``."""
        self._transitions.append(Transition(source, target, when))
        return self

    def set_state(self, **kwargs: typing.Any) -> None:
        """Merge values into the router state that transition predicates read.

        Call this from your ``@function_tool``s off real tool results; the routing
        is then a deterministic function of that state.
        """
        self.state.update(kwargs)

    def validate(self) -> None:
        """Fail fast on an obviously-broken graph (unknown start/targets)."""
        if self.start not in self._sub_agents:
            raise ValueError(f"start sub-agent {self.start!r} is not registered")
        for t in self._transitions:
            for role, sid in (("source", t.source), ("target", t.target)):
                if sid not in self._sub_agents:
                    raise ValueError(f"transition {role} {sid!r} is not a registered sub-agent")

    # -- routing -----------------------------------------------------------------

    def _next_active(self) -> typing.Optional[str]:
        """The next sub-agent id, deterministically: the first conditional transition
        out of the active node whose predicate passes, else the default, else None
        (terminal — stay put)."""
        out = [t for t in self._transitions if t.source == self._active]
        for t in out:
            if t.when is None:
                continue
            try:
                if t.when(self.state):
                    return t.target
            except Exception:
                logger.exception(f"[{self.name}] transition predicate {self._active}->{t.target} raised")
        default = next((t for t in out if t.when is None), None)
        return default.target if default else None

    async def _enter(self, sub_id: str, *, previous: typing.Optional[str]) -> None:
        """Make ``sub_id`` active and log the move to the Events tab.

        Mid-call voice/language swap is intentionally not attempted here: the platform
        ignores crew-sent output-agent settings (a crew owns only the LLM turn), so a
        runtime voice swap is a platform gap tracked separately — not an SDK no-op.
        """
        self._active = sub_id
        await self.send_event(
            SDKAgentLogEvent(
                name="agent.transition",
                payload={"from": previous, "to": sub_id, "state": dict(self.state)},
            )
        )

    async def generate_response(self) -> typing.AsyncIterator[str]:
        self.validate()
        if not self._entered:
            self._entered = True
            await self._enter(self._active, previous=None)

        sub = self._sub_agents[self._active]
        registry = self._registries[self._active]

        # Swap in the active sub-agent's system prompt, keep the conversation.
        conversation = [m for m in self.context.messages if m.get("role") != "system"]
        self.context.set_messages([{"role": "system", "content": sub.prompt}] + conversation)

        # One LLM turn with this sub-agent's tools. Tools run first (they update
        # state via set_state), then we stream the spoken reply.
        resp = await self.llm.chat(self.context.messages, tools=registry.get_schemas())
        tool_calls = getattr(resp, "tool_calls", None)
        if tool_calls:
            for result in await registry.execute(tool_calls, context=self):
                self.context.add_message(result.to_message())
            async for chunk in self.llm.chat(self.context.messages, stream=True):
                if getattr(chunk, "content", None):
                    yield chunk.content
        else:
            yield getattr(resp, "content", None) or ""

        # Advance deterministically AFTER the turn, off the state tools just set.
        nxt = self._next_active()
        if nxt and nxt != self._active:
            await self._enter(nxt, previous=self._active)
