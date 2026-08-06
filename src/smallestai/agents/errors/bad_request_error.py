# Hand-maintained (see .fernignore). Kept out of regeneration to auto-specialize
# a plan/entitlement-gated 400 into PlanNotEntitledError. Re-apply after a regen.

import typing

from ...core._error_hints import looks_plan_gated
from ...core.api_error import ApiError


class BadRequestError(ApiError):
    def __new__(cls, body: typing.Any = None, headers: typing.Optional[typing.Dict[str, str]] = None):
        # The platform returns plan/entitlement gating as a 400 with an
        # "…upgrade to a higher plan…" message (see access.middleware.ts). Return
        # it as PlanNotEntitledError so callers can catch it distinctly. It
        # subclasses BadRequestError, so `except BadRequestError` still works.
        if cls is BadRequestError and looks_plan_gated(body):
            return super().__new__(PlanNotEntitledError)
        return super().__new__(cls)

    def __init__(self, body: typing.Any, headers: typing.Optional[typing.Dict[str, str]] = None):
        super().__init__(status_code=400, headers=headers, body=body)


class PlanNotEntitledError(BadRequestError):
    """A request rejected because the org's plan doesn't include the feature (or a
    plan limit was hit) — the platform returns HTTP 400 with a "…please upgrade to
    a higher plan…" message. Subclass of BadRequestError, so `except
    BadRequestError` still catches it. Gated features include campaigns, knowledge
    base, webhooks, integrations, phone numbers, inbound/outbound telephony, and
    the waves models. Detection matches the platform message
    (access.middleware.ts) — see SDK_ESCALATIONS.log."""
