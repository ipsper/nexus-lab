"""
Basic FastAPI endpoint tests
"""
import pytest
from support.fastapi_support import (
    test_root_endpoint,
    test_health_endpoint,
    test_docs_endpoint,
    test_openapi_endpoint
)


@pytest.mark.api
def test_fastapi_root_endpoint(api_client):
    """Test root endpoint returns 200"""
    test_root_endpoint(api_client)


@pytest.mark.api
def test_fastapi_health_endpoint(api_client):
    """Test health endpoint"""
    test_health_endpoint(api_client)


@pytest.mark.api
def test_fastapi_docs_endpoint(api_client):
    """Test API documentation endpoint"""
    test_docs_endpoint(api_client)


@pytest.mark.api
def test_fastapi_openapi_endpoint(api_client):
    """Test OpenAPI schema endpoint"""
    test_openapi_endpoint(api_client)
