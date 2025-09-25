"""
Basic FastAPI endpoint tests - Grundläggande API-funktionalitet
"""
import pytest
import time


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_root_endpoint(api_client):
    """Test root endpoint returns correct welcome message"""
    response = api_client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "Välkommen till Nexus Repository Manager API" in data["message"]
    assert "version" in data
    assert "docs" in data
    assert "health" in data


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_health_endpoint(api_client):
    """Test health endpoint returns correct status"""
    response = api_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "environment" in data


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_docs_endpoint(api_client):
    """Test API documentation endpoint"""
    response = api_client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "swagger" in response.text.lower()


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_openapi_endpoint(api_client):
    """Test OpenAPI schema endpoint"""
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
    assert "components" in data
    assert data["info"]["title"] == "Nexus Repository Manager API"


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_stats_endpoint(api_client):
    """Test stats endpoint returns repository statistics"""
    response = api_client.get("/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_repositories" in data
    assert "total_packages" in data
    assert "active_repositories" in data
    assert "packages_by_repository" in data
    
    # Verifiera att data är av rätt typ
    assert isinstance(data["total_repositories"], int)
    assert isinstance(data["total_packages"], int)
    assert isinstance(data["active_repositories"], int)
    assert isinstance(data["packages_by_repository"], dict)


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_formats_endpoint(api_client):
    """Test formats endpoint returns supported formats"""
    response = api_client.get("/formats")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "supported_formats" in data
    assert "format_info" in data
    
    # Kontrollera att supported_formats är en lista
    supported_formats = data["supported_formats"]
    assert isinstance(supported_formats, list)
    assert len(supported_formats) > 0
    
    # Verifiera att viktiga formats finns
    expected_formats = ["pypi", "apt", "rpm", "docker"]
    for format_name in expected_formats:
        assert any(format_name in str(item) for item in supported_formats), f"Format {format_name} not found in response"


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_config_endpoint(api_client):
    """Test config endpoint returns configuration"""
    response = api_client.get("/config")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    
    # Verifiera att viktiga config-nycklar finns
    expected_keys = ["nexus_url", "api_version", "supported_formats"]
    for key in expected_keys:
        assert key in data, f"Config key {key} not found in response"


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_pip_package_endpoint(api_client):
    """Test pip-package endpoint returns pip package information"""
    response = api_client.get("/pip-package")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    
    # Verifiera att pip-paket information finns
    expected_keys = ["name", "version", "description", "repository_url"]
    for key in expected_keys:
        assert key in data, f"Pip package key {key} not found in response"


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_repositories_list_endpoint(api_client):
    """Test repositories list endpoint returns all repositories"""
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0, "No repositories found"
    
    # Verifiera att varje repository har rätt struktur
    for repo in data:
        assert "name" in repo
        assert "type" in repo
        assert "format" in repo
        assert "url" in repo
        assert "status" in repo
        
        # Verifiera att status är "active"
        assert repo["status"] == "active", f"Repository {repo['name']} is not active"


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_repositories_specific_endpoint(api_client):
    """Test specific repository endpoint"""
    # Hämta lista över repositories först
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    
    repositories = response.json()
    assert len(repositories) > 0, "No repositories available for testing"
    
    # Testa första repository
    first_repo = repositories[0]
    repo_name = first_repo["name"]
    
    response = api_client.get(f"/repositories/{repo_name}")
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    assert data["name"] == repo_name
    assert "type" in data
    assert "format" in data
    assert "url" in data
    assert "status" in data


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_packages_list_endpoint(api_client):
    """Test packages list endpoint"""
    response = api_client.get("/packages/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    
    # För en ny installation kan listan vara tom
    # Detta är OK, vi testar bara att endpoint svarar


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_repository_packages_endpoint(api_client):
    """Test repository packages endpoint"""
    # Hämta lista över repositories först
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    
    repositories = response.json()
    assert len(repositories) > 0, "No repositories available for testing"
    
    # Testa första repository
    first_repo = repositories[0]
    repo_name = first_repo["name"]
    
    response = api_client.get(f"/repositories/{repo_name}/packages")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    
    # För en ny installation kan listan vara tom
    # Detta är OK, vi testar bara att endpoint svarar


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_response_headers(api_client):
    """Test that API returns correct headers"""
    response = api_client.get("/health")
    assert response.status_code == 200
    
    # Verifiera att Content-Type är JSON
    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.api
@pytest.mark.basic
def test_fastapi_response_times(api_client):
    """Test that API responses are reasonably fast"""
    endpoints_to_test = [
        "/",
        "/health",
        "/stats",
        "/repositories/",
        "/packages/"
    ]
    
    max_response_time = 2.0  # 2 sekunder max
    
    for endpoint in endpoints_to_test:
        start_time = time.time()
        response = api_client.get(endpoint)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"
        assert response_time < max_response_time, f"Endpoint {endpoint} took {response_time:.2f}s (max: {max_response_time}s)"
