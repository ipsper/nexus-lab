"""
Pytest configuration and fixtures for FastAPI testing
"""
import pytest
import requests
import time
from typing import Generator
from support.api_client import APIClient
from support.k8s_helper import K8sHelper


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "api: API endpoint tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow running tests"
    )
    config.addinivalue_line(
        "markers", "k8s: Kubernetes integration tests (run separately on host)"
    )


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for the FastAPI application via Kong Gateway"""
    # Use host.docker.internal when running in Docker container
    import os
    host = "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"
    return f"http://{host}:8000/api"


@pytest.fixture(scope="session")
def kong_base_url() -> str:
    """Base URL for Kong Gateway"""
    import os
    host = "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"
    return f"http://{host}:8000"


@pytest.fixture(scope="session")
def nexus_base_url() -> str:
    """Base URL for Nexus Repository Manager via Kong Gateway"""
    import os
    host = "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"
    return f"http://{host}:8000/nexus"


@pytest.fixture(scope="session")
def api_client(api_base_url: str) -> Generator[APIClient, None, None]:
    """API client for testing FastAPI endpoints"""
    client = APIClient(api_base_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def kong_client(kong_base_url: str) -> Generator[APIClient, None, None]:
    """API client for testing Kong Gateway"""
    client = APIClient(kong_base_url)
    yield client
    client.close()




@pytest.fixture(scope="session")
def nexus_client(nexus_base_url: str) -> Generator[APIClient, None, None]:
    """API client for testing Nexus Repository Manager"""
    client = APIClient(nexus_base_url)
    yield client
    client.close()


@pytest.fixture(scope="session", autouse=True)
def wait_for_services(api_base_url: str, kong_base_url: str, nexus_base_url: str):
    """Wait for all services to be available before running tests"""
    print("\n🔍 Checking services availability...")
    
    services = [
        ("FastAPI", api_base_url),
        ("Kong Gateway", kong_base_url),
        ("Nexus", nexus_base_url)
    ]
    
    for service_name, url in services:
        max_retries = 10  # Reduced from 30
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code in [200, 404, 502, 503]:  # Accept more status codes
                    print(f"✅ {service_name} is accessible at {url}")
                    break
            except requests.exceptions.RequestException:
                pass
            
            retry_count += 1
            time.sleep(1)  # Reduced from 2
        
        if retry_count >= max_retries:
            print(f"⚠️  {service_name} not immediately available at {url} - tests will continue")


@pytest.fixture
def k8s_helper() -> K8sHelper:
    """Kubernetes helper for testing"""
    return K8sHelper()
