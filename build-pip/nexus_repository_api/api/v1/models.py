"""
Pydantic models för API v1
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


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


class ScheduleFrequency(str, Enum):
    """Schema-frekvenser"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class ScheduleRequest(BaseModel):
    """Request för att skapa ett schema"""
    name: str
    endpoint: str  # t.ex. "/api/repositories/"
    method: str = "GET"  # HTTP-metod
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None  # För POST/PUT requests
    frequency: ScheduleFrequency
    start_time: Optional[datetime] = None  # När schemat ska börja
    end_time: Optional[datetime] = None  # När schemat ska sluta
    max_executions: Optional[int] = None  # Max antal körningar
    cron_expression: Optional[str] = None  # För custom frekvens
    enabled: bool = True


class ScheduleUpdate(BaseModel):
    """Request för att uppdatera ett schema (alla fält optional)"""
    name: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
    frequency: Optional[ScheduleFrequency] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_executions: Optional[int] = None
    cron_expression: Optional[str] = None
    enabled: Optional[bool] = None


class ScheduleResponse(BaseModel):
    """Response för schema-information"""
    id: str
    name: str
    endpoint: str
    method: str
    frequency: ScheduleFrequency
    next_execution: Optional[datetime]
    last_execution: Optional[datetime]
    execution_count: int
    max_executions: Optional[int]
    enabled: bool
    created_at: datetime


class ScheduleExecution(BaseModel):
    """Information om en schema-körning"""
    id: str
    schedule_id: str
    executed_at: datetime
    status: str  # "success", "failed", "running"
    response_status: Optional[int]
    response_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    execution_time_ms: Optional[int]


# In-memory storage (i en riktig app skulle detta vara en databas)
repositories = [
    RepositoryInfo(
        name="pypi-hosted",
        type="hosted",
        format="pypi",
        url="http://localhost:8000/repository/pypi-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="apt-hosted",
        type="hosted",
        format="apt",
        url="http://localhost:8000/repository/apt-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="rpm-hosted",
        type="hosted",
        format="rpm",
        url="http://localhost:8000/repository/rpm-hosted/",
        status="active"
    ),
    RepositoryInfo(
        name="docker-hosted",
        type="hosted",
        format="docker",
        url="http://localhost:8000/repository/docker-hosted/",
        status="active"
    )
]

packages = []

# Schema storage (i en riktig app skulle detta vara en databas)
schedules: Dict[str, ScheduleResponse] = {}
schedule_executions: List[ScheduleExecution] = []
