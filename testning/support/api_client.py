"""
API Client for testing HTTP endpoints
"""
import requests
from typing import Dict, Any, Optional
import json


class APIClient:
    """Simple API client for testing"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get(self, endpoint: str = "", **kwargs) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, timeout=self.timeout, **kwargs)
    
    def post(self, endpoint: str = "", data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if data:
            kwargs['json'] = data
        return self.session.post(url, timeout=self.timeout, **kwargs)
    
    def put(self, endpoint: str = "", data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if data:
            kwargs['json'] = data
        return self.session.put(url, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str = "", **kwargs) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.delete(url, timeout=self.timeout, **kwargs)
    
    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = self.get("/health")
            return response.status_code == 200
        except:
            return False
    
    def close(self):
        """Close the session"""
        self.session.close()
