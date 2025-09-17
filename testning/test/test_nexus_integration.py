"""
Nexus Repository Manager integration tests
"""
import pytest
from support.nexus_support import (
    test_nexus_accessible,
    test_nexus_health_check,
    test_nexus_repositories,
    test_nexus_through_kong,
    test_nexus_api_through_kong
)


@pytest.mark.integration
@pytest.mark.slow
def test_nexus_accessible_endpoint(nexus_client):
    """Test Nexus is accessible"""
    test_nexus_accessible(nexus_client)


@pytest.mark.integration
@pytest.mark.slow
def test_nexus_health_check_endpoint(nexus_client):
    """Test Nexus health check endpoint"""
    test_nexus_health_check(nexus_client)


@pytest.mark.integration
@pytest.mark.slow
def test_nexus_repositories_endpoint(nexus_client):
    """Test Nexus repositories endpoint"""
    test_nexus_repositories(nexus_client)


@pytest.mark.integration
@pytest.mark.slow
def test_nexus_through_kong_endpoint(kong_client):
    """Test Nexus access through Kong Gateway"""
    test_nexus_through_kong(kong_client)


@pytest.mark.integration
@pytest.mark.slow
def test_nexus_api_through_kong_endpoint(kong_client):
    """Test Nexus API access through Kong Gateway"""
    test_nexus_api_through_kong(kong_client)
