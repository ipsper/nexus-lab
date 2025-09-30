"""
Statistics and analytics endpoints
"""
from fastapi import APIRouter
from .models import repositories, packages

# Skapa router för stats endpoints
router = APIRouter(
    prefix="/api",
    tags=["överigt"],
    responses={404: {"description": "Resurs inte hittad"}},
)


@router.get("/stats")
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
