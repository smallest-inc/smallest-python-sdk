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
            file_paths: List of PDF file paths to upload
            urls: List of URLs to scrape
            text: Text content (may not be available via API yet)
        
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
        
        # Step 2: Upload PDF Files
        if file_paths:
            for file_path in file_paths:
                self.add_file(kb_id, file_path)
        
        # Step 3: Scrape URLs
        if urls:
            self.scrape_urls(kb_id, urls)
        
        # Step 4: Add text (may not be available yet)
        if text:
            self.add_text(kb_id, text)
        
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
    
    def get_items(self, kb_id: str) -> Dict[str, Any]:
        """Get all items in a knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/items"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def delete_item(self, kb_id: str, item_id: str) -> Dict[str, Any]:
        """Delete an item from a knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/items/{item_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # =========================================================================
    # Content Management
    # =========================================================================
    
    def add_file(self, kb_id: str, file_path: str) -> Dict[str, Any]:
        """
        Add a PDF file to the knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            file_path: Path to PDF file
            
        Returns:
            Upload response
            
        Note:
            Only PDF files are supported.
        """
        url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-media"
        
        with open(file_path, "rb") as f:
            files = {"media": (os.path.basename(file_path), f, "application/pdf")}
            response = requests.post(url, headers=self._get_headers(), files=files)
        
        response.raise_for_status()
        return response.json()
    
    def scrape_urls(self, kb_id: str, urls: List[str]) -> Dict[str, Any]:
        """
        Scrape URLs and add content to knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            urls: List of URLs to scrape
            
        Returns:
            Scrape response
        """
        url = f"{self.base_url}/knowledgebase/{kb_id}/scrape-urls"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        
        response = requests.post(url, headers=headers, json={"urls": urls})
        response.raise_for_status()
        return response.json()
    
    def get_scraped_urls(self, kb_id: str) -> Dict[str, Any]:
        """Get all scraped URLs for a knowledge base."""
        url = f"{self.base_url}/knowledgebase/{kb_id}/scraped-urls"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Deprecated/legacy methods
    def add_url(self, kb_id: str, source_url: str) -> Dict[str, Any]:
        """
        DEPRECATED: Use scrape_urls() instead.
        """
        return self.scrape_urls(kb_id, [source_url])
    
    def add_text(self, kb_id: str, text: str) -> Dict[str, Any]:
        """
        Add text content to knowledge base.
        
        Note: This endpoint may not be available yet.
        If it fails, use the dashboard to add text content.
        """
        url = f"{self.base_url}/knowledgebase/{kb_id}/items/upload-text"
        headers = self._get_headers()
        headers["Content-Type"] = "application/json"
        
        response = requests.post(url, headers=headers, json={"text": text})
        if response.status_code == 404:
            print("Warning: Text upload API not available. Use dashboard instead.")
            return {"status": False, "error": "Text upload not available via API"}
        
        response.raise_for_status()
        return response.json()
