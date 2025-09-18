"""
Basic FastAPI endpoint tests
"""
import pytest


@pytest.mark.api
def test_fastapi_root_endpoint(api_client):
    """Test root endpoint returns 200"""
    response = api_client.get("/")
    assert response.status_code == 200


@pytest.mark.api
def test_fastapi_health_endpoint(api_client):
    """Test health endpoint"""
    response = api_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.api
def test_fastapi_docs_endpoint(api_client):
    """Test API documentation endpoint"""
    response = api_client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.api
def test_fastapi_openapi_endpoint(api_client):
    """Test OpenAPI schema endpoint"""
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Nexus Repository Manager API"
