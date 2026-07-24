#!/usr/bin/env python3
"""Live E2E for the Agent Versioning v2 (branch/revision) SDK surface.

Runs the full branch/revision lifecycle THROUGH the generated typed client and
the `Versioning` helper, against a live backend, on a throwaway forked branch
that it archives afterward. This is the script we run against every regen that
touches the versioning surface, before shipping.

Requirements:
    SMALLEST_API_KEY   - bearer key for the target environment
    SMALLEST_BASE_URL  - optional atoms base, e.g. https://api.dev.smallest.ai/atoms/v1
                         (omit to hit Production)
    E2E_AGENT_ID       - optional agent to fork from (default: a dev test agent)

Usage:
    SMALLEST_API_KEY=sk_... SMALLEST_BASE_URL=https://api.dev.smallest.ai/atoms/v1 \
        python tests/velocity/v2_versioning_e2e.py
"""
import os
import sys

from smallestai import SmallestAI
from smallestai.environment import SmallestAIEnvironment
from smallestai.atoms.helpers.versioning import (
    Versioning,
    DraftConflictError,
    MigrationRequiredError,
)

KEY = os.environ.get("SMALLEST_API_KEY")
BASE = os.environ.get("SMALLEST_BASE_URL")
AGENT = os.environ.get("E2E_AGENT_ID", "6a61ec314138fd26c7acd84f")

if not KEY:
    print("SMALLEST_API_KEY is required")
    sys.exit(2)


def make_client() -> SmallestAI:
    if BASE:
        host = BASE.split("/atoms")[0]
        ws = host.replace("https://", "wss://").replace("http://", "ws://")
        env = SmallestAIEnvironment(atoms=BASE, waves=host, waves_ws=ws)
        return SmallestAI(environment=env, api_key=KEY)
    return SmallestAI(api_key=KEY)


_ok = 0
_fail = 0
_failed = []


def check(cond: bool, label: str, detail: str = "") -> None:
    global _ok, _fail
    print(("  PASS " if cond else "  FAIL ") + label + (f"  {detail}" if detail else ""))
    if cond:
        _ok += 1
    else:
        _fail += 1
        _failed.append(label)


def main() -> int:
    client = make_client()
    v = Versioning(client)
    fork_id = None
    try:
        print(f"\n== agent {AGENT} @ {BASE or 'PRODUCTION'} ==")

        # list + find main
        listed = v.branches.list(id=AGENT)
        branches = listed.data.branches
        main = next(b for b in branches if b.branch.is_default)
        main_id = main.branch.id
        check(bool(branches) and main_id, "branches.list -> main", f"main={main_id} isLive={main.is_live}")

        # fork
        fk = v.branches.create_branch(id=AGENT, source_branch_id=main_id, name=f"e2e-{os.getpid()}")
        fork_id = fk.data.id
        check(fork_id is not None and fk.data.status == "active", "create_branch (fork)", f"id={fork_id}")

        # typed update_draft via helper
        ud = v.update_draft(AGENT, fork_id, global_prompt="E2E typed prompt", first_message="Hi from e2e")
        check(ud is not None, "update_draft (typed kwargs)", f"draftRevision={getattr(ud.data,'draft_revision',None)}")

        # get_draft
        gd = v.branches.get_draft(id=AGENT, branch_id=fork_id)
        check(gd.data.latest is not None, "get_draft (DraftDetail)", f"editCount={gd.data.edit_count}")
        cur_rev = gd.data.latest.draft_revision

        # publish + wait_for_commit (helper handles scanning->poll)
        revision = v.publish_and_wait(AGENT, fork_id, label="e2e", timeout=90, poll_interval=2)
        check(getattr(revision, "status", None) == "published", "publish_and_wait -> published",
              f"rev={getattr(revision,'id',None)} securityCheck={getattr(getattr(revision,'security_check',None),'status',None)}")

        # revisions list / get / history
        rl = v.revisions.list(id=AGENT, branch_id=fork_id)
        check(rl.data.revisions is not None, "revisions.list", f"count={len(rl.data.revisions or [])}")
        rid = revision.id
        rg = v.revisions.get(id=AGENT, branch_id=fork_id, revision_id=rid)
        check(rg.data is not None, "revisions.get", "")
        rh = v.revisions.get_history(id=AGENT, branch_id=fork_id, revision_id=rid)
        check(rh.data is not None, "revisions.get_history", "")

        # test_call
        tc = v.branches.test_call(id=AGENT, branch_id=fork_id, mode="webcall")
        check(tc.data is not None, "test_call (webcall)", "")

        # DraftConflict discriminator: open a fresh edit then send a stale expected_revision
        v.update_draft(AGENT, fork_id, global_prompt="edit A")
        gd2 = v.branches.get_draft(id=AGENT, branch_id=fork_id)
        latest_rev = gd2.data.latest.draft_revision
        v.update_draft(AGENT, fork_id, expected_revision=latest_rev, global_prompt="edit B")  # bumps
        conflict_raised = False
        try:
            v.update_draft(AGENT, fork_id, expected_revision=latest_rev, global_prompt="edit C stale")
        except DraftConflictError as e:
            conflict_raised = True
            # dev returns the rich data.conflict (diffs); prod returns lean errors (fields).
            has_detail = bool(e.diffs) or bool(getattr(e, "fields", []))
            check(has_detail, "DraftConflictError discriminated",
                  f"expected={e.expected_revision} latest={e.latest_revision} diffs={len(e.diffs)} fields={getattr(e,'fields',[])}")
        check(conflict_raised, "stale expected_revision raises DraftConflictError")

        # publish the pending draft edits as a 2nd revision, so restore has an
        # OLDER target than head (restoring the current head is a 409 no-op).
        rev2 = v.publish_and_wait(AGENT, fork_id, label="e2e-2", timeout=90, poll_interval=2)
        check(getattr(rev2, "status", None) == "published", "second publish -> published",
              f"rev={getattr(rev2,'id',None)}")

        # restore the FIRST revision (older than head) -> new head revision
        rr = v.revisions.restore(id=AGENT, branch_id=fork_id, revision_id=rid)
        check(rr.data is not None, "revisions.restore (older revision)", f"state={getattr(rr.data,'state',None)}")
        ml = v.branches.make_live(id=AGENT, branch_id=fork_id)
        check(ml.data is not None, "make_live (fork)", "")
        v.branches.make_live(id=AGENT, branch_id=main_id)  # revert
        check(True, "make_live (revert to main)")

        print(f"\n==== {_ok} PASS / {_fail} FAIL ====")
        if _failed:
            print("failed:", _failed)
        return 1 if _fail else 0
    finally:
        if fork_id:
            try:
                arch = v.branches.archive(id=AGENT, branch_id=fork_id)
                print(f"cleanup: archived fork {fork_id} -> {arch.data}")
            except Exception as e:
                print(f"cleanup: archive failed for {fork_id}: {e}")


if __name__ == "__main__":
    sys.exit(main())
