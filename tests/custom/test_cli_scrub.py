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

    def test_masks_statefulset_pod_name(self):
        out = scrub_internal("pod agent-abc123-0 restarting")
        self.assertNotIn("agent-abc123-0", out)
        self.assertIn("[internal]", out)

    def test_masks_private_pod_ip(self):
        for ip in ("10.4.2.7", "172.20.1.9:8080", "192.168.0.5"):
            out = scrub_internal(f"dial tcp {ip}: connection refused")
            self.assertNotIn(ip.split(":")[0], out)
            self.assertIn("[internal]", out)

    def test_masks_bare_svc_address(self):
        for host in ("agent-x-svc.agents:8080", "agent-x-svc.agents", "agent-x-svc:8080"):
            out = scrub_internal(f"connect {host} failed")
            self.assertNotIn("agent-x-svc", out)
            self.assertIn("[internal]", out)

    def test_keeps_agent_and_build_ids(self):
        # The bare agent/build id is needed by the user and must survive.
        text = "build agent-6abca782d27fc8c73fbfb2b1 failed"
        self.assertEqual(scrub_internal(text), text)

    def test_does_not_overmask_bare_svc_token(self):
        # A ``-svc`` token that is not an address (no .ns / :port) is left alone.
        text = "could not import aws-svc client helper"
        self.assertEqual(scrub_internal(text), text)

    def test_keeps_public_api_host(self):
        text = "POST https://api.smallest.ai/atoms/v1/sdk failed with 502"
        self.assertEqual(scrub_internal(text), text)

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
