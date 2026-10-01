"""Read-only-rootfs-safe logging setup for the crew server.

Prod crew pods run with a read-only root filesystem. Anything that tries to
open a file for writing under the pod's working directory (for example a
loguru file sink pointed at ``logs/...``) raises ``OSError: [Errno 30]
Read-only file system`` at import or startup. If that happens on the crew
server's startup path the pod boots dead and refuses every session.

This module centralises logging setup so the crew server never writes to the
pod rootfs by default, and so that if anything (user code, a future sink) does
attempt a file sink that the filesystem rejects, we degrade to stderr instead
of taking the pod down.
"""

from __future__ import annotations

import os
import sys

from loguru import logger

_configured = False


def _log_dir() -> str | None:
    """A writable directory for optional file logging, or None.

    We never assume the current working directory is writable (it is the pod
    rootfs in prod, which is read-only). Honour an explicit override, else fall
    back to $TMPDIR / /tmp, else None (stderr only).
    """
    override = os.getenv("SMALLESTAI_LOG_DIR")
    if override:
        return override
    tmp = os.getenv("TMPDIR") or "/tmp"
    return tmp if os.path.isdir(tmp) else None


def configure_crew_logging() -> None:
    """Point loguru at stderr and make file logging read-only-fs safe.

    Idempotent. Always installs a stderr sink (works on a read-only rootfs).
    A file sink is only added when ``SMALLESTAI_LOG_DIR`` (or a writable
    $TMPDIR) is available AND writable; any OSError while adding it is
    swallowed so a read-only filesystem can never make the pod boot dead.
    """
    global _configured
    if _configured:
        return
    _configured = True

    # Replace loguru's defaults with a single stderr sink. stderr is always
    # writable in a container (captured by `kubectl logs`), and never touches
    # the rootfs.
    logger.remove()
    logger.add(sys.stderr, level=os.getenv("SMALLESTAI_LOG_LEVEL", "INFO"))

    log_dir = _log_dir()
    if not log_dir:
        return
    try:
        os.makedirs(log_dir, exist_ok=True)
        logger.add(
            os.path.join(log_dir, "crew.log"),
            level=os.getenv("SMALLESTAI_LOG_LEVEL", "INFO"),
            rotation="10 MB",
            retention=3,
            enqueue=True,
        )
    except OSError:
        # Read-only filesystem (or no permission). stderr logging already
        # works; a missing file sink must never take the pod down.
        logger.warning(
            "File logging disabled: {} is not writable. Logging to stderr only.",
            log_dir,
        )
