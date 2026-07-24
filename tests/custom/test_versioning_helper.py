"""Unit tests for the Versioning helper — the 409 discriminator + facade wiring.

No network: these exercise the exception-discrimination logic against synthetic
ApiError bodies (dev's rich `data.conflict` shape, prod's lean `errors` shape, the
migration flag, and the base-revision case). Live coverage is in
tests/velocity/v2_versioning_e2e.py.
"""
from smallestai.atoms.helpers import (
    Versioning,
    VersioningError,
    MigrationRequiredError,
    DraftConflictError,
    BaseRevisionUnavailableError,
    SecurityCheckFailedError,
)
from smallestai.atoms.helpers.versioning import _discriminate_conflict
from smallestai.core.api_error import ApiError


def _conflict(body):
    return _discriminate_conflict(ApiError(status_code=409, headers={}, body=body))


def test_migration_required():
    e = _conflict({"error_type": "versioning_v2_migration_required"})
    assert isinstance(e, MigrationRequiredError)


def test_draft_conflict_rich_dev_shape():
    e = _conflict(
        {"data": {"conflict": {"expectedRevision": 2, "latestRevision": 3,
                               "diffs": [{"section": "workflow_prompt"}]}}}
    )
    assert isinstance(e, DraftConflictError)
    assert e.expected_revision == 2
    assert e.latest_revision == 3
    assert len(e.diffs) == 1


def test_draft_conflict_lean_prod_shape():
    e = _conflict({"status": False, "errors": ["workflow_prompt.globalPrompt"]})
    assert isinstance(e, DraftConflictError)
    assert e.fields == ["workflow_prompt.globalPrompt"]


def test_base_revision_unavailable():
    e = _conflict({"status": False, "errors": ["base_revision_unavailable"]})
    assert isinstance(e, BaseRevisionUnavailableError)


def test_all_versioning_errors_share_base():
    for cls in (
        MigrationRequiredError,
        DraftConflictError,
        BaseRevisionUnavailableError,
        SecurityCheckFailedError,
    ):
        assert issubclass(cls, VersioningError)


def test_facade_wires_generated_clients():
    branches = object()
    revisions = object()

    class _Atoms:
        agent_versioning_branches = branches
        agent_versioning_revisions = revisions

    class _Client:
        atoms = _Atoms()

    v = Versioning(_Client())
    assert v.branches is branches
    assert v.revisions is revisions
