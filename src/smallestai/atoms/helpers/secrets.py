"""
Secrets vault.

The org-level, write-only Secrets vault: store API keys and tokens encrypted and
reference them by name from a tool's ``auth`` block. Values are never returned —
``list`` and ``create`` surface the name only.

Usage:
    from smallestai.atoms.helpers import Secrets

    secrets = Secrets()
    secrets.create(name="ORDER_API_TOKEN", value="sk_live_...")
    secrets.list()          # names only
    secrets.delete(secret_id)
"""

import os
from typing import Any, Dict, Optional

import requests

DEFAULT_BASE_URL = "https://api.smallest.ai/atoms/v1"


class Secrets:
    """Manager for the org Secrets vault (``/secret``).

    Standalone:
        secrets = Secrets()
        secrets.list()
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Args:
            base_url: API base URL (default: api.smallest.ai/atoms/v1)
            api_key: API key (default: SMALLEST_API_KEY env var)
        """
        self.base_url = base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list(self) -> Dict[str, Any]:
        """List the org's secret names (values are never returned)."""
        url = f"{self.base_url}/secret"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def create(self, name: str, value: str) -> Dict[str, Any]:
        """Create a secret. The value is encrypted at rest; the response holds the name only.

        Args:
            name: secret name (letters, numbers, underscores) — referenced from a tool's ``auth``.
            value: the secret value (write-only).
        """
        url = f"{self.base_url}/secret"
        response = requests.post(url, headers=self._get_headers(), json={"name": name, "value": value})
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def delete(self, secret_id: str) -> Dict[str, Any]:
        """Delete a secret by its id."""
        url = f"{self.base_url}/secret/{secret_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]
