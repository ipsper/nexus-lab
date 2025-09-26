"""
Nexus Repository Manager API - Huvudapplikation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nexus_repository_api.api.v1 import repository, packages, system, schedule

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
        {
            "name": "schema",
            "description": "Schemaläggning av API-anrop - skapa, hantera och övervaka automatiska uppgifter",
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
app.include_router(schedule.router)


@app.on_event("startup")
async def startup_event():
    """Starta background tasks vid applikationsstart"""
    import asyncio
    # Starta schema background task
    asyncio.create_task(schedule.run_scheduled_tasks())

def run_server(host: str = "0.0.0.0", port: int = 3000, reload: bool = False, log_level: str = "info"):
    """Starta servern med uvicorn"""
    import uvicorn
    uvicorn.run(
        "nexus_repository_api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )


if __name__ == "__main__":
    run_server()