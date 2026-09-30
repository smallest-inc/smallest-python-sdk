# Hand-maintained (see .fernignore). Kept out of regeneration to append an
# actionable hint to error messages (auth / permission / plan-gated). Re-apply
# the __str__ enrichment after a regen.

from typing import Any, Dict, Optional


class ApiError(Exception):
    headers: Optional[Dict[str, str]]
    status_code: Optional[int]
    body: Any

    def __init__(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        status_code: Optional[int] = None,
        body: Any = None,
    ) -> None:
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        base = f"status_code: {self.status_code}, body: {self.body}"
        # Local import keeps the error module dependency-light and avoids cycles.
        from ._error_hints import hint_for

        hint = hint_for(self.status_code, self.body)
        return f"{base}\n{hint}" if hint else base
