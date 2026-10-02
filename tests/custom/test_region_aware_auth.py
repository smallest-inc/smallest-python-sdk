"""Region-aware auth login: `--base-url` is persisted and honored by the clients.

`auth login --base-url https://api.india.smallest.ai` pins the regional host so a
non-default-region user does not have to set SMALLEST_BASE_URL on every command.
Precedence: SMALLEST_BASE_URL env > the host pinned at login > the default.
"""

import os
import tempfile
import unittest
from unittest import mock

from smallestai.cli.lib.atoms import AtomsAPIClient


class RegionAwareAuthTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._home = mock.patch.dict(os.environ, {"HOME": self._tmp.name}, clear=False)
        self._home.start()
        os.environ.pop("SMALLEST_BASE_URL", None)
        from smallestai.cli.lib import client as client_mod
        from smallestai.cli.lib.auth import AuthClient

        self.AuthClient = AuthClient
        self.client_mod = client_mod

    def tearDown(self):
        self._home.stop()
        self._tmp.cleanup()

    def test_login_persists_base_url_stripped(self):
        ac = self.AuthClient()
        ac.login("sk_test", base_url="https://api.india.smallest.ai/")
        self.assertEqual(ac.get_base_url(), "https://api.india.smallest.ai")  # trailing slash stripped
        self.assertEqual(ac.get_credentials()["access_token"], "sk_test")

    def test_login_without_base_url_stores_none(self):
        ac = self.AuthClient()
        ac.login("sk_test")
        self.assertIsNone(ac.get_base_url())

    def test_resolve_base_url_precedence(self):
        ac = self.AuthClient()
        ac.login("sk_test", base_url="https://api.india.smallest.ai")
        # pinned host wins over default
        self.assertEqual(self.client_mod.resolve_base_url(ac), "https://api.india.smallest.ai")
        # SMALLEST_BASE_URL env overrides the pinned host
        with mock.patch.dict(os.environ, {"SMALLEST_BASE_URL": "https://api.dev.smallest.ai"}):
            self.assertEqual(self.client_mod.resolve_base_url(ac), "https://api.dev.smallest.ai")

    def test_resolve_base_url_default(self):
        ac = self.AuthClient()  # no login
        self.assertEqual(self.client_mod.resolve_base_url(ac), "https://api.smallest.ai")

    def test_atoms_client_honors_base_url(self):
        self.assertEqual(
            AtomsAPIClient(base_url="https://api.india.smallest.ai/").base_url,
            "https://api.india.smallest.ai",
        )
        self.assertEqual(AtomsAPIClient().base_url, "https://api.smallest.ai")


if __name__ == "__main__":
    unittest.main()
