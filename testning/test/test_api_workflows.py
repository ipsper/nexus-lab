"""
API End-to-End Tests - Testar kompletta arbetsflöden
"""
import pytest
import requests
import time


@pytest.mark.api
@pytest.mark.workflows
def test_complete_repository_workflow(api_client):
    """Test complete repository management workflow"""
    # Steg 1: Lista befintliga repositories
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    initial_repos = response.json()
    initial_count = len(initial_repos)
    
    # Steg 2: Hämta statistik
    response = api_client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_repositories" in stats
    assert stats["total_repositories"] == initial_count
    
    # Steg 3: Testa att hämta specifika repositories
    for repo in initial_repos:
        repo_name = repo["name"]
        response = api_client.get(f"/repositories/{repo_name}")
        assert response.status_code == 200
        
        repo_data = response.json()
        assert repo_data["name"] == repo_name
        assert repo_data["status"] == "active"
    
    # Steg 4: Testa packages (alla paket)
    response = api_client.get("/packages/")
    assert response.status_code == 200
    
    packages = response.json()
    assert isinstance(packages, list)
    
    # Steg 5: Verifiera att statistik är konsistent
    response = api_client.get("/stats")
    assert response.status_code == 200
    final_stats = response.json()
    assert final_stats["total_repositories"] == initial_count


@pytest.mark.api
@pytest.mark.workflows
def test_api_health_monitoring_workflow(api_client):
    """Test API health monitoring workflow"""
    # Steg 1: Kontrollera grundläggande health
    response = api_client.get("/health")
    assert response.status_code == 200
    
    health_data = response.json()
    assert health_data["status"] == "healthy"
    assert "timestamp" in health_data
    assert "version" in health_data
    assert "environment" in health_data
    
    # Steg 2: Kontrollera att health är konsistent över tid
    time.sleep(1)  # Vänta 1 sekund
    
    response = api_client.get("/health")
    assert response.status_code == 200
    
    new_health_data = response.json()
    assert new_health_data["status"] == "healthy"
    assert new_health_data["version"] == health_data["version"]
    assert new_health_data["environment"] == health_data["environment"]
    
    # Timestamp ska vara olika
    assert new_health_data["timestamp"] != health_data["timestamp"]


@pytest.mark.api
@pytest.mark.workflows
def test_api_documentation_workflow(api_client):
    """Test API documentation workflow"""
    # Steg 1: Hämta OpenAPI spec
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    
    openapi_spec = response.json()
    assert "openapi" in openapi_spec
    assert "info" in openapi_spec
    assert "paths" in openapi_spec
    
    # Steg 2: Verifiera att alla dokumenterade endpoints finns
    documented_paths = list(openapi_spec["paths"].keys())
    expected_paths = [
        "/",
        "/health",
        "/stats",
        "/formats",
        "/config",
        "/pip-package",
        "/repositories/",
        "/packages/"
    ]
    
    for expected_path in expected_paths:
        assert expected_path in documented_paths, f"Path {expected_path} not documented"
    
    # Steg 3: Testa att dokumenterade endpoints fungerar
    for path in documented_paths:
        if path.endswith("/"):
            # Lista endpoints
            response = api_client.get(path)
            assert response.status_code == 200
        elif "{" in path:
            # Parameterized endpoints - testa med dummy data
            if "/repositories/" in path and "/packages" in path:
                # Testa med befintligt repository
                repos_response = api_client.get("/repositories/")
                if repos_response.status_code == 200:
                    repos = repos_response.json()
                    if repos:
                        repo_name = repos[0]["name"]
                        test_path = path.replace("{repository_name}", repo_name)
                        response = api_client.get(test_path)
                        assert response.status_code in [200, 404]  # 404 OK för tomma listor
            elif "/repositories/" in path:
                # Testa med befintligt repository
                repos_response = api_client.get("/repositories/")
                if repos_response.status_code == 200:
                    repos = repos_response.json()
                    if repos:
                        repo_name = repos[0]["name"]
                        test_path = path.replace("{repository_name}", repo_name)
                        response = api_client.get(test_path)
                        assert response.status_code == 200
            elif "/packages/" in path:
                # Testa med dummy package name
                test_path = path.replace("{package_name}", "test-package")
                response = api_client.get(test_path)
                assert response.status_code in [200, 404]  # 404 OK för icke-existerande paket


@pytest.mark.api
@pytest.mark.workflows
def test_api_configuration_workflow(api_client):
    """Test API configuration workflow"""
    # Steg 1: Hämta konfiguration
    response = api_client.get("/config")
    assert response.status_code == 200
    
    config = response.json()
    assert isinstance(config, dict)
    
    # Steg 2: Hämta formats
    response = api_client.get("/formats")
    assert response.status_code == 200
    
    formats = response.json()
    assert isinstance(formats, dict)
    assert "supported_formats" in formats
    assert "format_info" in formats
    
    # Steg 3: Verifiera att formats är konsistent med config
    if "supported_formats" in config:
        config_formats = config["supported_formats"]
        assert isinstance(config_formats, list)
        
        # Verifiera att formats från /formats finns i config
        for format_item in formats:
            format_name = str(format_item).lower()
            assert any(format_name in str(config_format).lower() for config_format in config_formats), \
                f"Format {format_item} not found in config"


@pytest.mark.api
@pytest.mark.workflows
def test_api_pip_package_workflow(api_client):
    """Test pip package information workflow"""
    # Steg 1: Hämta pip-paket information
    response = api_client.get("/pip-package")
    assert response.status_code == 200
    
    pip_data = response.json()
    assert isinstance(pip_data, dict)
    
    # Steg 2: Verifiera att pip-paket information är komplett
    expected_keys = ["package_name", "version", "location", "install_path"]
    for key in expected_keys:
        assert key in pip_data, f"Pip package missing key: {key}"
    
    # Steg 3: Verifiera att version är giltig
    version = pip_data.get("version", "unknown")
    assert version != "unknown", "Version should be available"
    
    # Steg 4: Verifiera att location är antingen 'local' eller 'gitlab'
    location = pip_data.get("location", "unknown")
    assert location in ["local", "gitlab"], f"Invalid location: {location}"


@pytest.mark.api
@pytest.mark.workflows
def test_api_statistics_workflow(api_client):
    """Test API statistics workflow"""
    # Steg 1: Hämta initial statistik
    response = api_client.get("/stats")
    assert response.status_code == 200
    
    initial_stats = response.json()
    assert "total_repositories" in initial_stats
    assert "total_packages" in initial_stats
    assert "active_repositories" in initial_stats
    assert "packages_by_repository" in initial_stats
    
    # Steg 2: Hämta repositories och verifiera statistik
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    
    repositories = response.json()
    assert len(repositories) == initial_stats["total_repositories"]
    assert len(repositories) == initial_stats["active_repositories"]
    
    # Steg 3: Verifiera packages_by_repository
    packages_by_repo = initial_stats["packages_by_repository"]
    assert isinstance(packages_by_repo, dict)
    
    for repo in repositories:
        repo_name = repo["name"]
        assert repo_name in packages_by_repo, f"Repository {repo_name} not in packages_by_repository"
        assert isinstance(packages_by_repo[repo_name], int), f"Package count for {repo_name} not an integer"
    
    # Steg 4: Verifiera att total_packages är summan av alla repositories
    total_packages = sum(packages_by_repo.values())
    assert total_packages == initial_stats["total_packages"]


@pytest.mark.api
@pytest.mark.workflows
def test_api_error_recovery_workflow(api_client):
    """Test API error recovery workflow"""
    # Steg 1: Testa icke-existerande endpoint
    response = api_client.get("/nonexistent")
    assert response.status_code == 404
    
    # Steg 2: Verifiera att API fortfarande fungerar efter fel
    response = api_client.get("/health")
    assert response.status_code == 200
    
    # Steg 3: Testa icke-existerande repository
    response = api_client.get("/repositories/nonexistent-repo")
    assert response.status_code == 404
    
    # Steg 4: Verifiera att API fortfarande fungerar
    response = api_client.get("/repositories/")
    assert response.status_code == 200
    
    # Steg 5: Testa ogiltig POST request
    response = api_client.post("/repositories/", json={"invalid": "data"})
    assert response.status_code in [400, 422]
    
    # Steg 6: Verifiera att API fortfarande fungerar
    response = api_client.get("/stats")
    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.workflows
def test_api_concurrent_workflow(api_client):
    """Test API concurrent access workflow"""
    import threading
    import time
    
    results = []
    errors = []
    
    def make_requests():
        try:
            # Gör flera requests
            health_response = api_client.get("/health")
            stats_response = api_client.get("/stats")
            repos_response = api_client.get("/repositories/")
            
            results.append({
                "health": health_response.status_code,
                "stats": stats_response.status_code,
                "repos": repos_response.status_code
            })
        except Exception as e:
            errors.append(str(e))
    
    # Skapa 5 samtidiga trådar
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_requests)
        threads.append(thread)
        thread.start()
    
    # Vänta på att alla trådar ska slutföras
    for thread in threads:
        thread.join()
    
    # Verifiera att alla requests lyckades
    assert len(errors) == 0, f"Concurrent requests failed: {errors}"
    assert len(results) == 5, f"Expected 5 results, got {len(results)}"
    
    # Verifiera att alla responses var 200
    for result in results:
        assert result["health"] == 200, f"Health request failed: {result['health']}"
        assert result["stats"] == 200, f"Stats request failed: {result['stats']}"
        assert result["repos"] == 200, f"Repos request failed: {result['repos']}"


@pytest.mark.api
@pytest.mark.workflows
def test_api_performance_workflow(api_client):
    """Test API performance workflow"""
    import time
    
    # Testa response times för olika endpoints
    endpoints = [
        "/",
        "/health",
        "/stats",
        "/formats",
        "/config",
        "/pip-package",
        "/repositories/",
        "/packages/"
    ]
    
    max_response_time = 2.0  # 2 sekunder max per request
    
    for endpoint in endpoints:
        start_time = time.time()
        response = api_client.get(endpoint)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"
        assert response_time < max_response_time, f"Endpoint {endpoint} took {response_time:.2f}s (max: {max_response_time}s)"


@pytest.mark.api
@pytest.mark.workflows
def test_api_data_consistency_workflow(api_client):
    """Test API data consistency workflow"""
    # Steg 1: Hämta data från olika endpoints
    stats_response = api_client.get("/stats")
    repos_response = api_client.get("/repositories/")
    
    assert stats_response.status_code == 200
    assert repos_response.status_code == 200
    
    stats = stats_response.json()
    repositories = repos_response.json()
    
    # Steg 2: Verifiera att data är konsistent
    assert len(repositories) == stats["total_repositories"]
    assert len(repositories) == stats["active_repositories"]
    
    # Steg 3: Verifiera att packages_by_repository är korrekt
    packages_by_repo = stats["packages_by_repository"]
    for repo in repositories:
        repo_name = repo["name"]
        assert repo_name in packages_by_repo, f"Repository {repo_name} not in packages_by_repository"
    
    # Steg 4: Verifiera att total_packages är korrekt
    total_packages = sum(packages_by_repo.values())
    assert total_packages == stats["total_packages"]
    
    # Steg 5: Verifiera att alla repositories är aktiva
    for repo in repositories:
        assert repo["status"] == "active", f"Repository {repo['name']} is not active"
