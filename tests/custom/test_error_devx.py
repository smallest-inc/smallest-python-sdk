"""DevX: actionable error messages + PlanNotEntitledError specialization.

A plan-gated 403 should be catchable as PlanNotEntitledError while staying a
ForbiddenError (backward-compatible). Error messages should carry an actionable
hint for auth (401) and plan-gated (403) failures.
"""
import unittest

from smallestai import PlanNotEntitledError as PlanNotEntitledFromRoot
from smallestai.atoms.errors.forbidden_error import ForbiddenError, PlanNotEntitledError
from smallestai.atoms.errors.unauthorized_error import UnauthorizedError
from smallestai.core.api_error import ApiError
from smallestai.errors import PlanNotEntitledError as PlanNotEntitledFromErrors


class ErrorDevxTest(unittest.TestCase):
    def test_plan_gated_403_becomes_plan_not_entitled(self):
        err = ForbiddenError(body={"message": "DNC is not available on your plan. Upgrade to Enterprise."})
        self.assertIsInstance(err, PlanNotEntitledError)
        self.assertIsInstance(err, ForbiddenError)  # backward-compatible
        self.assertEqual(err.status_code, 403)

    def test_generic_403_stays_forbidden(self):
        err = ForbiddenError(body={"message": "You do not have access to this resource."})
        self.assertIsInstance(err, ForbiddenError)
        self.assertNotIsInstance(err, PlanNotEntitledError)

    def test_explicit_plan_error_construction(self):
        err = PlanNotEntitledError(body={"message": "feature_not_entitled"})
        self.assertIsInstance(err, PlanNotEntitledError)
        self.assertEqual(err.status_code, 403)

    def test_exported_symbols_are_the_same_class(self):
        self.assertIs(PlanNotEntitledFromRoot, PlanNotEntitledError)
        self.assertIs(PlanNotEntitledFromErrors, PlanNotEntitledError)

    def test_401_message_has_auth_hint(self):
        msg = str(UnauthorizedError(body={"message": "invalid token"}))
        self.assertIn("SMALLEST_API_KEY", msg)

    def test_plan_gated_message_has_upgrade_hint(self):
        msg = str(ForbiddenError(body={"message": "requires a paid plan; upgrade your plan"}))
        self.assertIn("plan-gated", msg.lower())

    def test_success_case_no_hint_noise(self):
        # A non-auth, non-403 error keeps a clean message.
        msg = str(ApiError(status_code=500, body="boom"))
        self.assertIn("boom", msg)
        self.assertNotIn("SMALLEST_API_KEY", msg)


if __name__ == "__main__":
    unittest.main()
