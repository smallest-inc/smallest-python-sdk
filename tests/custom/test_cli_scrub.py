"""CLI log hygiene: cluster-internal topology is masked, customer errors pass through."""

import unittest

from smallestai.cli.lib.scrub import scrub_internal


class ScrubInternalTest(unittest.TestCase):
    def test_masks_cluster_internal_ws_url(self):
        text = "connecting ws://agent-abc-123-svc.agents.svc.cluster.local/ws now"
        out = scrub_internal(text)
        self.assertNotIn("cluster.local", out)
        self.assertNotIn("agent-abc-123-svc", out)
        self.assertIn("[internal]", out)

    def test_masks_bare_svc_host_with_port(self):
        out = scrub_internal("dial agent-x-9-svc.agents.svc.cluster.local:8080 failed")
        self.assertNotIn("cluster.local", out)
        self.assertIn("[internal]", out)

    def test_masks_pod_name(self):
        out = scrub_internal("pod agent-abc123-7d9f8b6c4-x2k9p OOMKilled")
        self.assertNotIn("agent-abc123-7d9f8b6c4-x2k9p", out)
        self.assertIn("[internal]", out)

    def test_keeps_customer_env_var_error(self):
        text = "openai.OpenAIError: Missing credentials; set OPENAI_API_KEY"
        self.assertEqual(scrub_internal(text), text)

    def test_keeps_customer_import_error(self):
        text = "ModuleNotFoundError: No module named 'my_package'"
        self.assertEqual(scrub_internal(text), text)

    def test_empty_is_safe(self):
        self.assertEqual(scrub_internal(""), "")


if __name__ == "__main__":
    unittest.main()
