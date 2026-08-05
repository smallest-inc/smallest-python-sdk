# Hand-maintained (see .fernignore). Kept out of regeneration to auto-specialize
# a plan-gated 403 into PlanNotEntitledError. Re-apply after a regen.

import typing

from ...core._error_hints import looks_plan_gated
from ...core.api_error import ApiError


class ForbiddenError(ApiError):
    def __new__(cls, body: typing.Any = None, headers: typing.Optional[typing.Dict[str, str]] = None):
        # A 403 whose body looks like a plan/entitlement gate is returned as a
        # PlanNotEntitledError so callers can `except PlanNotEntitledError`.
        # It subclasses ForbiddenError, so existing `except ForbiddenError`
        # handlers keep working — fully backward-compatible.
        if cls is ForbiddenError and looks_plan_gated(body):
            return super().__new__(PlanNotEntitledError)
        return super().__new__(cls)

    def __init__(self, body: typing.Any, headers: typing.Optional[typing.Dict[str, str]] = None):
        super().__init__(status_code=403, headers=headers, body=body)


class PlanNotEntitledError(ForbiddenError):
    """A 403 that looks like a plan / entitlement gate — the API key is valid but
    the feature needs a higher plan (e.g. an Enterprise-only feature such as DNC
    writes). Subclass of ForbiddenError, so `except ForbiddenError` still catches
    it. The exact detection is a heuristic until the platform returns a stable
    machine-readable code (see SDK_ESCALATIONS.log)."""
