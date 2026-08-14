"""Startup banner for the smallestai CLI.

Concentric rings (left-aligned, gently pulsing) above the SMALLEST AI wordmark,
in the brand blue #3B82F6. The pulse only runs on an interactive TTY; piped,
CI, NO_COLOR, or SMALLESTAI_NO_ANIM output gets a single static frame. Narrow
terminals fall back to a compact text wordmark so nothing wraps.
"""

from __future__ import annotations

import math
import os
import shutil
import sys
import time

_BRAND = (59, 130, 246)  # #3B82F6

_WORDMARK = [
    r"███████╗███╗   ███╗ █████╗ ██╗     ██╗     ███████╗███████╗████████╗     █████╗ ██╗",
    r"██╔════╝████╗ ████║██╔══██╗██║     ██║     ██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗██║",
    r"███████╗██╔████╔██║███████║██║     ██║     █████╗  ███████╗   ██║       ███████║██║",
    r"╚════██║██║╚██╔╝██║██╔══██║██║     ██║     ██╔══╝  ╚════██║   ██║       ██╔══██║██║",
    r"███████║██║ ╚═╝ ██║██║  ██║███████╗███████╗███████╗███████║   ██║       ██║  ██║██║",
    r"╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝   ╚═╝       ╚═╝  ╚═╝╚═╝",
]
_WORDMARK_WIDTH = 83
_INDENT = "  "
_MIN_WIDTH = _WORDMARK_WIDTH + 4  # leave a little breathing room

_TAGLINE = "Build, deploy, and run voice agents and speech models."

# Braille rasterisation: 2x4 dots per glyph, mapped to the Unicode braille block.
_BR = [0x1, 0x2, 0x4, 0x40, 0x8, 0x10, 0x20, 0x80]
_OFF = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
_RING_COLS, _RING_ROWS = 16, 7
_BASE_RADII = (1.0, 0.62, 0.26)

_RESET = "\033[0m"
_HIDE = "\033[?25l"
_SHOW = "\033[?25h"


def _fg(rgb: tuple[int, int, int]) -> str:
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def _rings(radii: tuple[float, ...], thick: float = 0.045) -> list[str]:
    cols, rows = _RING_COLS, _RING_ROWS
    w, h = cols * 2, rows * 4
    cx, cy = (w - 1) / 2, (h - 1) / 2
    rr = min(cx, cy)
    grid = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            d = math.hypot((x - cx) / rr, (y - cy) / rr)
            if any(abs(d - r) < thick for r in radii):
                grid[y][x] = 1
    lines = []
    for r in range(rows):
        line = "".join(
            chr(0x2800 + sum(_BR[i] for i, (a, b) in enumerate(_OFF) if grid[r * 4 + b][c * 2 + a])) or " "
            for c in range(cols)
        )
        lines.append(line)
    return lines


def _pulse_radii(t: float) -> tuple[float, ...]:
    s = 0.28 * math.sin(t * 2 * math.pi)
    return tuple(min(1.02, r + s) for r in _BASE_RADII)


def _color_enabled() -> bool:
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _animate_enabled() -> bool:
    return (
        sys.stdout.isatty()
        and not os.environ.get("NO_COLOR")
        and not os.environ.get("CI")
        and not os.environ.get("SMALLESTAI_NO_ANIM")
    )


def _term_width() -> int:
    try:
        return shutil.get_terminal_size((80, 24)).columns
    except Exception:
        return 80


def print_banner() -> None:
    """Render the rings + wordmark to stdout (animated on an interactive TTY)."""
    color = _color_enabled()
    blue = _fg(_BRAND) if color else ""
    reset = _RESET if color else ""
    out = sys.stdout

    if _term_width() < _MIN_WIDTH:
        out.write(f"\n{_INDENT}{blue}SMALLEST AI{reset}\n")
        out.flush()
        return

    ring_static = _rings(_BASE_RADII)

    if _animate_enabled():
        out.write(_HIDE)
        try:
            for line in ring_static:
                out.write(f"{_INDENT}{blue}{line}{reset}\n")
            fps = 20
            for f in range(1, int(1.2 * fps) + 1):
                out.write(f"\033[{_RING_ROWS}A")
                for line in _rings(_pulse_radii(f / fps)):
                    out.write(f"\r{_INDENT}{blue}{line}{reset}\033[K\n")
                out.flush()
                time.sleep(1 / fps)
            out.write(f"\033[{_RING_ROWS}A")
            for line in ring_static:
                out.write(f"\r{_INDENT}{blue}{line}{reset}\033[K\n")
        finally:
            out.write(_SHOW + reset)
    else:
        for line in ring_static:
            out.write(f"{_INDENT}{blue}{line}{reset}\n")

    out.write("\n")
    for w in _WORDMARK:
        out.write(f"{_INDENT}{blue}{w}{reset}\n")
    out.flush()
