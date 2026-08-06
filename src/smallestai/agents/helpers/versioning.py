"""Ergonomic helpers over the generated Agent Versioning v2 (branch/revision) client.

Fern generates the raw branch/revision methods and the typed models. This module
adds the two things Fern cannot generate for any SDK:

  1. `wait_for_commit` / `publish_and_wait` — publishing a draft returns only
     `{state: "scanning"}` (HTTP 202) while a security scan runs; there is no
     revision id in that response. The caller has to list the branch's newest
     revision and poll it until `status == "published"`. This wraps that loop.

  2. A discriminator for the three 409 flavors on draft writes, which the raw
     client all surfaces as a single `ConflictError`:
       - error_type == "versioning_v2_migration_required" -> MigrationRequiredError
       - data.conflict{expectedRevision, latestRevision, diffs} -> DraftConflictError
       - errors == ["base_revision_unavailable"]              -> BaseRevisionUnavailableError

This is a thin wrapper over `client.agents.agent_versioning_branches` /
`.agent_versioning_revisions`, so it rides future regens without changes.
"""
from __future__ import annotations

import time
import typing

from ...core.api_error import ApiError


class VersioningError(Exception):
    """Base class for versioning helper errors."""


class MigrationRequiredError(VersioningError):
    """A v1 versioning endpoint was called while the branch model is enabled.

    Migrate to the branch/revision API (client.agents.agent_versioning_branches).
    """


class DraftConflictError(VersioningError):
    """Optimistic-concurrency conflict on update_draft.

    `expectedRevision` did not match the branch's current draft revision because
    another edit landed first. Inspect `.diffs`, then either rebase on
    `.latest_revision` or force-overwrite by resending without expectedRevision.
    """

    def __init__(self, conflict: typing.Dict[str, typing.Any]):
        self.conflict = conflict
        self.expected_revision = conflict.get("expectedRevision")
        self.latest_revision = conflict.get("latestRevision")
        self.diffs = conflict.get("diffs") or []
        # `fields` is the lean prod variant: a list of "<section>.<field>" paths
        # that conflicted, without the structured expected/latest/diffs detail.
        self.fields = conflict.get("fields") or []
        if self.expected_revision is not None or self.latest_revision is not None:
            detail = (
                f"based on r{self.expected_revision}, latest is r{self.latest_revision} "
                f"({len(self.diffs)} section(s) changed)"
            )
        else:
            detail = "conflicting fields: " + (", ".join(self.fields) or "unknown")
        super().__init__(f"draft conflict: {detail}")


class BaseRevisionUnavailableError(VersioningError):
    """`expectedRevision` referenced a base revision that does not exist / is unavailable."""


class SecurityCheckFailedError(VersioningError):
    """The published revision's security scan came back failed."""


def _body_dict(err: ApiError) -> typing.Dict[str, typing.Any]:
    """Best-effort extraction of the raw JSON body from an ApiError.

    `body` is typed `Any`; depending on whether the generator emitted a typed
    error class or fell through to the base ApiError, it may be a dict or a
    pydantic model (with extras preserved). Handle both.
    """
    b = getattr(err, "body", None)
    if isinstance(b, dict):
        return b
    for meth in ("model_dump", "dict"):
        fn = getattr(b, meth, None)
        if callable(fn):
            try:
                out = fn()
                if isinstance(out, dict):
                    return out
            except Exception:
                pass
    return {}


def _discriminate_conflict(err: ApiError) -> Exception:
    body = _body_dict(err)
    if body.get("error_type") == "versioning_v2_migration_required":
        return MigrationRequiredError(str(body.get("message") or body))
    data = body.get("data")
    if isinstance(data, dict) and isinstance(data.get("conflict"), dict):
        return DraftConflictError(data["conflict"])  # dev/rich variant
    errors = body.get("errors") or []
    if isinstance(errors, list):
        if "base_revision_unavailable" in errors:
            return BaseRevisionUnavailableError(str(body))
        # Prod/lean variant: 409 whose `errors` are "<section>.<field>" conflict
        # paths, without the structured data.conflict block. Still a draft conflict.
        if errors:
            return DraftConflictError({"fields": errors})
    return err  # unknown 409 shape: let the original propagate


def _state(obj: typing.Any) -> typing.Optional[str]:
    s = getattr(obj, "state", None)
    return str(s) if s is not None else None


class Versioning:
    """Thin ergonomic facade over the generated v2 versioning client.

    Usage:
        from smallestai import SmallestAI
        from smallestai.agents.helpers.versioning import Versioning

        client = SmallestAI(api_key="...")
        v = Versioning(client)

        branch = v.branches.create_branch(id=agent_id, source_branch_id=main_id, name="feature-x")
        v.update_draft(agent_id, branch.data.id, global_prompt="You are ...", first_message="Hi!")
        revision = v.publish_and_wait(agent_id, branch.data.id)   # blocks until scan completes
        v.branches.make_live(id=agent_id, branch_id=branch.data.id)
    """

    def __init__(self, client: typing.Any):
        self._client = client
        self.branches = client.agents.agent_versioning_branches
        self.revisions = client.agents.agent_versioning_revisions

    def update_draft(self, agent_id: str, branch_id: str, **fields: typing.Any) -> typing.Any:
        """update_draft with the three 409 flavors mapped to typed exceptions.

        Pass the typed config kwargs (global_prompt=, first_message=, synthesizer=, ...)
        and optionally expected_revision= for optimistic concurrency.
        """
        try:
            return self.branches.update_draft(id=agent_id, branch_id=branch_id, **fields)
        except ApiError as e:
            # The 409s (migration / draft-conflict / base-revision) may surface as a
            # typed ConflictError or, if the spec omits the 409 response declaration,
            # as a bare ApiError. ConflictError subclasses ApiError, so this catches both.
            if getattr(e, "status_code", None) == 409:
                raise _discriminate_conflict(e) from e
            raise

    def wait_for_commit(
        self,
        agent_id: str,
        branch_id: str,
        *,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> typing.Any:
        """Poll the branch's newest revision until it reaches `status == "published"`.

        Returns the published Revision. Raises SecurityCheckFailedError if the scan
        fails, or TimeoutError if it does not finish within `timeout` seconds.
        """
        deadline = time.monotonic() + timeout
        last_status = None
        while time.monotonic() < deadline:
            listed = self.revisions.list(id=agent_id, branch_id=branch_id, limit=1)
            revs = getattr(listed.data, "revisions", None) or []
            if revs:
                rev_id = revs[0].id
                got = self.revisions.get(id=agent_id, branch_id=branch_id, revision_id=rev_id)
                rev = getattr(got.data, "revision", None) or got.data
                last_status = getattr(rev, "status", None)
                sec = getattr(rev, "security_check", None)
                sec_status = getattr(sec, "status", None) if sec is not None else None
                if last_status == "published":
                    return rev
                if sec_status == "failed":
                    raise SecurityCheckFailedError(f"security check failed for revision {rev_id}")
            time.sleep(poll_interval)
        raise TimeoutError(
            f"revision did not reach 'published' within {timeout}s (last status={last_status})"
        )

    def publish_and_wait(
        self,
        agent_id: str,
        branch_id: str,
        *,
        label: typing.Optional[str] = None,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> typing.Any:
        """Publish the branch's open draft and block until the revision is published.

        Handles both publish outcomes: sync `committed` (revision inline) and async
        `scanning` (poll until published).
        """
        res = self.branches.publish_draft(id=agent_id, branch_id=branch_id, label=label)
        data = res.data
        if _state(data) == "committed" and getattr(data, "revision", None) is not None:
            return data.revision
        return self.wait_for_commit(
            agent_id, branch_id, timeout=timeout, poll_interval=poll_interval
        )

    def edit_and_publish(
        self,
        agent_id: str,
        branch_id: str,
        *,
        label: typing.Optional[str] = None,
        expected_revision: typing.Optional[int] = None,
        timeout: float = 120.0,
        poll_interval: float = 2.0,
        **fields: typing.Any,
    ) -> typing.Any:
        """One-call config edit: update the draft with `fields`, then publish and wait.

        The simple "change the agent's config" path over the versioned draft->publish
        flow. Pass the typed config kwargs (global_prompt=, synthesizer=, ...). Returns
        the published Revision. Raises DraftConflictError if `expected_revision` is stale.
        """
        kwargs = dict(fields)
        if expected_revision is not None:
            kwargs["expected_revision"] = expected_revision
        self.update_draft(agent_id, branch_id, **kwargs)
        return self.publish_and_wait(
            agent_id, branch_id, label=label, timeout=timeout, poll_interval=poll_interval
        )
