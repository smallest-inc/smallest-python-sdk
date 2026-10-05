"""Deterministic routing logic for DeterministicRouter (PRO-3271).

Covers the transition engine (the deterministic part) without the LLM turn: default
edges, data-dependent predicates, skip, terminal, and graph validation.
"""

import pytest

from smallestai.atoms.crew import DeterministicRouter, SubAgent


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
