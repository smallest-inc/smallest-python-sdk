"""Every helper HTTP call has to carry a timeout.

`requests` has no default timeout, so a call that got none waits forever on a
half-open connection. AgentTools already threaded a `request_timeout` through every
call; Audience, CallAnalytics, Campaign and KB did not, so 28 call sites could hang.

Logic-only: `requests` is replaced with a recorder, so nothing leaves the process.
"""

import inspect
from unittest.mock import patch

import pytest

from smallestai.atoms.helpers import audience as audience_module
from smallestai.atoms.helpers import call as call_module
from smallestai.atoms.helpers import campaign as campaign_module
from smallestai.atoms.helpers import kb as kb_module
from smallestai.atoms.helpers.agent_tools import AgentTools
from smallestai.atoms.helpers.audience import Audience
from smallestai.atoms.helpers.call import CallAnalytics
from smallestai.atoms.helpers.campaign import Campaign
from smallestai.atoms.helpers.kb import KB

MANAGERS = [
    pytest.param(Audience, audience_module, id="Audience"),
    pytest.param(CallAnalytics, call_module, id="CallAnalytics"),
    pytest.param(Campaign, campaign_module, id="Campaign"),
    pytest.param(KB, kb_module, id="KB"),
]


class _Recorder:
    """Stands in for the `requests` module and keeps every call's kwargs."""

    def __init__(self):
        self.calls = []

    def _verb(self, name):
        def go(*args, **kwargs):
            self.calls.append((name, kwargs))
            return _Response()

        return go

    def __getattr__(self, name):
        if name in ("get", "post", "put", "patch", "delete"):
            return self._verb(name)
        raise AttributeError(name)


class _Response:
    status_code = 200
    text = "{}"

    def raise_for_status(self):
        return None

    def json(self):
        return {}


def _public_methods(manager):
    return [
        (name, member) for name, member in inspect.getmembers(manager, inspect.isfunction) if not name.startswith("_")
    ]


def _sample_args(signature):
    """A placeholder for each required argument, so the method reaches its request."""
    return ["x" for name, p in list(signature.parameters.items())[1:] if p.default is inspect.Parameter.empty]


@pytest.mark.parametrize("manager, module", MANAGERS)
def test_every_request_carries_a_timeout(manager, module):
    recorder = _Recorder()
    instance = manager(api_key="k")

    with patch.object(module, "requests", recorder):
        for name, method in _public_methods(manager):
            try:
                method(instance, *_sample_args(inspect.signature(method)))
            except Exception:  # a method may reject the placeholder; the call is what matters
                pass

    assert recorder.calls, f"{manager.__name__} made no request to inspect"
    missing = [name for name, kwargs in recorder.calls if kwargs.get("timeout") is None]
    assert missing == [], f"{manager.__name__} sent no timeout on: {missing}"


@pytest.mark.parametrize("manager, module", MANAGERS)
def test_the_caller_can_choose_the_timeout(manager, module):
    recorder = _Recorder()
    instance = manager(api_key="k", request_timeout=1.5)

    with patch.object(module, "requests", recorder):
        for name, method in _public_methods(manager):
            try:
                method(instance, *_sample_args(inspect.signature(method)))
            except Exception:
                pass

    assert {kwargs["timeout"] for _, kwargs in recorder.calls} == {1.5}


@pytest.mark.parametrize("manager, module", MANAGERS)
def test_the_default_matches_the_helper_that_already_had_one(manager, module):
    assert module.DEFAULT_REQUEST_TIMEOUT == inspect.signature(AgentTools).parameters["request_timeout"].default
