"""
Nexus Repository API - En FastAPI-baserad webbapplikation för att hantera Nexus Repository Manager

Detta paket tillhandahåller ett komplett REST API för att hantera Nexus Repository Manager,
inklusive repository-hantering, paket-upload/download och statistik.
"""

__version__ = "1.0.0"
__author__ = "IP-solutions Lab Team"
__email__ = "per.nehlin@ip-solutions.se"
__description__ = "En FastAPI-baserad webbapplikation för att hantera Nexus Repository Manager"

from .main import app, run_server
from .models import RepositoryInfo, PackageInfo, HealthResponse

__all__ = [
    "app",
    "run_server", 
    "RepositoryInfo",
    "PackageInfo",
    "HealthResponse",
]
