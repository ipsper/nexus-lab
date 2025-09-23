"""
System information and utility endpoints
"""
from fastapi import APIRouter
from datetime import datetime
import os
import sys
import subprocess
from importlib.metadata import distribution
from .models import HealthResponse, PipPackageInfo, repositories, packages

# Skapa router för system endpoints
router = APIRouter(
    prefix="/api",
    tags=["överigt"],
    responses={404: {"description": "Resurs inte hittad"}},
)


@router.get("/", response_model=dict)
async def root():
    """Root endpoint med grundläggande information"""
    return {
        "message": "Välkommen till Nexus Repository Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
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


@router.get("/config")
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


@router.get("/pip-package", response_model=PipPackageInfo)
async def get_pip_package_info():
    """Hämta information om det installerade pip-paketet"""
    try:
        # Hämta paketinformation
        package_name = "nexus-repository-api"
        try:
            dist = distribution(package_name)
            if dist:
                version = dist.version
                location = dist.locate_file('').parent if hasattr(dist, 'locate_file') else "unknown"
            else:
                version = "unknown"
                location = "unknown"
        except Exception:
            # Fallback om paketet inte hittas
            version = "unknown"
            location = "unknown"

        # Bestäm om det är lokalt eller från GitLab
        location_str = str(location) if location else "unknown"
        is_local = "build-pip" in location_str or "nexus-lab" in location_str
        package_location = "local" if is_local else "gitlab"

        # Hämta Git-information om möjligt
        git_info = None
        try:
            # Kolla om vi är i en Git-repo
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            if result.returncode == 0:
                # Hämta Git-information
                git_commit = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                ).stdout.strip()

                git_branch = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                ).stdout.strip()

                git_info = {
                    "commit": git_commit,
                    "branch": git_branch,
                    "is_git_repo": True
                }
        except Exception:
            git_info = {"is_git_repo": False}

        # Hämta build-information
        build_info = {
            "python_version": sys.version,
            "platform": sys.platform,
            "environment": os.getenv("ENVIRONMENT", "development"),
            "ci_project_id": os.getenv("CI_PROJECT_ID"),
            "ci_api_v4_url": os.getenv("CI_API_V4_URL")
        }

        return PipPackageInfo(
            package_name=package_name,
            version=version,
            location=package_location,
            install_path=str(location) if location else "unknown",
            git_info=git_info,
            build_info=build_info
        )

    except Exception as e:
        # Fallback om något går fel
        return PipPackageInfo(
            package_name="nexus-repository-api",
            version="unknown",
            location="unknown",
            install_path="unknown",
            git_info={"error": str(e)},
            build_info={"error": str(e)}
        )
