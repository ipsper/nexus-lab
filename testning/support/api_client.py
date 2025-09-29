"""
API Client for testing HTTP endpoints
"""
import httpx
from typing import Dict, Any, Optional
import json


class APIClient:
    """Simple API client for testing"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.Client(
            timeout=timeout,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
    
    def get(self, endpoint: str = "", **kwargs) -> httpx.Response:
        """GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.get(url, **kwargs)
    
    def post(self, endpoint: str = "", data: Optional[Dict[str, Any]] = None, **kwargs) -> httpx.Response:
        """POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if data:
            kwargs['json'] = data
        return self.client.post(url, **kwargs)
    
    def put(self, endpoint: str = "", data: Optional[Dict[str, Any]] = None, **kwargs) -> httpx.Response:
        """PUT request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if data:
            kwargs['json'] = data
        return self.client.put(url, **kwargs)
    
    def delete(self, endpoint: str = "", **kwargs) -> httpx.Response:
        """DELETE request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.client.delete(url, **kwargs)
    
    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = self.get("/health")
            return response.status_code == 200
        except:
            return False
    
    def close(self):
        """Close the client"""
        self.client.close()
