"""
Nexus Repository Manager support functions - rena hjälpfunktioner
"""
import requests
from support.api_client import APIClient
from typing import Optional


def get_nexus_version(nexus_client: APIClient) -> Optional[str]:
    """Hämta Nexus version"""
    try:
        response = nexus_client.get("/service/rest/v1/status")
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("version")
    except:
        pass
    return None


def is_nexus_ready(nexus_client: APIClient) -> bool:
    """Kontrollera om Nexus är redo"""
    try:
        response = nexus_client.get("/service/rest/v1/status")
        if response.status_code == 200:
            data = response.json()
            state = data.get("data", {}).get("state")
            return state == "STARTED"
    except:
        pass
    return False


def get_repositories_list(nexus_client: APIClient) -> list:
    """Hämta lista över repositories"""
    response = nexus_client.get("/service/rest/v1/repositories")
    if response.status_code == 200:
        return response.json()
    return []


def repository_exists(nexus_client: APIClient, repo_name: str) -> bool:
    """Kontrollera om repository finns"""
    repositories = get_repositories_list(nexus_client)
    return any(repo.get("name") == repo_name for repo in repositories)


