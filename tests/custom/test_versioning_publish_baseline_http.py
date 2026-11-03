"""Exercise publish baseline handling through the generated client and in-memory HTTP."""

import httpx
import pytest

from smallestai import SmallestAI
from smallestai.atoms.helpers.versioning import SecurityCheckFailedError, Versioning
from smallestai.core.api_error import ApiError


# --- Synthetic transport helpers ---
def _versioning_transport(*, fail_baseline=False, first_publish=False, scan_fails=False):
    calls = []
    listings = 0

    def respond(request):
        nonlocal listings
        path = request.url.path
        calls.append((request.method, path))
        if request.method == "GET" and path.endswith("/revisions"):
            listings += 1
            if fail_baseline and listings == 1:
                return httpx.Response(503, json={"error": "temporary lookup failure"})
            if first_publish:
                revision_id = None if listings == 1 else "r1"
            else:
                revision_id = "r1" if listings <= 2 else "r2"
            revisions = [{"_id": revision_id}] if revision_id else []
            return httpx.Response(200, json={"status": True, "data": {"revisions": revisions}})
        if request.method == "POST" and path.endswith("/draft/publish"):
            return httpx.Response(202, json={"status": True, "data": {"state": "scanning"}})
        if request.method == "GET" and "/revisions/" in path:
            revision_id = path.rsplit("/", 1)[-1]
            revision = {"_id": revision_id, "status": "published"}
            if scan_fails and revision_id == "r2":
                revision = {"_id": revision_id, "status": "scanning", "securityCheck": {"status": "failed"}}
            return httpx.Response(
                200,
                json={"status": True, "data": {"revision": revision}},
            )
        raise AssertionError(f"Unexpected synthetic request: {request.method} {path}")

    return httpx.MockTransport(respond), calls


def _versioning(transport):
    http_client = httpx.Client(transport=transport)
    return Versioning(SmallestAI(api_key="synthetic", httpx_client=http_client, max_retries=0)), http_client


# --- Native HTTP regression and nearby publish invariants ---
def test_failed_baseline_lookup_prevents_ambiguous_publish():
    transport, calls = _versioning_transport(fail_baseline=True)
    versioning, http_client = _versioning(transport)
    try:
        with pytest.raises(ApiError) as error:
            versioning.publish_and_wait("agent", "branch", poll_interval=0)
        assert error.value.status_code == 503
        assert not any(method == "POST" for method, _ in calls)
    finally:
        http_client.close()


@pytest.mark.parametrize("first_publish,expected", [(False, "r2"), (True, "r1")])
def test_successful_baseline_waits_for_its_publish(first_publish, expected):
    transport, calls = _versioning_transport(first_publish=first_publish)
    versioning, http_client = _versioning(transport)
    try:
        revision = versioning.publish_and_wait("agent", "branch", poll_interval=0)
        assert revision.id == expected
        assert sum(method == "POST" for method, _ in calls) == 1
    finally:
        http_client.close()


def test_new_revision_scan_failure_is_not_success():
    transport, calls = _versioning_transport(scan_fails=True)
    versioning, http_client = _versioning(transport)
    try:
        with pytest.raises(SecurityCheckFailedError):
            versioning.publish_and_wait("agent", "branch", poll_interval=0)
        assert sum(method == "POST" for method, _ in calls) == 1
    finally:
        http_client.close()
