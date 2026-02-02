"""
Campaign management.

Usage:
    from smallestai.atoms.campaign import Campaign
    
    campaign = Campaign()
    campaign.create(name="My Campaign", agent_id="...", audience_id="...", phone_ids=["..."])
    campaign.start(campaign_id)
"""

import os
import requests
from typing import Any, Dict, List, Optional

# Default API base URL
DEFAULT_BASE_URL = "https://atoms.smallest.ai/api/v1"


class Campaign:
    """
    Manager for campaign operations.
    
    Can be used standalone:
        campaign = Campaign()
        campaign.create(...)
    
    Or via AtomsClient:
        client = AtomsClient()
        client.campaign.create(...)
    """
    
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None
    ):
        """
        Initialize Campaign manager.
        
        Args:
            base_url: API base URL (default: atoms.smallest.ai)
            api_key: API key (default: SMALLEST_API_KEY env var)
        """
        self.base_url = base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def create(
        self,
        name: str,
        agent_id: str,
        audience_id: str,
        phone_ids: List[str],
        description: str = "",
        max_retries: int = 3,
        retry_delay: int = 15
    ) -> Dict[str, Any]:
        """Create a new campaign."""
        url = f"{self.base_url}/campaign"
        payload = {
            "name": name,
            "agentId": agent_id,
            "audienceId": audience_id,
            "phoneNumberIds": phone_ids,
            "description": description,
            "maxRetries": max_retries,
            "retryDelay": retry_delay
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    
    def get(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign details."""
        url = f"{self.base_url}/campaign/{campaign_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def list(self, limit: int = 50) -> Dict[str, Any]:
        """List all campaigns."""
        url = f"{self.base_url}/campaign"
        params = {"limit": limit}
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()
    
    def delete(self, campaign_id: str) -> Dict[str, Any]:
        """Delete a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # Campaign Control
    # =========================================================================
    
    def start(self, campaign_id: str) -> Dict[str, Any]:
        """Start a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/start"
        response = requests.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def stop(self, campaign_id: str) -> Dict[str, Any]:
        """Stop a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/stop"
        response = requests.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def pause(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a campaign."""
        url = f"{self.base_url}/campaign/{campaign_id}/pause"
        response = requests.post(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
