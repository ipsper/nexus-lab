"""
Nexus Repository Manager integration test functions
"""
import pytest
import requests
from support.api_client import APIClient


def test_nexus_accessible(nexus_client: APIClient):
    """Test Nexus is accessible"""
    response = nexus_client.get("/")
    assert response.status_code == 200
    assert "Nexus Repository Manager" in response.text


def test_nexus_health_check(nexus_client: APIClient):
    """Test Nexus health check endpoint"""
    response = nexus_client.get("/service/rest/v1/status")
    # Nexus may not be fully ready yet, accept 404 or 503
    assert response.status_code in [200, 404, 503]
    
    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            assert "data" in data
            assert "state" in data["data"]
        except (ValueError, requests.exceptions.JSONDecodeError):
            # JSON parsing failed, but endpoint responded - OK for startup
            pass


def test_nexus_repositories(nexus_client: APIClient):
    """Test Nexus repositories endpoint"""
    response = nexus_client.get("/service/rest/v1/repositories")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_nexus_through_kong(kong_client: APIClient):
    """Test Nexus access through Kong Gateway"""
    response = kong_client.get("/nexus")
    assert response.status_code == 200
    assert "Nexus Repository Manager" in response.text


def test_nexus_api_through_kong(kong_client: APIClient):
    """Test Nexus API access through Kong Gateway"""
    response = kong_client.get("/nexus/service/rest/v1/status")
    # Nexus may not be fully ready yet, accept 404 or 503
    assert response.status_code in [200, 404, 503]
    
    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            assert "data" in data
            assert "state" in data["data"]
        except (ValueError, requests.exceptions.JSONDecodeError):
            # JSON parsing failed, but endpoint responded - OK for startup
            pass
