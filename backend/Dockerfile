# Nexus Repository API - Docker Image med Pip-paket
# Detta Dockerfile använder det lokalt installerade pip-paketet

# Använd Python 3.13 slim image (samma som build-miljön)
FROM python:3.13-slim

# Sätt arbetskatalog
WORKDIR /app

# Installera systemberoenden
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiera det byggda pip-paketet från local-install output
COPY build-pip/dist/nexus_repository_api-1.0.0-py3-none-any.whl .

# Uppdatera pip till senaste version och installera pip-paketet
RUN pip install --upgrade pip==25.2 && pip install --no-cache-dir nexus_repository_api-1.0.0-py3-none-any.whl

# Exponera port 3000
EXPOSE 3000

# Miljövariabler
ENV ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Starta applikationen med nexus-api kommandot
CMD ["nexus-api", "--host", "0.0.0.0", "--port", "3000"]
