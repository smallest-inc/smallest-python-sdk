"""Scrub cluster-internal infra topology out of user-facing CLI output.

Build logs, deploy errors, and build-detail panels can carry our internal K8s
topology: the cluster-internal service URL
(``ws://agent-<agent>-<build>-svc.agents.svc.cluster.local/ws``), pod names,
and raw internal stack traces. That is useless to customers and leaks our
infra, so by default we mask it. The raw text is still available with
``--verbose``.
"""

from __future__ import annotations

import re

# Cluster-internal service / DNS names, e.g.
#   ws://agent-abc-123-svc.agents.svc.cluster.local/ws
#   agent-abc-123-svc.agents.svc.cluster.local
_INTERNAL_URL_RE = re.compile(
    r"\bwss?://[a-z0-9.\-]*\.svc\.cluster\.local(?::\d+)?(?:/\S*)?",
    re.IGNORECASE,
)
_INTERNAL_HOST_RE = re.compile(
    r"\b[a-z0-9.\-]*\.svc\.cluster\.local(?::\d+)?",
    re.IGNORECASE,
)
# Pod names, e.g. agent-abc123-7d9f8b6c4-x2k9p (deployment-replicaset-pod suffix).
_POD_NAME_RE = re.compile(
    r"\bagent-[a-z0-9]+-[a-f0-9]{8,10}-[a-z0-9]{5}\b",
    re.IGNORECASE,
)

_MASK = "[internal]"


def scrub_internal(text: str) -> str:
    """Replace cluster-internal URLs, hostnames, and pod names with a mask."""
    if not text:
        return text
    text = _INTERNAL_URL_RE.sub(_MASK, text)
    text = _INTERNAL_HOST_RE.sub(_MASK, text)
    text = _POD_NAME_RE.sub(_MASK, text)
    return text
