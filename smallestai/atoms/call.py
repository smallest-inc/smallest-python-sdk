"""
Call management and analytics.

Usage:
    from smallestai.atoms.call import Call
    
    call = Call()
    call.get_calls()
    call.get_call("id")
"""

import os
from typing import Any, Dict, Optional, List
import requests

# Default API base URL
DEFAULT_BASE_URL = "https://atoms.smallest.ai/api/v1"


class Call:
    """
    Manager for call operations and analytics.
    
    Can be used standalone:
        call = Call()
        call.get_calls()
    
    Or via AtomsClient:
        client = AtomsClient()
        client.call.get_calls()
    """
    
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None
    ):
        """
        Initialize Call manager.
        
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
    # Call Analytics
    # =========================================================================
    
    def get_call(self, call_id: str) -> Dict[str, Any]:
        """Get details for a single call."""
        url = f"{self.base_url}/conversation/{call_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_calls(
        self,
        agent_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None,
        call_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated list of calls."""
        url = f"{self.base_url}/conversation"
        params = {"page": page, "limit": limit}
        if agent_id: params["agentIds"] = agent_id
        if campaign_id: params["campaignIds"] = campaign_id
        if status: params["statusFilter"] = status
        if call_type: params["callTypes"] = call_type
        if search: params["search"] = search
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()
    
    def search_calls(self, call_ids: List[str]) -> Dict[str, Any]:
        """Batch search calls by ID."""
        url = f"{self.base_url}/conversation/search"
        response = requests.post(
            url,
            headers=self._get_headers(),
            json={"callIds": call_ids}
        )
        response.raise_for_status()
        return response.json()

    # =========================================================================
    # Post-Call Analytics Configuration
    # =========================================================================
    
    def get_post_call_config(self, agent_id: str) -> Dict[str, Any]:
        """Get post-call analytics config for an agent."""
        url = f"{self.base_url}/agent/{agent_id}/post-call-analytics"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def set_post_call_config(
        self,
        agent_id: str,
        summary_prompt: Optional[str] = None,
        disposition_metrics: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Set post-call analytics config for an agent."""
        url = f"{self.base_url}/agent/{agent_id}/post-call-analytics"
        payload = {}
        if summary_prompt is not None:
            payload["summaryPrompt"] = summary_prompt
        if disposition_metrics is not None:
            payload["dispositionMetrics"] = disposition_metrics
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
