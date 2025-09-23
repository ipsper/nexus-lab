"""
Nexus Repository Manager API - Huvudapplikation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import repository, packages, system

# Skapa FastAPI-instans med taggrupper
app = FastAPI(
    title="Nexus Repository Manager API",
    description="En FastAPI-applikation för att hantera Nexus Repository Manager",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
    tags_metadata=[
        {
            "name": "repository",
            "description": "Operations för att hantera repositories - skapa, hämta och konfigurera olika typer av paketarkiv",
        },
        {
            "name": "packages",
            "description": "Operations för att hantera paket - ladda upp, hämta, söka och hantera paket i repositories",
        },
        {
            "name": "överigt",
            "description": "Systeminformation, statistik, konfiguration och utvecklingsverktyg",
        },
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inkludera API routers
app.include_router(system.router)
app.include_router(repository.router)
app.include_router(packages.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )