"""Unit tests for the hand-written SDK fixes (no network). Run by CI's test job."""
import os
import warnings
from types import SimpleNamespace as NS

import pytest


def test_openai_client_raises_without_key():
    os.environ.pop("OPENAI_API_KEY", None)
    from smallestai.atoms.crew.clients.openai import OpenAIClient
    with pytest.raises(ValueError):
        OpenAIClient(api_key=None)  # #1: must raise, not silently warn


def test_openai_client_ok_with_key():
    from smallestai.atoms.crew.clients.openai import OpenAIClient
    assert OpenAIClient(api_key="sk_test") is not None


def test_openai_electron_factory():
    from smallestai.atoms.crew.clients.openai import OpenAIClient
    os.environ["SMALLEST_API_KEY"] = "sk_dummy"
    assert OpenAIClient.electron() is not None  # #12


def test_call_analytics_rename_and_alias():
    from smallestai.atoms.helpers import CallAnalytics, Call
    assert CallAnalytics(api_key="x") is not None
    assert issubclass(Call, CallAnalytics)
    with pytest.warns(DeprecationWarning):  # #15
        Call(api_key="x")


def test_helpers_import_clean():
    import smallestai.atoms.helpers  # noqa: F401  (#17 — requests dep present)


def test_as_page_normalizes_shapes():
    from smallestai.atoms.helpers import as_page  # #25
    assert as_page(NS(data=NS(agents=[1, 2], total_count=2, has_more=False))).items == [1, 2]
    p = as_page(NS(data=NS(logs=[1], pagination=NS(total=1, has_more=True))))
    assert p.items == [1] and p.total_count == 1 and p.has_more is True
    assert as_page(NS(data=[3, 4])).items == [3, 4]
    assert as_page({"data": {"records": [9], "total_count": 1}}).items == [9]


def test_require_id_guard():
    from smallestai.atoms.helpers import require_id  # #18
    for bad in ["", "   ", None]:
        with pytest.raises(ValueError):
            require_id(bad)
    assert require_id("abc") == "abc"
