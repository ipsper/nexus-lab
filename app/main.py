from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

# Skapa FastAPI-instans
app = FastAPI(
    title="Nexus Repository Manager API",
    description="En FastAPI-applikation för att hantera Nexus Repository Manager",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic modeller
class RepositoryInfo(BaseModel):
    name: str
    type: str
    format: str
    url: str
    status: str

class PackageInfo(BaseModel):
    name: str
    version: str
    repository: str
    upload_date: Optional[datetime] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

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

# Root endpoint
@app.get("/", response_model=dict)
async def root():
    return {
        "message": "Välkommen till Nexus Repository Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

# Repository endpoints
@app.get("/repositories", response_model=List[RepositoryInfo])
async def get_repositories():
    """Hämta alla repositories"""
    return repositories

@app.get("/repositories/{repository_name}", response_model=RepositoryInfo)
async def get_repository(repository_name: str):
    """Hämta specifik repository"""
    for repo in repositories:
        if repo.name == repository_name:
            return repo
    raise HTTPException(status_code=404, detail="Repository inte hittad")

@app.post("/repositories", response_model=RepositoryInfo)
async def create_repository(repository: RepositoryInfo):
    """Skapa ny repository"""
    # Kontrollera om repository redan finns
    for repo in repositories:
        if repo.name == repository.name:
            raise HTTPException(status_code=400, detail="Repository finns redan")
    
    repositories.append(repository)
    return repository

# Package endpoints
@app.get("/packages", response_model=List[PackageInfo])
async def get_packages():
    """Hämta alla paket"""
    return packages

@app.post("/packages", response_model=PackageInfo)
async def upload_package(package: PackageInfo):
    """Ladda upp paket"""
    package.upload_date = datetime.now()
    packages.append(package)
    return package

@app.get("/packages/{package_name}", response_model=List[PackageInfo])
async def get_package(package_name: str):
    """Hämta paket efter namn"""
    found_packages = [pkg for pkg in packages if pkg.name == package_name]
    if not found_packages:
        raise HTTPException(status_code=404, detail="Paket inte hittat")
    return found_packages

# Repository-specifika paket
@app.get("/repositories/{repository_name}/packages", response_model=List[PackageInfo])
async def get_repository_packages(repository_name: str):
    """Hämta paket från specifik repository"""
    # Kontrollera att repository finns
    repo_exists = any(repo.name == repository_name for repo in repositories)
    if not repo_exists:
        raise HTTPException(status_code=404, detail="Repository inte hittad")
    
    repo_packages = [pkg for pkg in packages if pkg.repository == repository_name]
    return repo_packages

# Statistik endpoints
@app.get("/stats")
async def get_stats():
    """Hämta statistik"""
    return {
        "total_repositories": len(repositories),
        "total_packages": len(packages),
        "active_repositories": len([repo for repo in repositories if repo.status == "active"]),
        "packages_by_repository": {
            repo.name: len([pkg for pkg in packages if pkg.repository == repo.name])
            for repo in repositories
        }
    }

# Repository format endpoints
@app.get("/formats")
async def get_supported_formats():
    """Hämta stödda format"""
    formats = list(set(repo.format for repo in repositories))
    return {
        "supported_formats": formats,
        "format_info": {
            "pypi": "Python paket (pip)",
            "apt": "Debian/Ubuntu paket",
            "rpm": "Red Hat/CentOS paket",
            "docker": "Docker containers",
            "maven": "Java/Maven artefakter",
            "npm": "Node.js paket"
        }
    }

# Konfiguration endpoints
@app.get("/config")
async def get_config():
    """Hämta konfiguration"""
    return {
        "nexus_url": "http://localhost:8081",
        "api_version": "1.0.0",
        "supported_operations": [
            "list_repositories",
            "create_repository",
            "upload_package",
            "download_package",
            "search_packages"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
