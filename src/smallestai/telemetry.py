"""Anonymous, opt-out usage telemetry.

Hand-written and listed in .fernignore, so an SDK regeneration never touches it.

Two kinds of events go to Smallest's platform PostHog project ("New Smallest Inc"):

- ``cli_invoked``: which CLI command group ran (see ``smallestai.cli.main``).
- ``sdk_method_called``: which SDK method ran and whether it succeeded. Recorded by
  the HTTP client hook in ``smallestai.core._telemetry_http_client``.

It is deliberately minimal and privacy-first:

- NO personal data or secrets: never an API key, header, URL, query string, request or
  response body, text, audio, agent id, phone number, file path, or error message.
- ``sdk_method_called`` carries exactly: SDK version, Python version, OS name
  (``platform.system()``), the SDK method name, success (bool) and, on failure, the
  error class name plus ``http_status`` (int) when the failure was an HTTP error
  response, and ``$sample_rate`` (see Sampling below). Plus a random anonymous install id as PostHog's ``distinct_id``
  (a uuid4 kept in a local config file, never derived from the API key, host or user).
  It asks PostHog to skip GeoIP enrichment and person profiles. (``cli_invoked`` keeps
  PostHog's default server-side country lookup, as since 5.10.0.)
- Fire-and-forget on a background daemon thread with a short timeout. It never
  blocks the API call, never changes its result or its errors, and never raises.

Sampling: ``sdk_method_called`` is sampled per event (default 10%, override with
``SMALLEST_TELEMETRY_SAMPLE_RATE``, a float from 0 to 1). The keep/drop decision is
``random.random() < rate``, made before the event is built or queued (and, in the HTTP
hook, before the frame walk), so a dropped event costs one env read and one random
draw. Kept events carry ``$sample_rate`` so PostHog can scale counts back up. A value
that isn't a finite number from 0 to 1 falls back to the 0.1 default (no clamping, so a
typo like ``10`` doesn't silently mean "send everything"). ``cli_invoked`` is never
sampled.

Opt out any time:

    export SMALLEST_TELEMETRY_DISABLED=1   # or DO_NOT_TRACK=1, or SMALLESTAI_TELEMETRY=0

or per client: ``SmallestAI(telemetry=False)``. ``sdk_method_called`` is also off
automatically while a pytest test runs (``PYTEST_CURRENT_TEST``) and when ``CI`` is set.
"""

from __future__ import annotations

import json
import math
import os
import platform
import queue
import random
import re
import threading
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# Smallest's platform PostHog project ("New Smallest Inc", US cloud), shared with other
# product analytics; first used by the SDK in 5.10.0 (#93/#95). The phc_ key is
# write-only and meant to ship in client code (allowlisted in .gitleaks.toml).
# SMALLEST_TELEMETRY_KEY / SMALLEST_TELEMETRY_HOST override both, e.g. for a self-hosted
# PostHog or a staging project.
_POSTHOG_HOST = "https://us.i.posthog.com"
_PROJECT_KEY = "phc_vqBpz5cQHFjsmfFix6KuCjf8iwtH2hJaeReHPSq46PyH"
_KEY_ENV = "SMALLEST_TELEMETRY_KEY"
_HOST_ENV = "SMALLEST_TELEMETRY_HOST"
_DISABLE_ENV = "SMALLEST_TELEMETRY_DISABLED"
_SAMPLE_RATE_ENV = "SMALLEST_TELEMETRY_SAMPLE_RATE"
DEFAULT_SAMPLE_RATE = 0.1

_OFF_VALUES = {"0", "false", "no", "off"}
_ON_VALUES = {"1", "true", "yes", "on"}

METHOD_EVENT = "sdk_method_called"
# The only properties an sdk_method_called event may carry. Enforced in
# method_properties() and asserted in tests/custom/test_telemetry_runtime.py.
ALLOWED_METHOD_PROPERTIES = frozenset(
    {"sdk_version", "python_version", "os", "method", "success", "error_type", "http_status", "$sample_rate"}
)
# PostHog processing directives (not data): skip IP-based GeoIP lookup and do not
# create a person profile for the anonymous id.
_POSTHOG_DIRECTIVES = {"$geoip_disable": True, "$process_person_profile": False}

_TIMEOUT_S = 2.0
_QUEUE_MAX = 1000
_BATCH_MAX = 50
_SAFE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]{0,99}$")


def _env_on(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _ON_VALUES


def is_enabled() -> bool:
    """On by default; off with SMALLEST_TELEMETRY_DISABLED=1, DO_NOT_TRACK=1 or SMALLESTAI_TELEMETRY=0."""
    if _env_on(_DISABLE_ENV):
        return False
    if os.getenv("SMALLESTAI_TELEMETRY", "").strip().lower() in _OFF_VALUES:
        return False
    if _env_on("DO_NOT_TRACK"):
        return False
    return True


def _in_test_or_ci() -> bool:
    """True while a pytest test runs, or on a CI runner (CI=true: GitHub Actions, GitLab, CircleCI, ...)."""
    return bool(os.getenv("PYTEST_CURRENT_TEST")) or _env_on("CI")


def runtime_enabled() -> bool:
    """Whether sdk_method_called events may be sent from this process."""
    return is_enabled() and not _in_test_or_ci()


def sample_rate() -> float:
    """Per-call sampling rate: SMALLEST_TELEMETRY_SAMPLE_RATE if it is a finite float in
    [0, 1], else DEFAULT_SAMPLE_RATE (0.1). Never raises."""
    raw = os.getenv(_SAMPLE_RATE_ENV, "").strip()
    if not raw:
        return DEFAULT_SAMPLE_RATE
    try:
        rate = float(raw)
    except (TypeError, ValueError):
        return DEFAULT_SAMPLE_RATE
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        return DEFAULT_SAMPLE_RATE
    return rate


def sampled_rate() -> Optional[float]:
    """Decide whether to keep the next sdk_method_called event.

    Returns the sample rate when the event should be sent (to stamp as ``$sample_rate``),
    or None when telemetry is off or the event is sampled out. Never raises.
    """
    try:
        if not runtime_enabled():
            return None
        rate = sample_rate()
        return rate if random.random() < rate else None
    except Exception:
        return None


def _project_key() -> str:
    return os.getenv(_KEY_ENV, "").strip() or _PROJECT_KEY


def _host() -> str:
    return (os.getenv(_HOST_ENV, "").strip() or _POSTHOG_HOST).rstrip("/")


def _config_dir() -> Path:
    base = os.getenv("XDG_CONFIG_HOME") or os.path.join(str(Path.home()), ".config")
    return Path(base) / "smallestai"


def _state_file() -> Path:
    return _config_dir() / "telemetry.json"


def _read_state() -> Dict[str, Any]:
    try:
        return json.loads(_state_file().read_text())
    except Exception:
        return {}


def _write_state(state: Dict[str, Any]) -> None:
    try:
        _config_dir().mkdir(parents=True, exist_ok=True)
        _state_file().write_text(json.dumps(state))
    except Exception:
        pass


def install_id() -> str:
    """A random anonymous id, persisted once per install. Not tied to any account."""
    state = _read_state()
    iid = state.get("install_id")
    if not iid:
        iid = uuid.uuid4().hex
        state["install_id"] = iid
        _write_state(state)
    return iid


def _sdk_version() -> str:
    try:
        from smallestai.version import __version__

        return __version__
    except Exception:
        return "unknown"


def _base_properties() -> Dict[str, Any]:
    return {
        "sdk_version": _sdk_version(),
        "python_version": platform.python_version(),
        "os": platform.system(),
    }


def maybe_show_first_run_notice() -> None:
    """Print a one-time notice about anonymous telemetry (only if enabled)."""
    if not is_enabled():
        return
    state = _read_state()
    if state.get("notice_shown"):
        return
    state["notice_shown"] = True
    _write_state(state)
    try:
        print(
            "smallestai collects anonymous usage telemetry to improve the SDK "
            "(no personal data or secrets). Opt out with SMALLEST_TELEMETRY_DISABLED=1.",
            flush=True,
        )
    except Exception:
        pass


def _post(event: str, properties: Dict[str, Any]) -> None:
    try:
        import httpx

        payload = {
            "api_key": _project_key(),
            "event": event,
            "distinct_id": install_id(),
            "properties": properties,
        }
        httpx.post(f"{_host()}/capture/", json=payload, timeout=_TIMEOUT_S)
    except Exception:
        pass  # telemetry must never affect the caller


def capture(event: str, properties: Optional[Dict[str, Any]] = None) -> None:
    """Fire-and-forget an anonymous event. Never blocks, never raises, respects opt-out."""
    if not is_enabled():
        return
    props = {**_base_properties(), **(properties or {})}
    threading.Thread(target=_post, args=(event, props), daemon=True).start()


# ---------------------------------------------------------------------------
# sdk_method_called: per-call runtime events, batched on one background thread.
# ---------------------------------------------------------------------------


def _safe_name(value: Optional[str], fallback: str) -> str:
    if isinstance(value, str) and _SAFE_NAME.match(value):
        return value
    return fallback


def _valid_http_status(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 100 <= value <= 599


def method_properties(
    method: str,
    *,
    success: bool,
    error_type: Optional[str] = None,
    http_status: Optional[int] = None,
    sample_rate: Optional[float] = None,
) -> Dict[str, Any]:
    """Build the full property set for one sdk_method_called event. Nothing else is ever added.

    ``http_status`` is kept only on failures, and only when it is a valid HTTP status int
    (i.e. the failure was an HTTP error response, not a transport or client error).
    ``sample_rate`` becomes ``$sample_rate`` when it is a number in (0, 1].
    """
    props: Dict[str, Any] = {
        **_base_properties(),
        "method": _safe_name(method, "unknown"),
        "success": bool(success),
    }
    if not success:
        props["error_type"] = _safe_name(error_type, "Error")
        if _valid_http_status(http_status):
            props["http_status"] = http_status
    if isinstance(sample_rate, (int, float)) and not isinstance(sample_rate, bool) and 0.0 < sample_rate <= 1.0:
        props["$sample_rate"] = float(sample_rate)
    return {k: v for k, v in props.items() if k in ALLOWED_METHOD_PROPERTIES}


def _wire_event(props: Dict[str, Any], distinct_id: str) -> Dict[str, Any]:
    return {
        "event": METHOD_EVENT,
        "distinct_id": distinct_id,
        "properties": {**props, **_POSTHOG_DIRECTIVES},
    }


def _send_batch(batch: List[Dict[str, Any]]) -> None:
    """POST a batch to PostHog's /batch/ endpoint with stdlib urllib. Never raises."""
    try:
        host = _host()
        if not host.startswith(("https://", "http://")):
            return
        distinct_id = install_id()
        body = json.dumps({"api_key": _project_key(), "batch": [_wire_event(p, distinct_id) for p in batch]})
        request = urllib.request.Request(
            f"{host}/batch/",
            data=body.encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=_TIMEOUT_S):  # noqa: S310 - http(s) only, checked above
            pass
    except Exception:
        pass


def _worker(q: "queue.Queue[Dict[str, Any]]") -> None:
    while True:
        try:
            batch = [q.get()]
            while len(batch) < _BATCH_MAX:
                try:
                    batch.append(q.get_nowait())
                except queue.Empty:
                    break
            _send_batch(batch)
        except Exception:
            pass


_queue: "Optional[queue.Queue[Dict[str, Any]]]" = None
_queue_pid: Optional[int] = None
_queue_lock = threading.Lock()
_fork_hook_registered = False


def _reset_after_fork() -> None:
    """Child side of a fork: drop the parent's queue, worker and lock.

    The worker thread does not survive a fork, and the lock may have been held by
    another parent thread at fork time (e.g. gunicorn --preload), so the child gets
    fresh state and starts its own worker on first use.
    """
    global _queue, _queue_pid, _queue_lock
    _queue = None
    _queue_pid = None
    _queue_lock = threading.Lock()


def _register_fork_hook() -> None:
    global _fork_hook_registered
    if _fork_hook_registered:
        return
    _fork_hook_registered = True
    if hasattr(os, "register_at_fork"):  # POSIX only
        os.register_at_fork(after_in_child=_reset_after_fork)


def _get_queue() -> "queue.Queue[Dict[str, Any]]":
    """Lazily start one daemon worker per process (restarted after a fork)."""
    global _queue, _queue_pid
    pid = os.getpid()
    if _queue is None or _queue_pid != pid:
        with _queue_lock:
            _register_fork_hook()
            if _queue is None or _queue_pid != pid:
                q: "queue.Queue[Dict[str, Any]]" = queue.Queue(maxsize=_QUEUE_MAX)
                threading.Thread(target=_worker, args=(q,), name="smallestai-telemetry", daemon=True).start()
                _queue, _queue_pid = q, pid
    return _queue


def record_sampled(
    method: str,
    *,
    sample_rate: float,
    success: bool,
    error_type: Optional[str] = None,
    http_status: Optional[int] = None,
) -> None:
    """Queue an event whose sampling decision was already made with sampled_rate().

    Used by the HTTP hook, which samples before walking frames. Never blocks or raises;
    drops the event if the queue is full.
    """
    try:
        _get_queue().put_nowait(
            method_properties(
                method, success=success, error_type=error_type, http_status=http_status, sample_rate=sample_rate
            )
        )
    except Exception:
        pass


def record_method(
    method: str, *, success: bool, error_type: Optional[str] = None, http_status: Optional[int] = None
) -> None:
    """Sample and queue one sdk_method_called event. O(1) on the caller's thread; never blocks or raises.

    The entry point for anything outside the HTTP hook (e.g. WebSocket clients, helpers).
    Events are dropped (not built or queued) when telemetry is off, when sampled out, and
    when the queue is full.
    """
    rate = sampled_rate()
    if rate is None:
        return
    record_sampled(method, sample_rate=rate, success=success, error_type=error_type, http_status=http_status)
