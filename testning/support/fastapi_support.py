"""
FastAPI Basic test functions
"""
import pytest
from support.api_client import APIClient


def test_root_endpoint(api_client: APIClient):
    """Test root endpoint returns 200"""
    response = api_client.get("/")
    assert response.status_code == 200


def test_health_endpoint(api_client: APIClient):
    """Test health endpoint"""
    response = api_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_docs_endpoint(api_client: APIClient):
    """Test API documentation endpoint"""
    response = api_client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_openapi_endpoint(api_client: APIClient):
    """Test OpenAPI schema endpoint"""
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Nexus Repository Manager API"
