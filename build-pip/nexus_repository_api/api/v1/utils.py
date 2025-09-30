"""
Utility endpoints for system information
"""
from fastapi import APIRouter
from .models import repositories

# Skapa router för utility endpoints
router = APIRouter(
    prefix="/api",
    tags=["överigt"],
    responses={404: {"description": "Resurs inte hittad"}},
)


@router.get("/formats")
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
