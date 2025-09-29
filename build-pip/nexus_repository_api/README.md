# Nexus Repository Manager API

En FastAPI-baserad webbapplikation som tillhandahåller ett REST API för att hantera Nexus Repository Manager. Applikationen körs på port 8000 och kan deployeras i en Docker-container.

## Funktioner

- **Repository Management**: Hantera olika typer av repositories (PyPI, APT, RPM, Docker)
- **Package Management**: Ladda upp, hämta och söka paket
- **Health Monitoring**: Health check endpoints för övervakning
- **RESTful API**: Komplett REST API med automatisk dokumentation
- **CORS Support**: Stöd för Cross-Origin Resource Sharing
- **Docker Support**: Färdig Docker-konfiguration

## Stödda Repository-format

- **PyPI**: Python paket (pip)
- **APT**: Debian/Ubuntu paket
- **RPM**: Red Hat/CentOS paket
- **Docker**: Docker containers
- **Maven**: Java/Maven artefakter (planerat)
- **npm**: Node.js paket (planerat)

## Snabbstart

### Lokal utveckling

1. **Installera beroenden**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Starta applikationen**:
   ```bash
   python main.py
   ```

3. **Öppna API-dokumentation**:
   - Swagger UI: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

### Med Docker

1. **Bygg och kör med Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Eller bygg och kör manuellt**:
   ```bash
   # Bygg image
   docker build -t nexus-api .
   
   # Kör container
   docker run -p 8000:8000 nexus-api
   ```

## API Endpoints

### Grundläggande

- `GET /api/` - Root endpoint med grundläggande information
- `GET /api/health` - Health check endpoint
- `GET /api/docs` - Swagger UI dokumentation
- `GET /api/redoc` - ReDoc dokumentation

### Repositories

- `GET /api/repositories/` - Hämta alla repositories
- `GET /api/repositories/{name}` - Hämta specifik repository
- `POST /api/repositories/` - Skapa ny repository

### Paket

- `GET /api/packages/` - Hämta alla paket
- `POST /api/packages/` - Ladda upp paket
- `GET /api/packages/{name}` - Hämta paket efter namn
- `GET /api/packages/repositories/{name}/packages` - Hämta paket från specifik repository

### Statistik och konfiguration

- `GET /api/stats` - Hämta statistik
- `GET /api/formats` - Hämta stödda format
- `GET /api/config` - Hämta konfiguration
- `GET /api/pip-package` - Hämta pip-paket information

## Exempel på användning

### Grundläggande API-anrop

```bash
# Health check
curl -X GET "http://localhost:8000/api/health" \
  -H "accept: application/json"

# Root endpoint
curl -X GET "http://localhost:8000/api/" \
  -H "accept: application/json"

# API-konfiguration
curl -X GET "http://localhost:8000/api/config" \
  -H "accept: application/json"

# Pip-paket information
curl -X GET "http://localhost:8000/api/pip-package" \
  -H "accept: application/json"

# Statistik
curl -X GET "http://localhost:8000/api/stats" \
  -H "accept: application/json"

# Stödda format
curl -X GET "http://localhost:8000/api/formats" \
  -H "accept: application/json"
```

### Repository-hantering

```bash
# Hämta alla repositories
curl -X GET "http://localhost:8000/api/repositories/" \
  -H "accept: application/json"

# Hämta specifik repository
curl -X GET "http://localhost:8000/api/repositories/pypi-hosted" \
  -H "accept: application/json"

# Skapa ny repository (POST med JSON-data)
curl -X POST "http://localhost:8000/api/repositories/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-repo",
    "format": "pypi",
    "type": "hosted",
    "description": "Test repository"
  }'
```

### Paket-hantering

```bash
# Hämta alla paket
curl -X GET "http://localhost:8000/api/packages/" \
  -H "accept: application/json"

# Hämta specifikt paket
curl -X GET "http://localhost:8000/api/packages/requests" \
  -H "accept: application/json"

# Hämta paket från specifik repository
curl -X GET "http://localhost:8000/api/packages/repositories/pypi-hosted/packages" \
  -H "accept: application/json"

# Skapa nytt paket (POST med JSON-data)
curl -X POST "http://localhost:8000/api/packages/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-package",
    "version": "1.0.0",
    "repository": "pypi-hosted",
    "description": "Test package"
  }'
```

### Swagger UI och dokumentation

```bash
# Öppna Swagger UI i webbläsare
open http://localhost:8000/api/docs

# Hämta OpenAPI specifikation
curl -X GET "http://localhost:8000/api/openapi.json" \
  -H "accept: application/json" | jq '.'

# Hämta ReDoc dokumentation
curl -X GET "http://localhost:8000/api/redoc" \
  -H "accept: text/html"
```

### Avancerade exempel

```bash
# Testa med verbose output för debugging
curl -v -X GET "http://localhost:8000/api/health" \
  -H "accept: application/json"

# Testa med timeout
curl --max-time 10 -X GET "http://localhost:8000/api/stats" \
  -H "accept: application/json"

# Testa med custom headers
curl -X GET "http://localhost:8000/api/config" \
  -H "accept: application/json" \
  -H "User-Agent: MyApp/1.0" \
  -H "X-API-Key: your-api-key"

# Spara response till fil
curl -X GET "http://localhost:8000/api/stats" \
  -H "accept: application/json" \
  -o stats.json
```

### Felsöknings-exempel

```bash
# Testa anslutning (endast status)
curl -I "http://localhost:8000/api/health"

# Testa med olika HTTP-metoder
curl -X OPTIONS "http://localhost:8000/api/health" \
  -H "accept: application/json"

# Testa med felaktig data för att se error handling
curl -X POST "http://localhost:8000/api/repositories/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# Testa 404-fel
curl -X GET "http://localhost:8000/api/nonexistent" \
  -H "accept: application/json"
```

### Batch-testning

```bash
# Testa alla endpoints i en loop
for endpoint in health config stats formats repositories packages; do
  echo "Testing /api/$endpoint"
  curl -s -X GET "http://localhost:8000/api/$endpoint" \
    -H "accept: application/json" | jq '.'
  echo "---"
done
```

## Konfiguration

### Miljövariabler

Kopiera `env.example` till `.env` och anpassa:

```bash
cp env.example .env
```

Tillgängliga miljövariabler:

- `ENVIRONMENT`: Miljö (development/production)
- `NEXUS_URL`: URL till Nexus Repository Manager
- `API_VERSION`: API-version
- `DEBUG`: Debug-läge (true/false)
- `LOG_LEVEL`: Loggningsnivå
- `CORS_ORIGINS`: Tillåtna CORS-origins

### Docker-konfiguration

Applikationen inkluderar:

- **Dockerfile**: Multi-stage build för optimerad image
- **docker-compose.yml**: Komplett Docker Compose-konfiguration
- **Health checks**: Automatiska hälsokontroller
- **Restart policies**: Automatisk omstart vid fel

## Utveckling

### Projektstruktur

```
app/
├── main.py              # Huvudapplikation
├── requirements.txt     # Python-beroenden
├── Dockerfile          # Docker-konfiguration
├── docker-compose.yml  # Docker Compose-konfiguration
├── env.example         # Miljövariabler-exempel
└── README.md           # Denna fil
```

### Lägga till nya endpoints

1. Definiera Pydantic-modeller för request/response
2. Skapa endpoint-funktioner med FastAPI-decorators
3. Lägg till dokumentation och exempel

### Lägga till databas

Applikationen är förberedd för databasintegration:

1. Lägg till databas-URL i miljövariabler
2. Installera databas-driver (SQLAlchemy, etc.)
3. Implementera databasmodeller
4. Uppdatera CRUD-operationer

## Deployment

### Med Kind/Kubernetes

Applikationen kan deployeras till samma Kind-kluster som Nexus:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus-api
  namespace: nexus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nexus-api
  template:
    metadata:
      labels:
        app: nexus-api
    spec:
      containers:
      - name: nexus-api
        image: nexus-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: NEXUS_URL
          value: "http://nexus-service:8081"
---
apiVersion: v1
kind: Service
metadata:
  name: nexus-api-service
  namespace: nexus
spec:
  selector:
    app: nexus-api
  ports:
  - port: 8000
    targetPort: 8000
  type: NodePort
```

### Med Docker Swarm

```bash
# Deploya stack
docker stack deploy -c docker-compose.yml nexus-api
```

## Felsökning

### Vanliga problem

1. **Port redan används**:
   ```bash
   # Kontrollera vilken process som använder port 8000
   lsof -i :8000
   ```

2. **Container startar inte**:
   ```bash
   # Kontrollera loggar
   docker logs nexus-api
   ```

3. **API svarar inte**:
   ```bash
   # Kontrollera health check
   curl http://localhost:8000/api/health
   ```

### Loggar

```bash
# Docker Compose
docker-compose logs -f nexus-api

# Docker
docker logs -f nexus-api

# Kubernetes
kubectl logs -f deployment/nexus-api -n nexus
```

## Säkerhet

### Produktionsrekommendationer

1. **Använd HTTPS**: Konfigurera SSL/TLS
2. **Autentisering**: Implementera API-nycklar eller JWT
3. **Rate limiting**: Begränsa antal requests per IP
4. **Input validation**: Validera all input noggrant
5. **Logging**: Logga alla viktiga operationer

### Säkerhetsheaders

Applikationen inkluderar grundläggande säkerhetsheaders via CORS-middleware.

## Monitoring

### Health checks

- **Endpoint**: `/health`
- **Docker**: Automatisk health check var 30:e sekund
- **Kubernetes**: Liveness och readiness probes

### Metrics

Framtida funktioner:
- Prometheus metrics
- Grafana dashboards
- Alerting

## Licens

Denna applikation är licensierad under MIT License.

## Support

För support och frågor:
- Skapa issue i projektets repository
- Kontakta utvecklingsteamet
- Läs API-dokumentationen på `/docs`
