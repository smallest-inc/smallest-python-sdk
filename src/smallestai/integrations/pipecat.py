"""Lazy adapter for the Smallest AI pipecat services.

Re-exports ``pipecat.services.smallest`` under the SDK namespace:

    from smallestai.integrations.pipecat import SmallestSTTService, SmallestTTSService

The core ``smallestai`` package does not depend on pipecat. Install the extra to use
this adapter::

    pip install "smallestai[pipecat]"

Anything the framework plugin exposes is available here; the names simply forward to
``pipecat.services.smallest``.
"""

from __future__ import annotations

import typing

_INSTALL_HINT = 'pip install "smallestai[pipecat]"  (or: pip install "pipecat-ai[smallest]")'


def _load() -> typing.Any:
    try:
        import pipecat.services.smallest as _mod  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - exercised via the missing-dep test
        raise ImportError(
            "The pipecat integration requires pipecat-ai. Install it with:\n    " + _INSTALL_HINT
        ) from exc
    return _mod


def __getattr__(name: str) -> typing.Any:
    module = _load()
    try:
        return getattr(module, name)
    except AttributeError as exc:
        raise AttributeError(f"'pipecat.services.smallest' has no attribute {name!r}") from exc


def __dir__() -> typing.List[str]:
    try:
        return sorted(dir(_load()))
    except ImportError:
        return []
