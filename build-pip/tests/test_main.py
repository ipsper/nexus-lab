"""
Tester för huvudmodulen
"""

import pytest
from fastapi.testclient import TestClient
from nexus_repository_api.main import app

client = TestClient(app)


def test_root():
    """Testa root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Välkommen till Nexus Repository Manager API"
    assert data["version"] == "1.0.0"


def test_health_check():
    """Testa health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data


def test_get_repositories():
    """Testa hämtning av repositories"""
    response = client.get("/repositories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Kontrollera första repository
    repo = data[0]
    assert "name" in repo
    assert "type" in repo
    assert "format" in repo
    assert "url" in repo
    assert "status" in repo


def test_get_repository():
    """Testa hämtning av specifik repository"""
    # Testa befintlig repository
    response = client.get("/repositories/pypi-hosted")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "pypi-hosted"
    assert data["format"] == "pypi"
    
    # Testa icke-existerande repository
    response = client.get("/repositories/nonexistent")
    assert response.status_code == 404


def test_create_repository():
    """Testa skapande av ny repository"""
    new_repo = {
        "name": "test-repo",
        "type": "hosted",
        "format": "maven",
        "url": "http://localhost:8081/repository/test-repo/",
        "status": "active"
    }
    
    response = client.post("/repositories", json=new_repo)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-repo"
    assert data["format"] == "maven"
    
    # Testa att skapa samma repository igen (ska ge fel)
    response = client.post("/repositories", json=new_repo)
    assert response.status_code == 400


def test_get_packages():
    """Testa hämtning av paket"""
    response = client.get("/packages")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_upload_package():
    """Testa uppladdning av paket"""
    package = {
        "name": "test-package",
        "version": "1.0.0",
        "repository": "pypi-hosted"
    }
    
    response = client.post("/packages", json=package)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-package"
    assert data["version"] == "1.0.0"
    assert "upload_date" in data


def test_get_stats():
    """Testa statistik endpoint"""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_repositories" in data
    assert "total_packages" in data
    assert "active_repositories" in data
    assert "packages_by_repository" in data


def test_get_formats():
    """Testa format endpoint"""
    response = client.get("/formats")
    assert response.status_code == 200
    data = response.json()
    assert "supported_formats" in data
    assert "format_info" in data
    assert isinstance(data["supported_formats"], list)


def test_get_config():
    """Testa konfiguration endpoint"""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "nexus_url" in data
    assert "api_version" in data
    assert "supported_operations" in data
