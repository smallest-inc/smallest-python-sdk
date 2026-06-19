"""Unit tests for the hand-written REST helpers (KB, Audience, Campaign) + Page.

No network: we monkeypatch the `requests` module each helper imports and assert it
builds the right URL with bearer auth. Guards the helpers the verify harness flagged
as untested.
"""
import smallestai.atoms.helpers.audience as audience_mod
import smallestai.atoms.helpers.campaign as campaign_mod
import smallestai.atoms.helpers.kb as kb_mod
from smallestai.atoms.helpers import KB, Audience, Campaign, Page


class _FakeResp:
    def __init__(self):
        self.calls = []

    def raise_for_status(self):
        return None

    def json(self):
        return {"status": True, "data": []}


class _FakeRequests:
    """Records (method, url, headers) and returns a canned response."""

    def __init__(self):
        self.last = None
        self._resp = _FakeResp()

    def _record(self, method):
        def fn(url, headers=None, **kw):
            self.last = (method, url, headers or {})
            return self._resp
        return fn

    def __getattr__(self, name):
        if name in ("get", "post", "put", "patch", "delete"):
            return self._record(name)
        raise AttributeError(name)


def _patch(monkeypatch, module):
    fake = _FakeRequests()
    monkeypatch.setattr(module, "requests", fake)
    return fake


def test_page_defaults():
    p = Page()
    assert p.items == [] and p.total_count is None and p.has_more is None
    p2 = Page(items=[1, 2], total_count=2)
    assert p2.items == [1, 2] and p2.total_count == 2


def test_kb_list_builds_url_with_auth(monkeypatch):
    fake = _patch(monkeypatch, kb_mod)
    KB(base_url="https://api.example/atoms/v1", api_key="sk_test").list()
    method, url, headers = fake.last
    assert method == "get" and url.startswith("https://api.example/atoms/v1")
    assert headers.get("Authorization") == "Bearer sk_test"


def test_audience_list_builds_url_with_auth(monkeypatch):
    fake = _patch(monkeypatch, audience_mod)
    Audience(base_url="https://api.example/atoms/v1", api_key="sk_test").list()
    method, url, headers = fake.last
    assert method == "get" and url.startswith("https://api.example/atoms/v1")
    assert headers.get("Authorization") == "Bearer sk_test"


def test_campaign_list_builds_url_with_auth(monkeypatch):
    fake = _patch(monkeypatch, campaign_mod)
    Campaign(base_url="https://api.example/atoms/v1", api_key="sk_test").list()
    method, url, headers = fake.last
    assert method == "get" and url.startswith("https://api.example/atoms/v1")
    assert headers.get("Authorization") == "Bearer sk_test"
