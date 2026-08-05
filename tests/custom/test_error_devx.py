"""DevX: actionable error messages + PlanNotEntitledError specialization.

The platform returns plan/entitlement gating as an HTTP 400 with body
`{status: false, errors: ["… please upgrade to a higher plan …"]}` (see atoms
main-backend access.middleware.ts). It should surface as PlanNotEntitledError
while staying a BadRequestError (backward-compatible).
"""
import unittest

from smallestai import PlanNotEntitledError as PlanNotEntitledFromRoot
from smallestai.atoms.errors.bad_request_error import BadRequestError, PlanNotEntitledError
from smallestai.atoms.errors.unauthorized_error import UnauthorizedError
from smallestai.core.api_error import ApiError
from smallestai.errors import PlanNotEntitledError as PlanNotEntitledFromErrors

_PLAN_GATED_BODY = {
    "status": False,
    "errors": ["Your plan has no access to campaigns, please upgrade to a higher plan to access this feature"],
}
_LIMIT_BODY = {
    "status": False,
    "errors": ["You have reached the maximum number of agents for your plan, please upgrade to a higher plan to create more agents"],
}


class ErrorDevxTest(unittest.TestCase):
    def test_plan_gated_400_becomes_plan_not_entitled(self):
        err = BadRequestError(body=_PLAN_GATED_BODY)
        self.assertIsInstance(err, PlanNotEntitledError)
        self.assertIsInstance(err, BadRequestError)
        self.assertEqual(err.status_code, 400)

    def test_plan_limit_400_also_specializes(self):
        self.assertIsInstance(BadRequestError(body=_LIMIT_BODY), PlanNotEntitledError)

    def test_generic_400_stays_bad_request(self):
        err = BadRequestError(body={"status": False, "errors": ["voiceId is required"]})
        self.assertIsInstance(err, BadRequestError)
        self.assertNotIsInstance(err, PlanNotEntitledError)

    def test_catch_as_plan_not_entitled(self):
        try:
            raise BadRequestError(body=_PLAN_GATED_BODY)
        except PlanNotEntitledError:
            pass
        else:
            self.fail("expected PlanNotEntitledError")

    def test_exported_symbols_are_the_same_class(self):
        self.assertIs(PlanNotEntitledFromRoot, PlanNotEntitledError)
        self.assertIs(PlanNotEntitledFromErrors, PlanNotEntitledError)

    def test_401_message_has_auth_hint(self):
        self.assertIn("SMALLEST_API_KEY", str(UnauthorizedError(body={"errors": ["invalid token"]})))

    def test_plan_gated_message_has_upgrade_hint(self):
        msg = str(BadRequestError(body=_PLAN_GATED_BODY)).lower()
        self.assertIn("plan", msg)
        self.assertIn("upgrade", msg)

    def test_no_hint_noise_on_plain_error(self):
        msg = str(ApiError(status_code=500, body="boom"))
        self.assertIn("boom", msg)
        self.assertNotIn("SMALLEST_API_KEY", msg)


if __name__ == "__main__":
    unittest.main()
