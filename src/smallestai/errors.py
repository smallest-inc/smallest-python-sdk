"""Public error types for the SmallestAI SDK.

    from smallestai.errors import PlanNotEntitledError, ForbiddenError, ApiError

Every SDK error subclasses ``ApiError`` (exposes ``.status_code``, ``.body``,
``.headers``). A plan/entitlement-gated 403 is raised as ``PlanNotEntitledError``
(a subclass of ``ForbiddenError``), so you can handle "needs a higher plan"
distinctly while ``except ForbiddenError`` still catches it.
"""

from smallestai.atoms.errors.bad_request_error import BadRequestError
from smallestai.atoms.errors.conflict_error import ConflictError
from smallestai.atoms.errors.forbidden_error import ForbiddenError, PlanNotEntitledError
from smallestai.atoms.errors.not_found_error import NotFoundError
from smallestai.atoms.errors.too_many_requests_error import TooManyRequestsError
from smallestai.atoms.errors.unauthorized_error import UnauthorizedError
from smallestai.core.api_error import ApiError

__all__ = [
    "ApiError",
    "BadRequestError",
    "ConflictError",
    "ForbiddenError",
    "NotFoundError",
    "PlanNotEntitledError",
    "TooManyRequestsError",
    "UnauthorizedError",
]
