"""Scrub cluster-internal infra topology out of user-facing CLI output.

Build logs, deploy errors, and build-detail panels can carry our internal K8s
topology: the cluster-internal service URL
(``ws://agent-<agent>-<build>-svc.agents.svc.cluster.local/ws``), pod names,
pod IPs, and raw internal stack traces. That is useless to customers and leaks
our infra, so by default we mask it. The raw text is still available with
``--verbose``.

Design note: this is a leak *filter*, not a parser. It errs toward masking.
A false positive (masking something harmless) is acceptable; a false negative
(leaking a pod name or internal host) is not. The patterns below are
deliberately broad for that reason. Scrubbing is applied at the output boundary
(see ``emit_error``), so it does not matter which exception type produced the
string: anything printed through the crew error path is scrubbed the same way.
"""

from __future__ import annotations

import re

# Cluster-internal service / DNS, e.g.
#   ws://agent-abc-123-svc.agents.svc.cluster.local/ws
#   agent-abc-123-svc.agents.svc.cluster.local:8080
_INTERNAL_URL_RE = re.compile(
    r"\bwss?://[a-z0-9.\-]*\.(?:svc\.cluster\.local|cluster\.local|local)(?::\d+)?(?:/\S*)?",
    re.IGNORECASE,
)
_INTERNAL_HOST_RE = re.compile(
    r"\b[a-z0-9.\-]*\.(?:svc\.cluster\.local|cluster\.local)(?::\d+)?",
    re.IGNORECASE,
)
# Bare in-namespace Kubernetes service names (no cluster domain), e.g.
#   agent-abc-123-svc.agents:8080
#   some-svc.default
#   agent-x-svc:8080
# K8s services conventionally carry a ``-svc`` segment. Require it to be an
# actual address (followed by ``.<namespace>`` or ``:<port>``) so a bare token
# like ``aws-svc`` in a customer error is not masked.
_INTERNAL_SVC_RE = re.compile(
    r"\b[a-z0-9\-]+-svc(?:\.[a-z0-9\-]+(?::\d+)?|:\d+)\b",
    re.IGNORECASE,
)
# Pod names:
#   deployment-replicaset-pod, e.g. agent-abc123-7d9f8b6c4-x2k9p
#   statefulset-ordinal,       e.g. agent-abc123-0
# The bare agent/build id (``agent-<24hex>``, no further ``-<group>``) is left
# intact: callers need it. Both shapes require at least one extra dash-group
# beyond the id, which a bare id never has.
_POD_NAME_RE = re.compile(
    r"\bagent-[a-z0-9\-]+-[a-z0-9]{8,10}-[a-z0-9]{5}\b"  # replicaset pod
    r"|\bagent-[a-z0-9\-]+-\d{1,3}\b",                    # statefulset pod
    re.IGNORECASE,
)
# Private / cluster pod IPs (RFC-1918), optional port:
#   10.x.x.x, 172.16-31.x.x, 192.168.x.x
_INTERNAL_IP_RE = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})(?::\d+)?\b",
)

_MASK = "[internal]"

_PATTERNS = (
    _INTERNAL_URL_RE,
    _INTERNAL_HOST_RE,
    _INTERNAL_SVC_RE,
    _POD_NAME_RE,
    _INTERNAL_IP_RE,
)


def scrub_internal(text: str) -> str:
    """Replace cluster-internal URLs, hostnames, service names, pod names, and
    pod IPs with a mask. Order matters: URL/host before the bare-service pattern
    so a full FQDN is masked as one unit."""
    if not text:
        return text
    for pattern in _PATTERNS:
        text = pattern.sub(_MASK, text)
    return text


def safe(text: str, verbose: bool = False) -> str:
    """Return ``text`` as-is when ``verbose`` (support wants raw infra detail),
    otherwise scrubbed. Single place that encodes the verbose escape hatch."""
    return text if verbose else scrub_internal(text)
