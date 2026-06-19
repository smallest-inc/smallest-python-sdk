"""
Response-envelope helpers (Atoms) — issue #25.

The Atoms wire API returns the `data` field in three different shapes:

* **create** → `data` is a bare id string
* **get**    → `data` is the full resource object
* **list**   → `data` wraps a per-resource array (e.g. `agents`, `logs`,
               `records`, `items`) plus pagination fields

These helpers give callers ONE predictable shape so code (and AI-generated
code) doesn't have to special-case each endpoint. They are intentionally thin
and side-effect-free, and live in a `.fernignore`-preserved file so they
survive regeneration. When the backend standardizes the envelope
(SPEC_FROM_CODE_MIGRATION workstream 1), these become no-ops and can be removed.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional

# Per-resource keys the list endpoints use to hold the array.
_LIST_KEYS = (
    "agents",
    "logs",
    "records",
    "items",
    "templates",
    "numbers",
    "phone_numbers",
    "campaigns",
    "members",
    "versions",
    "drafts",
    "knowledge_bases",
)


@dataclass
class Page:
    """Normalized list result: the items plus whatever pagination is available."""

    items: List[Any] = field(default_factory=list)
    total_count: Optional[int] = None
    total_pages: Optional[int] = None
    has_more: Optional[bool] = None


def _get(obj: Any, name: str) -> Any:
    """Attribute- or key-based access (works for pydantic models and dicts)."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def as_page(response: Any) -> Page:
    """Normalize any Atoms *list* response into a :class:`Page`.

    Accepts the raw SDK response (uses its ``.data``) or a ``data`` payload
    directly. Finds the array under any known per-resource key and surfaces
    pagination from either flat fields (``total_count``/``has_more``) or a
    nested ``pagination`` object.
    """
    data = _get(response, "data")
    if data is None:
        data = response

    if isinstance(data, list):
        return Page(items=list(data))

    pagination = _get(data, "pagination")
    for key in _LIST_KEYS:
        items = _get(data, key)
        if items is not None:
            return Page(
                items=list(items),
                total_count=(_get(data, "total_count") or _get(data, "total") or _get(data, "count")
                             or _get(pagination, "total") or _get(pagination, "total_count")),
                total_pages=_get(data, "total_pages") or _get(pagination, "total_pages"),
                has_more=(_get(data, "has_more") if _get(data, "has_more") is not None
                          else _get(pagination, "has_more")),
            )

    # Unknown shape — return the payload as a single-item page rather than guessing.
    return Page(items=[data])


def require_id(value: Optional[str], name: str = "id") -> str:
    """Guard against empty identifiers (issue #18).

    The generated ``get_*`` methods build ``GET /resource/`` for an empty id,
    which silently hits the *list* endpoint. Call this first to fail loudly.
    """
    if value is None or not str(value).strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value
