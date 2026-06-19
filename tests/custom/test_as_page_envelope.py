"""Regression tests for the as_page() pagination helper.

Guards the per-resource container-key handling. A missing key makes as_page
silently return the whole envelope as a single bogus item instead of the rows
(found in pre-merge review: `retries`, and the dual telephony/custom arrays).
"""
from smallestai.atoms.helpers import as_page


class _Resp:
    """Minimal stand-in for an SDK response with a `.data` payload."""

    def __init__(self, data):
        self.data = data


def test_bare_list_data() -> None:
    assert as_page(_Resp([1, 2, 3])).items == [1, 2, 3]


def test_agents_key() -> None:
    pg = as_page(_Resp({"agents": [{"a": 1}, {"a": 2}], "total_count": 2}))
    assert len(pg.items) == 2 and pg.total_count == 2


def test_retries_key() -> None:
    # conversations.list_retry_attempts — was unhandled, returned a 1-item envelope.
    pg = as_page(_Resp({"retries": [{"id": 1}, {"id": 2}, {"id": 3}]}))
    assert len(pg.items) == 3


def test_telephony_and_custom_products_concatenate() -> None:
    # phone_numbers.list_all_phone_numbers_platform_sip — two arrays, no single key.
    pg = as_page(_Resp({"telephony_products": [1, 2], "custom_products": [3]}))
    assert len(pg.items) == 3


def test_only_telephony_products() -> None:
    pg = as_page(_Resp({"telephony_products": [1, 2]}))
    assert len(pg.items) == 2


def test_campaigns_total_campaign_count() -> None:
    pg = as_page(_Resp({"campaigns": [{"c": 1}], "total_campaign_count": 42}))
    assert len(pg.items) == 1 and pg.total_count == 42


def test_nested_pagination() -> None:
    pg = as_page(_Resp({"logs": [1, 2], "pagination": {"total": 9, "hasMore": True}}))
    assert pg.items == [1, 2] and pg.total_count == 9
