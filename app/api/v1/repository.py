"""
Repository management endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
from .models import RepositoryInfo, repositories

# Skapa router för repository endpoints
router = APIRouter(
    prefix="/api/repositories",
    tags=["repository"],
    responses={404: {"description": "Repository inte hittad"}},
)


@router.get("/", response_model=List[RepositoryInfo])
async def get_repositories():
    """Hämta alla repositories"""
    return repositories


@router.get("/{repository_name}", response_model=RepositoryInfo)
async def get_repository(repository_name: str):
    """Hämta specifik repository"""
    for repo in repositories:
        if repo.name == repository_name:
            return repo
    raise HTTPException(status_code=404, detail="Repository inte hittad")


@router.post("/", response_model=RepositoryInfo)
async def create_repository(repository: RepositoryInfo):
    """Skapa ny repository"""
    # Kontrollera om repository redan finns
    for repo in repositories:
        if repo.name == repository.name:
            raise HTTPException(status_code=400, detail="Repository finns redan")
    
    repositories.append(repository)
    return repository
