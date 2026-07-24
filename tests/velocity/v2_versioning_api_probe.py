#!/usr/bin/env python3
"""Verbose live probe of the Agent Versioning v2 (branch/revision) REST API.

Runs the full lifecycle against the LIVE API using plain `requests` (no SDK), on
a throwaway forked branch that it archives afterward, and prints the real
response detail at each step so you can eyeball the actual shapes.

Only dependency: requests.

    pip install requests
    export SMALLEST_API_KEY=sk_...                                  # required
    export SMALLEST_BASE_URL=https://api.smallest.ai/atoms/v1       # prod (default)
    #   or https://api.dev.smallest.ai/atoms/v1 for dev
    export E2E_AGENT_ID=<agent id>          # optional; omit to auto-create a throwaway agent
    python tests/velocity/v2_versioning_api_probe.py
"""
import json
import os
import sys
import time

import requests

BASE = os.environ.get("SMALLEST_BASE_URL", "https://api.smallest.ai/atoms/v1").rstrip("/")
KEY = os.environ.get("SMALLEST_API_KEY")
AGENT = os.environ.get("E2E_AGENT_ID")
if not KEY:
    print("SMALLEST_API_KEY is required")
    sys.exit(2)
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

_ok = 0
_fail = 0
_failed = []


def call(method, path, **kw):
    r = requests.request(method, f"{BASE}{path}", headers=H, timeout=45, **kw)
    try:
        body = r.json()
    except Exception:
        body = {"_raw": r.text[:400]}
    return r.status_code, body, dict(r.headers)


def check(cond, label, detail=""):
    global _ok, _fail
    print(("  PASS " if cond else "  FAIL ") + label + (f"  {detail}" if detail else ""))
    if cond:
        _ok += 1
    else:
        _fail += 1
        _failed.append(label)


def show(title, obj, keys=None):
    if isinstance(obj, dict) and keys:
        obj = {k: obj.get(k) for k in keys}
    print(f"    {title}: {json.dumps(obj, default=str)[:600]}")


def main():
    print(f"\n=== Agent Versioning v2 API probe @ {BASE} ===")
    created = False
    agent_id = AGENT

    # 0. Create a throwaway agent if none was given.
    if not agent_id:
        sc, b, _ = call("POST", "/agent", json={
            "name": "v2-api-probe",
            "globalPrompt": "You are a probe agent.",
            "firstMessage": "Hi, probe here.",
            "language": {"switching": {"isEnabled": False}},
        })
        agent_id = b.get("data")
        created = True
        check(sc in (200, 201) and agent_id, "POST /agent (create throwaway)", f"http={sc} id={agent_id}")

    # 1. List branches -> find Main.
    sc, b, _ = call("GET", f"/agent/{agent_id}/branches")
    branches = b.get("data", {}).get("branches", [])
    main = next((x for x in branches if x.get("branch", {}).get("isDefault")), branches[0] if branches else None)
    check(sc == 200 and main, "GET /branches", f"http={sc} count={len(branches)}")
    show("Main BranchSummary", main, ["isLive", "hasOpenDraft", "revisionsCount", "headRevisionNumber"])
    show("Main .branch", main.get("branch", {}), ["_id", "name", "isDefault", "status", "headRevisionId"])
    main_id = main["branch"]["_id"]

    # 2. Fork a throwaway branch off Main.
    sc, b, _ = call("POST", f"/agent/{agent_id}/branches", json={"sourceBranchId": main_id, "name": f"probe-{os.getpid()}"})
    fork = b.get("data", {})
    fork_id = fork.get("_id")
    check(sc in (200, 201) and fork_id, "POST /branches (fork)", f"http={sc} fork={fork_id} status={fork.get('status')}")

    try:
        # 3. Edit the draft (camelCase config fields).
        sc, b, _ = call("PUT", f"/agent/{agent_id}/branches/{fork_id}/draft",
                        json={"globalPrompt": "Probe prompt v1.", "firstMessage": "Hello from probe."})
        check(sc == 200, "PUT /draft (globalPrompt + firstMessage)", f"http={sc}")

        # 4. Get the draft detail.
        sc, b, _ = call("GET", f"/agent/{agent_id}/branches/{fork_id}/draft")
        d = b.get("data", {})
        check(sc == 200, "GET /draft (DraftDetail)", f"http={sc} editCount={d.get('editCount')}")
        show("draft.latest", d.get("latest", {}), ["_id", "draftRevision", "status", "workflowType"])

        # 5. Publish -> poll -> published.
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/draft/publish", json={"label": "probe v1"})
        state = b.get("data", {}).get("state")
        check(sc in (200, 202), "POST /draft/publish", f"http={sc} state={state}")
        rev_id, rev = None, {}
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            sc, rl, _ = call("GET", f"/agent/{agent_id}/branches/{fork_id}/revisions", params={"limit": 1})
            revs = rl.get("data", {}).get("revisions", [])
            if revs:
                rev_id = revs[0]["_id"]
                sc, rb, _ = call("GET", f"/agent/{agent_id}/branches/{fork_id}/revisions/{rev_id}")
                rev = rb.get("data", {}).get("revision", {})
                if rev.get("status") == "published":
                    break
            time.sleep(2)
        check(rev.get("status") == "published", "publish -> revision published",
              f"rev={rev_id} status={rev.get('status')} securityCheck={(rev.get('securityCheck') or {}).get('status')}")
        show("Revision", rev, ["_id", "revisionNumber", "status", "label", "publishedByName", "promptScoreStale"])

        # 6. Test call (webcall).
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/test-call", json={"mode": "webcall"})
        check(sc == 200, "POST /test-call (webcall)", f"http={sc}")
        show("TestCallResult", b.get("data", {}), ["conversationId", "callId", "roomName", "host"])

        # 7. Second edit + publish so we have two revisions (also gives restore an older target).
        call("PUT", f"/agent/{agent_id}/branches/{fork_id}/draft", json={"globalPrompt": "Probe prompt v2."})
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/draft/publish", json={"label": "probe v2"})
        check(sc in (200, 202), "POST /draft/publish (2nd)", f"http={sc} state={b.get('data',{}).get('state')}")
        rev2_id = None
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            sc, rl, _ = call("GET", f"/agent/{agent_id}/branches/{fork_id}/revisions", params={"limit": 2})
            revs = rl.get("data", {}).get("revisions", [])
            newest = revs[0] if revs else {}
            if newest.get("_id") and newest["_id"] != rev_id and newest.get("status") == "published":
                rev2_id = newest["_id"]
                break
            time.sleep(2)
        check(rev2_id is not None, "2nd revision committed", f"rev2={rev2_id}")

        # 8. Diff the two committed revisions (a and b are 24-hex revision ids).
        sc, b, _ = call("GET", f"/agent/{agent_id}/diff", params={"a": rev_id, "b": rev2_id})
        d = b.get("data", {})
        check(sc == 200, "GET /diff (rev1 vs rev2)", f"http={sc}")
        show("diff", {"unchangedSections": d.get("unchangedSections"),
                      "diffs": [x.get("section") for x in d.get("diffs", [])]})

        # 9. Optimistic-concurrency conflict (stale expectedRevision).
        call("PUT", f"/agent/{agent_id}/branches/{fork_id}/draft", json={"globalPrompt": "edit A"})
        sc, gd, _ = call("GET", f"/agent/{agent_id}/branches/{fork_id}/draft")
        stale = gd.get("data", {}).get("latest", {}).get("draftRevision")
        call("PUT", f"/agent/{agent_id}/branches/{fork_id}/draft", json={"expectedRevision": stale, "globalPrompt": "edit B"})
        sc, b, _ = call("PUT", f"/agent/{agent_id}/branches/{fork_id}/draft", json={"expectedRevision": stale, "globalPrompt": "edit C"})
        check(sc == 409, "PUT /draft stale expectedRevision -> 409", f"http={sc}")
        show("conflict body", b)

        # 10. Restore the FIRST revision (older than head) -> new head revision.
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/revisions/{rev_id}/restore")
        check(sc == 200, "POST /revisions/{id}/restore (older revision)", f"http={sc} state={b.get('data',{}).get('state')}")

        # 11. Make the fork live, then revert Main.
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/live")
        check(sc == 200, "POST /branches/{fork}/live", f"http={sc} isLive={b.get('data',{}).get('isLive')}")
        sc, _, _ = call("POST", f"/agent/{agent_id}/branches/{main_id}/live")
        check(sc == 200, "POST /branches/{main}/live (revert)", f"http={sc}")

        # 12. v1 endpoint is deprecated under the branch model -> 409 migration.
        sc, b, hdr = call("POST", f"/agent/{agent_id}/drafts", json={})
        check(sc == 409 and b.get("error_type") == "versioning_v2_migration_required",
              "v1 POST /drafts -> 409 migration", f"http={sc} error_type={b.get('error_type')} Deprecation={hdr.get('Deprecation')}")
    finally:
        sc, b, _ = call("POST", f"/agent/{agent_id}/branches/{fork_id}/archive")
        print(f"\ncleanup: archived fork {fork_id} -> http={sc} {b.get('data', b)}")
        if created:
            print(f"note: created throwaway agent {agent_id} (no delete endpoint; remove from dashboard if you want).")

    print(f"\n==== {_ok} PASS / {_fail} FAIL ====")
    if _failed:
        print("failed:", _failed)
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())
