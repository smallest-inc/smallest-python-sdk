"""Lazy adapter for the Smallest AI LiveKit plugin.

Re-exports ``livekit.plugins.smallestai`` under the SDK namespace:

    from smallestai.integrations.livekit import TTS

The core ``smallestai`` package does not depend on LiveKit. Install the extra to use
this adapter::

    pip install "smallestai[livekit]"

Anything the framework plugin exposes is available here; the names forward to
``livekit.plugins.smallestai``.
"""

from __future__ import annotations

import typing

_INSTALL_HINT = 'pip install "smallestai[livekit]"  (or: pip install livekit-plugins-smallestai)'


def _load() -> typing.Any:
    try:
        import livekit.plugins.smallestai as _mod  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - exercised via the missing-dep test
        raise ImportError(
            "The livekit integration requires livekit-plugins-smallestai. Install it with:\n    " + _INSTALL_HINT
        ) from exc
    return _mod


def __getattr__(name: str) -> typing.Any:
    module = _load()
    try:
        return getattr(module, name)
    except AttributeError as exc:
        raise AttributeError(f"'livekit.plugins.smallestai' has no attribute {name!r}") from exc


def __dir__() -> typing.List[str]:
    try:
        return sorted(dir(_load()))
    except ImportError:
        return []
