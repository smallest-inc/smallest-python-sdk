"""Anonymous, opt-out usage telemetry.

Sends lightweight product events (CLI usage, deploy outcomes) to PostHog so we can see
what to improve. It is deliberately minimal and privacy-first:

- NO personal data or secrets: never an API key, agent id, prompt, transcript, phone
  number, file path, or error message. Only the event name, SDK / Python / OS version,
  and a random anonymous install id.
- Geography (country) is derived server-side by PostHog from the request IP; no location
  is ever collected client-side.
- Fire-and-forget on a daemon thread. It never blocks and never raises.

Opt out any time:

    export SMALLESTAI_TELEMETRY=0      # or DO_NOT_TRACK=1
"""
from __future__ import annotations

import json
import os
import platform
import threading
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

# PostHog project (US cloud). The phc_ key is write-only and safe to ship in a client.
_POSTHOG_HOST = "https://us.i.posthog.com"
_PROJECT_KEY = "phc_vqBpz5cQHFjsmfFix6KuCjf8iwtH2hJaeReHPSq46PyH"

_OFF_VALUES = {"0", "false", "no", "off"}
_ON_VALUES = {"1", "true", "yes", "on"}


def is_enabled() -> bool:
    """Telemetry is on by default; disabled by SMALLESTAI_TELEMETRY or DO_NOT_TRACK."""
    if os.getenv("SMALLESTAI_TELEMETRY", "").strip().lower() in _OFF_VALUES:
        return False
    if os.getenv("DO_NOT_TRACK", "").strip().lower() in _ON_VALUES:
        return False
    return True


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
            "(no personal data or secrets). Opt out with SMALLESTAI_TELEMETRY=0.",
            flush=True,
        )
    except Exception:
        pass


def _post(event: str, properties: Dict[str, Any]) -> None:
    try:
        import httpx

        payload = {
            "api_key": _PROJECT_KEY,
            "event": event,
            "distinct_id": install_id(),
            "properties": properties,
        }
        httpx.post(f"{_POSTHOG_HOST}/capture/", json=payload, timeout=2.0)
    except Exception:
        pass  # telemetry must never affect the caller


def capture(event: str, properties: Optional[Dict[str, Any]] = None) -> None:
    """Fire-and-forget an anonymous event. Never blocks, never raises, respects opt-out."""
    if not is_enabled():
        return
    props = {**_base_properties(), **(properties or {})}
    threading.Thread(target=_post, args=(event, props), daemon=True).start()
