"""
FastAPI support functions - rena hjälpfunktioner
"""
from support.api_client import APIClient
from typing import Dict, Any, List


def create_test_repository(api_client: APIClient, repo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Skapa test repository"""
    response = api_client.post("/repositories", data=repo_data)
    return response.json()


def get_repository_by_name(api_client: APIClient, name: str) -> Dict[str, Any]:
    """Hämta repository efter namn"""
    response = api_client.get(f"/repositories/{name}")
    return response.json() if response.status_code == 200 else None


def upload_test_package(api_client: APIClient, package_data: Dict[str, Any]) -> Dict[str, Any]:
    """Ladda upp test-paket"""
    response = api_client.post("/packages", data=package_data)
    return response.json()


def get_packages_by_name(api_client: APIClient, name: str) -> List[Dict[str, Any]]:
    """Hämta paket efter namn"""
    response = api_client.get(f"/packages/{name}")
    return response.json() if response.status_code == 200 else []


def get_repository_packages(api_client: APIClient, repo_name: str) -> List[Dict[str, Any]]:
    """Hämta paket från specifik repository"""
    response = api_client.get(f"/repositories/{repo_name}/packages")
    return response.json() if response.status_code == 200 else []


def get_openapi_schema(api_client: APIClient) -> Dict[str, Any]:
    """Hämta OpenAPI schema"""
    response = api_client.get("/openapi.json")
    return response.json() if response.status_code == 200 else {}


