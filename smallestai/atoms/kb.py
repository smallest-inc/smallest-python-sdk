"""
Knowledge Base management.

Usage:
    from smallestai.atoms.kb import KB
    
    kb = KB()
    kb.create(name="My KB", description="Company knowledge")
    kb.list()
"""

import os
import requests
from typing import Any, Dict, List, Optional

# Default API base URL
DEFAULT_BASE_URL = "https://atoms.smallest.ai/api/v1"


class KB:
    """
    Manager for Knowledge Base operations.
    
    Can be used standalone:
        kb = KB()
        kb.create(...)
    
    Or via AtomsClient:
        client = AtomsClient()
        client.kb.create(...)
    """
    
    def __init__(
        self,
        base_url: str = None,
        api_key: str = None
    ):
        """
        Initialize KB manager.
        
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
        name: str = None,
        description: str = None,
        file_paths: List[str] = None,
        urls: List[str] = None,
        text: str = None
    ) -> Dict[str, Any]:
        """
        Create a new Knowledge Base.
        
        Args:
            name: KB name
            description: KB description
            file_paths: List of file paths to upload
            urls: List of URLs to scrape
            text: Text content to add
        
        Returns:
            Created KB data
        """
        # Step 1: Create KB Container
        url = f"{self.base_url}/knowledgebase"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        
        payload = {}
        if name: payload["name"] = name
        if description: payload["description"] = description
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        kb_data = response.json()
        
        # Handle response format: {"status": true, "data": "kb_id_string"}
        kb_id = kb_data.get("data")
        if isinstance(kb_id, dict):
            kb_id = kb_id.get("_id")
        
        # Step 2: Upload Files
        if file_paths:
            files_url = f"{self.base_url}/knowledgebase/{kb_id}/items"
            for file_path in file_paths:
                with open(file_path, "rb") as f:
                    file_upload = {"file": f}
                    requests.post(files_url, headers=self._get_headers(), files=file_upload)
        
        # Step 3: Add URLs
        if urls:
            urls_url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-url"
            for u in urls:
                requests.post(urls_url, headers=headers, json={"url": u})
        
        # Step 4: Add Text
        if text:
            text_url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-text"
            requests.post(text_url, headers=headers, json={"text": text})
        
        # Return consistent format
        return {"status": True, "data": {"_id": kb_id}}
    
    def get(self, kb_id: str) -> Dict[str, Any]:
        """Get knowledge base details."""
        url = f"{self.base_url}/knowledgebase/{kb_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def list(self) -> Dict[str, Any]:
        """List all knowledge bases."""
        url = f"{self.base_url}/knowledgebase"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
        
    def delete(self, kb_id: str) -> Dict[str, Any]:
        """Delete a knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # Content Management
    # =========================================================================
    
    def add_file(self, kb_id: str, file_path: str) -> Dict[str, Any]:
        """Add a file to the knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/items"
        with open(file_path, "rb") as f:
            response = requests.post(url, headers=self._get_headers(), files={"file": f})
        response.raise_for_status()
        return response.json()
    
    def add_url(self, kb_id: str, source_url: str) -> Dict[str, Any]:
        """Add a URL to scrape to the knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-url"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, json={"url": source_url})
        response.raise_for_status()
        return response.json()
    
    def add_text(self, kb_id: str, text: str) -> Dict[str, Any]:
        """Add text content to the knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-text"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, json={"text": text})
        response.raise_for_status()
        return response.json()
