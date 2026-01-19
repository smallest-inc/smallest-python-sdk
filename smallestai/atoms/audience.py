"""
Audience management.

Usage:
    from smallestai.atoms.audience import Audience
    
    audience = Audience()
    audience.create(name="My Audience", phone_numbers=["+1234567890"])
    audience.list()
"""

import io
import os
import requests
from typing import Any, Dict, List, Optional, Tuple

# Default API base URL
DEFAULT_BASE_URL = "https://atoms.smallest.ai/api/v1"


class Audience:
    """
    Manager for audience operations.
    
    Can be used standalone:
        audience = Audience()
        audience.create(...)
    
    Or via AtomsClient:
        client = AtomsClient()
        client.audience.create(...)
    """
    
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None
    ):
        """
        Initialize Audience manager.
        
        Args:
            base_url: API base URL (default: atoms.smallest.ai)
            api_key: API key (default: SMALLEST_API_KEY env var)
        """
        self.base_url = base_url or os.environ.get("SMALLEST_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("SMALLEST_API_KEY", "")
    
    def _get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}
    
    # =========================================================================
    # CRUD Operations
    # =========================================================================
    
    def create(
        self,
        name: str,
        phone_numbers: List[str],
        names: Optional[List[Tuple[str, str]]] = None,
        description: str = "",
        phone_number_column_name: str = "phoneNumber"
    ) -> Dict[str, Any]:
        """
        Create a new audience.
        
        Args:
            name: Audience name
            phone_numbers: List of phone numbers
            names: Optional list of (firstName, lastName) tuples
            description: Optional description
            phone_number_column_name: Column name for phone in CSV
            
        Returns:
            Dict with audience data including _id
        """
        url = f"{self.base_url}/audience"
        
        # Build CSV content (format: firstName,lastName,phoneNumber)
        csv_lines = ["firstName,lastName,phoneNumber"]
        for i, phone in enumerate(phone_numbers):
            if names and i < len(names):
                first_name, last_name = names[i]
            else:
                first_name, last_name = "User", str(i + 1)
            csv_lines.append(f"{first_name},{last_name},{phone}")
        
        csv_content = "\n".join(csv_lines)
        
        files = {'file': ('contacts.csv', csv_content.encode('utf-8'), 'text/csv')}
        data = {
            'name': name,
            'phoneNumberColumnName': phone_number_column_name,
            'description': description
        }
        
        response = requests.post(url, headers=self._get_headers(), files=files, data=data)
        response.raise_for_status()
        return response.json()
    
    def get(self, audience_id: str) -> Dict[str, Any]:
        """Get audience details."""
        url = f"{self.base_url}/audience/{audience_id}"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_members(
        self,
        audience_id: str,
        page: int = 1,
        offset: int = 10,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get audience members."""
        url = f"{self.base_url}/audience/{audience_id}/members"
        params = {"page": page, "offset": offset}
        if search: params["search"] = search
        
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def list(self) -> Dict[str, Any]:
        """List all audiences."""
        url = f"{self.base_url}/audience"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def delete(self, audience_id: str) -> Dict[str, Any]:
        """Delete an audience."""
        url = f"{self.base_url}/audience/{audience_id}"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # Contact Management
    # =========================================================================
        
    def add_contacts(
        self,
        audience_id: str,
        phone_numbers: List[str],
        names: Optional[List[Tuple[str, str]]] = None
    ) -> Dict[str, Any]:
        """Add contacts to audience."""
        url = f"{self.base_url}/audience/{audience_id}/members"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        
        # Build members list
        members = []
        for i, phone in enumerate(phone_numbers):
            member = {"phoneNumber": phone}
            if names and i < len(names):
                member["firstName"] = names[i][0]
                member["lastName"] = names[i][1]
            else:
                member["firstName"] = "User"
                member["lastName"] = str(i + 1)
            members.append(member)
        
        response = requests.post(url, headers=headers, json={"members": members})
        response.raise_for_status()
        return response.json()
