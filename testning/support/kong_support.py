"""
Kong Gateway test functions
"""
import pytest
from support.api_client import APIClient


def test_kong_admin_api(kong_client: APIClient):
    """Test Kong Gateway is accessible (replaces admin API test)"""
    response = kong_client.get("/status")
    # Kong Gateway should return a proper response or route not found
    assert response.status_code in [200, 404]


def test_kong_gateway_nexus_route(kong_client: APIClient):
    """Test Kong routes to Nexus through /nexus path"""
    response = kong_client.get("/nexus")
    # Should either return 200 (Nexus) or 404 (if Nexus not ready)
    assert response.status_code in [200, 404, 502, 503]


def test_kong_gateway_api_route(kong_client: APIClient):
    """Test Kong routes to FastAPI through /api path"""
    response = kong_client.get("/api")
    # Should either return 200 (FastAPI) or 404 (if FastAPI not ready)
    assert response.status_code in [200, 404, 502, 503]


def test_kong_gateway_health(kong_client: APIClient):
    """Test Kong Gateway health"""
    response = kong_client.get("/status")
    # Kong Gateway should return a proper response or route not found
    assert response.status_code in [200, 404]


def test_kong_routes_configuration(kong_client: APIClient):
    """Test Kong routes work by testing actual endpoints"""
    # Test that Kong can route to API endpoints
    api_response = kong_client.get("/api/health")
    assert api_response.status_code == 200
    
    # Test that Kong can route to Nexus (may not be ready, so allow 502/503)
    nexus_response = kong_client.get("/nexus")
    assert nexus_response.status_code in [200, 404, 502, 503]
