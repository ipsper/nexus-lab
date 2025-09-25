"""
Pydantic models för API v1
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RepositoryInfo(BaseModel):
    """Model för repository information"""
    name: str
    type: str
    format: str
    url: str
    status: str


class PackageInfo(BaseModel):
    """Model för package information"""
    name: str
    version: str
    repository: str
    upload_date: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Model för health check response"""
    status: str
    timestamp: datetime
    version: str
    environment: str


class PipPackageInfo(BaseModel):
    """Response för pip-paketinformation"""
    package_name: str
    version: str
    location: str  # "local" eller "gitlab"
    install_path: str
    git_info: Optional[dict] = None
    build_info: Optional[dict] = None


# In-memory storage (i en riktig app skulle detta vara en databas)
repositories = [
    RepositoryInfo(
        name="pypi-hosted",
        type="hosted",
        format="pypi",
        url="http://localhost:8081/repository/pypi-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="apt-hosted",
        type="hosted",
        format="apt",
        url="http://localhost:8081/repository/apt-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="rpm-hosted",
        type="hosted",
        format="rpm",
        url="http://localhost:8081/repository/rpm-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="docker-hosted",
        type="hosted",
        format="docker",
        url="http://localhost:8081/repository/docker-hosted/",
        status="active"
    )
]

packages = []
