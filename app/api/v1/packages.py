"""
Package management endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from .models import PackageInfo, packages, repositories

# Skapa router för package endpoints
router = APIRouter(
    prefix="/api/packages",
    tags=["packages"],
    responses={404: {"description": "Paket inte hittat"}},
)


@router.get("/", response_model=List[PackageInfo])
async def get_packages():
    """Hämta alla paket"""
    return packages


@router.post("/", response_model=PackageInfo)
async def upload_package(package: PackageInfo):
    """Ladda upp paket"""
    package.upload_date = datetime.now()
    packages.append(package)
    return package


@router.get("/{package_name}", response_model=List[PackageInfo])
async def get_package(package_name: str):
    """Hämta paket efter namn"""
    found_packages = [pkg for pkg in packages if pkg.name == package_name]
    if not found_packages:
        raise HTTPException(status_code=404, detail="Paket inte hittat")
    return found_packages


# Repository-specific package endpoints
@router.get("/repositories/{repository_name}/packages", response_model=List[PackageInfo])
async def get_repository_packages(repository_name: str):
    """Hämta paket från specifik repository"""
    # Kontrollera att repository finns
    repo_exists = any(repo.name == repository_name for repo in repositories)
    if not repo_exists:
        raise HTTPException(status_code=404, detail="Repository inte hittad")
    
    repo_packages = [pkg for pkg in packages if pkg.repository == repository_name]
    return repo_packages
