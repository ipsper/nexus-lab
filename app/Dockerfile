# Använd Python 3.11 slim image
FROM python:3.11-slim

# Sätt arbetskatalog
WORKDIR /app

# Installera systemberoenden
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiera requirements och installera Python-paket
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera applikationskod
COPY . .

# Exponera port 3000
EXPOSE 3000

# Miljövariabler
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Starta applikationen
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
