"""Actionable-error helpers shared by the enriched ApiError / ForbiddenError.

Hand-maintained (see .fernignore). Kept dependency-free (no imports of the error
classes) so the error modules can import it without a cycle.
"""

import typing

# Markers that suggest a 403 is a plan/entitlement gate (feature needs a higher
# plan) rather than a generic permission denial. Best-effort heuristic until the
# platform exposes a stable machine-readable code — see SDK_ESCALATIONS.log.
# Kept reasonably specific to avoid mislabelling ordinary permission errors.
_PLAN_GATE_MARKERS = (
    "your plan",
    "upgrade",
    "entitl",  # entitled / entitlement
    "not available on your",
    "not enabled for your",
    "enterprise plan",
    "subscription required",
    "plan_upgrade_required",
    "feature_not_entitled",
    "requires a paid",
)


def _body_text(body: typing.Any) -> str:
    if body is None:
        return ""
    if isinstance(body, str):
        return body
    if isinstance(body, dict):
        parts = [str(body.get(k, "")) for k in ("message", "error", "code", "detail", "reason")]
        joined = " ".join(p for p in parts if p)
        return joined or str(body)
    return str(body)


def looks_plan_gated(body: typing.Any) -> bool:
    """Best-effort: does this 403 body look like a plan/entitlement gate?"""
    text = _body_text(body).lower()
    return bool(text) and any(m in text for m in _PLAN_GATE_MARKERS)


def hint_for(status_code: typing.Optional[int], body: typing.Any) -> str:
    """A one-line, actionable hint to append to an error message, or '' if none."""
    if status_code == 401:
        return (
            "Authentication failed. Check your API key (SMALLEST_API_KEY) — "
            "get one at https://app.smallest.ai/dashboard/api-keys."
        )
    if status_code == 403:
        if looks_plan_gated(body):
            return (
                "This looks like a plan-gated feature. It may require a plan "
                "upgrade (e.g. an Enterprise feature) — check your plan at "
                "https://app.smallest.ai or contact your account team."
            )
        return "Your API key is valid but is not permitted to perform this action."
    return ""
