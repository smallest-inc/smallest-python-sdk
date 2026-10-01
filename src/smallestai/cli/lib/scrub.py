"""Scrub cluster-internal infra topology out of user-facing CLI output.

Build logs, deploy errors, and build-detail panels can carry our internal K8s
topology: the cluster-internal service URL
(``ws://agent-<agent>-<build>-svc.agents.svc.cluster.local/ws``), pod names,
pod IPs, and raw internal stack traces. That is useless to customers and leaks
our infra, so we always mask it. There is no raw/unscrubbed mode: ``--verbose``
on the log stream controls volume (every line vs. status + tail), not masking,
so no CLI invocation ever prints raw topology.

Design note: this is a leak *filter*, not a parser. It errs toward masking.
A false positive (masking something harmless) is acceptable; a false negative
(leaking a pod name or internal host) is not. The patterns below are
deliberately broad for that reason. Scrubbing is applied at the output boundary
(``_print_error`` and the log-stream printers), so it does not matter which
exception type produced the string: everything the crew CLI prints is scrubbed.
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
    r"|\bagent-[a-z0-9\-]+-\d{1,3}\b",  # statefulset pod
    re.IGNORECASE,
)
# Private / cluster pod IPs (RFC-1918), optional port:
#   10.x.x.x, 172.16-31.x.x, 192.168.x.x
_INTERNAL_IP_RE = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3})(?::\d+)?\b",
)

# Region-coded public API hosts, e.g. api.in.smallest.ai / api.us.smallest.ai.
# These reveal which region an account is pinned to. Account-to-region is not
# auto geo-assigned, so exposing an org's region is a placement/security risk,
# mask it. The bare public host ``api.smallest.ai`` (no region segment) and the
# dashboard ``app.smallest.ai`` carry no region and are intentionally kept.
_REGION_HOST_RE = re.compile(
    r"\bapi\.[a-z]{2}\.smallest\.ai\b",
    re.IGNORECASE,
)
# Cloud region / availability-zone tokens, e.g. ap-south-1, us-west-2,
# eu-central-1, ap-south-1a. Reveals where the infra runs.
_CLOUD_REGION_RE = re.compile(
    r"\b(?:af|ap|ca|cn|eu|il|me|sa|us)-"
    r"(?:north|south|east|west|central|northeast|northwest|southeast|southwest)-\d[a-z]?\b",
    re.IGNORECASE,
)

_MASK = "[internal]"

_PATTERNS = (
    _INTERNAL_URL_RE,
    _INTERNAL_HOST_RE,
    _INTERNAL_SVC_RE,
    _POD_NAME_RE,
    _INTERNAL_IP_RE,
    _REGION_HOST_RE,
    _CLOUD_REGION_RE,
)


def scrub_internal(text: str) -> str:
    """Replace cluster-internal URLs, hostnames, service names, pod names, pod
    IPs, region-coded API hosts (api.<region>.smallest.ai), and cloud-region
    tokens (ap-south-1, ...) with a mask. Order matters: URL/host before the
    bare-service pattern so a full FQDN is masked as one unit."""
    if not text:
        return text
    for pattern in _PATTERNS:
        text = pattern.sub(_MASK, text)
    return text
