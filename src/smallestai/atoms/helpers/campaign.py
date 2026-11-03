"""
Campaign management.

Usage:
    from smallestai.atoms.helpers import Campaign

    campaign = Campaign()
    campaign.create(name="My Campaign", agent_id="...", audience_id="...", from_numbers=["+14155552671"])
    campaign.start(campaign_id)
"""

import os
import warnings
from typing import Any, Dict, List, Optional

import requests

# Default API base URL
DEFAULT_BASE_URL = "https://api.smallest.ai/atoms/v1"
DEFAULT_REQUEST_TIMEOUT = 30.0


class Campaign:
    """
    Manager for campaign operations.

    Can be used standalone:
        campaign = Campaign()
        campaign.create(...)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        *,
        request_timeout: float = DEFAULT_REQUEST_TIMEOUT,
    ):
        """
        Initialize Campaign manager.

        Args:
            base_url: API base URL (default: api.smallest.ai/atoms/v1)
            api_key: API key (default: SMALLEST_API_KEY env var)
            request_timeout: Per-request timeout in seconds
        """
        self.base_url = base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")
        self.request_timeout = request_timeout

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    def create(
        self,
        name: str,
        agent_id: str,
        audience_id: str,
        phone_ids: Optional[List[str]] = None,
        description: str = "",
        max_retries: int = 3,
        retry_delay: int = 15,
        *,
        from_numbers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new campaign.

        Args:
            from_numbers: Caller-ID numbers starting with ``+``. The API rotates
                these across calls and freezes the list at creation. Full E.164
                validation is performed by the server.
            phone_ids: Deprecated phone-number product IDs. Use ``from_numbers``;
                see https://docs.smallest.ai/voice-agents/deprecations/telephony-migration.
                Both fields may be sent; ``from_numbers`` takes precedence.

        At least one of ``from_numbers`` or ``phone_ids`` must be supplied.
        """
        if from_numbers is not None:
            if not isinstance(from_numbers, list) or any(
                not isinstance(number, str) or not number.startswith("+") for number in from_numbers
            ):
                raise ValueError("from_numbers must be a list of non-empty strings starting with '+'")
        if phone_ids is not None:
            warnings.warn(
                "phone_ids is deprecated; use from_numbers instead. "
                "See https://docs.smallest.ai/voice-agents/deprecations/telephony-migration",
                DeprecationWarning,
                stacklevel=2,
            )
        if from_numbers is None and phone_ids is None:
            raise ValueError("Supply from_numbers or phone_ids")
        url = f"{self.base_url}/campaign"
        payload: Dict[str, Any] = {
            "name": name,
            "agentId": agent_id,
            "audienceId": audience_id,
            "description": description,
            "maxRetries": max_retries,
            "retryDelay": retry_delay,
        }
        if from_numbers is not None:
            payload["fromNumbers"] = from_numbers
        if phone_ids is not None:
            payload["phoneNumberIds"] = phone_ids
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=self.request_timeout)  # type: ignore[arg-type]
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def get(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign details."""
        url = f"{self.base_url}/campaign/{campaign_id}"
        response = requests.get(url, headers=self._get_headers(), timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def list(self, limit: int = 50) -> Dict[str, Any]:
        """List all campaigns."""
        url = f"{self.base_url}/campaign"
        params = {"limit": limit}
        response = requests.get(url, headers=self._get_headers(), params=params, timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def delete(self, campaign_id: str) -> Dict[str, Any]:
        """Delete a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}"
        response = requests.delete(url, headers=self._get_headers(), timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    # =========================================================================
    # Campaign Control
    # =========================================================================

    def start(self, campaign_id: str) -> Dict[str, Any]:
        """Start a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/start"
        response = requests.post(url, headers=self._get_headers(), timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def stop(self, campaign_id: str) -> Dict[str, Any]:
        """Stop a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/stop"
        response = requests.post(url, headers=self._get_headers(), timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]

    def pause(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/pause"
        response = requests.post(url, headers=self._get_headers(), timeout=self.request_timeout)
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]
