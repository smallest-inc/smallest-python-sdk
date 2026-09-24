"""Actionable-error helpers shared by the enriched ApiError / BadRequestError.

Hand-maintained (see .fernignore). Kept dependency-free (no imports of the error
classes) so the error modules can import it without a cycle.

The plan-gate detection matches the platform's payment-entitlement middleware
(atoms main-backend access.middleware.ts): a gated feature is rejected with an
HTTP 400 body `{ "status": false, "errors": ["… please upgrade to a higher plan …"] }`.
"""

import typing

# Substrings that identify a plan/entitlement-gated 400 (feature not on plan, or
# Identifies an org allow-list gate (HTTP 403) — not plan-upgradeable by the user
# (e.g. GPT 5.2, conversational-flow agents).
_ORG_GATE_MARKER = "not available for your organization"


def _body_text(body: typing.Any) -> str:
    if body is None:
        return ""
    if isinstance(body, str):
        return body
    if isinstance(body, dict):
        # Platform error envelope is {status: false, errors: [...]}; also handle
        # the common single-field shapes.
        errors = body.get("errors")
        parts: typing.List[str] = []
        if isinstance(errors, (list, tuple)):
            parts.extend(str(e) for e in errors)
        elif errors:
            parts.append(str(errors))
        parts.extend(str(body.get(k, "")) for k in ("message", "error", "detail", "reason"))
        joined = " ".join(p for p in parts if p)
        return joined or str(body)
    return str(body)


def looks_plan_gated(body: typing.Any) -> bool:
    """Does this 400 body look like a plan/entitlement gate?

    Every plan-gating message the platform returns pairs "upgrade" with "plan"
    — the feature-access family ("Your plan has no access to X, please upgrade to
    a higher plan"), the limit family ("… reached the maximum … for your plan,
    please upgrade …"), and the product-specific ones ("… not available in your
    current plan. Please upgrade."). A generic 400 (validation, bad input) won't
    contain both words, so this stays specific. Verified against atoms
    main-backend (access.middleware.ts + constants/error-messages.ts)."""
    text = _body_text(body).lower()
    return "upgrade" in text and "plan" in text


def _looks_org_gated(body: typing.Any) -> bool:
    return _ORG_GATE_MARKER in _body_text(body).lower()


def hint_for(status_code: typing.Optional[int], body: typing.Any) -> str:
    """A one-line, actionable hint to append to an error message, or '' if none."""
    if status_code == 401:
        return (
            "Authentication failed. Check your API key (SMALLEST_API_KEY) — "
            "get one at https://app.smallest.ai/dashboard/api-keys."
        )
    if status_code == 400 and looks_plan_gated(body):
        return (
            "This feature (or limit) is not included in your current plan. "
            "Upgrade at https://app.smallest.ai or contact your account team."
        )
    if status_code == 403:
        if _looks_org_gated(body):
            return "This feature is limited to specific organizations. Contact your account team to enable it."
        return "Your API key is valid but is not permitted to perform this action."
    return ""
