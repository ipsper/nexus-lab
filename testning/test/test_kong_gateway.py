"""
Kong Gateway integration tests
"""
import pytest
from support.kong_support import (
    test_kong_admin_api,
    test_kong_gateway_nexus_route,
    test_kong_gateway_api_route,
    test_kong_gateway_health,
    test_kong_routes_configuration
)


@pytest.mark.integration
def test_kong_admin_api_endpoint(kong_client):
    """Test Kong Gateway is accessible"""
    test_kong_admin_api(kong_client)


@pytest.mark.integration
def test_kong_gateway_nexus_route_endpoint(kong_client):
    """Test Kong routes to Nexus through /nexus path"""
    test_kong_gateway_nexus_route(kong_client)


@pytest.mark.integration
def test_kong_gateway_api_route_endpoint(kong_client):
    """Test Kong routes to FastAPI through /api path"""
    test_kong_gateway_api_route(kong_client)


@pytest.mark.integration
def test_kong_gateway_health_endpoint(kong_client):
    """Test Kong Gateway health"""
    test_kong_gateway_health(kong_client)


@pytest.mark.integration
def test_kong_routes_configuration_endpoint(kong_client):
    """Test Kong routes are properly configured"""
    test_kong_routes_configuration(kong_client)
