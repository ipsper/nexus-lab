# Nexus Repository API - Docker Image med Pip-paket
# Detta Dockerfile använder det byggda pip-paketet istället för att kopiera koden

# Använd Python 3.11 slim image
FROM python:3.11-slim

# Sätt arbetskatalog
WORKDIR /app

# Installera systemberoenden
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiera det byggda pip-paketet
COPY build-pip/dist/nexus_repository_api-1.0.0-py3-none-any.whl .

# Installera pip-paketet
RUN pip install --no-cache-dir nexus_repository_api-1.0.0-py3-none-any.whl

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
