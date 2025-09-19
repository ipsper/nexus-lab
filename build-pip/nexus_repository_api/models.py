"""
Pydantic-modeller för Nexus Repository API
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RepositoryInfo(BaseModel):
    """Information om en repository"""
    name: str
    type: str
    format: str
    url: str
    status: str


class PackageInfo(BaseModel):
    """Information om ett paket"""
    name: str
    version: str
    repository: str
    upload_date: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Response för health check"""
    status: str
    timestamp: datetime
    version: str
    environment: str


class StatsResponse(BaseModel):
    """Response för statistik"""
    total_repositories: int
    total_packages: int
    active_repositories: int
    packages_by_repository: dict


class ConfigResponse(BaseModel):
    """Response för konfiguration"""
    nexus_url: str
    api_version: str
    supported_operations: list


class FormatsResponse(BaseModel):
    """Response för stödda format"""
    supported_formats: list
    format_info: dict
