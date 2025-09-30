"""
Health check and system status endpoints
"""
from fastapi import APIRouter
from datetime import datetime
import os
from .models import HealthResponse

# Skapa router för health endpoints
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
