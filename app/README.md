# Nexus Repository Manager API

En FastAPI-baserad webbapplikation som tillhandahåller ett REST API för att hantera Nexus Repository Manager. Applikationen körs på port 3000 och kan deployeras i en Docker-container.

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
   - Swagger UI: http://localhost:3000/docs
   - ReDoc: http://localhost:3000/redoc

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
   docker run -p 3000:3000 nexus-api
   ```

## API Endpoints

### Grundläggande

- `GET /` - Root endpoint med grundläggande information
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI dokumentation
- `GET /redoc` - ReDoc dokumentation

### Repositories

- `GET /repositories` - Hämta alla repositories
- `GET /repositories/{name}` - Hämta specifik repository
- `POST /repositories` - Skapa ny repository

### Paket

- `GET /packages` - Hämta alla paket
- `POST /packages` - Ladda upp paket
- `GET /packages/{name}` - Hämta paket efter namn
- `GET /repositories/{name}/packages` - Hämta paket från specifik repository

### Statistik och konfiguration

- `GET /stats` - Hämta statistik
- `GET /formats` - Hämta stödda format
- `GET /config` - Hämta konfiguration

## Exempel på användning

### Hämta alla repositories

```bash
curl http://localhost:3000/repositories
```

### Skapa ny repository

```bash
curl -X POST http://localhost:3000/repositories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "maven-hosted",
    "type": "hosted",
    "format": "maven",
    "url": "http://localhost:8081/repository/maven-hosted/",
    "status": "active"
  }'
```

### Ladda upp paket

```bash
curl -X POST http://localhost:3000/packages \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-package",
    "version": "1.0.0",
    "repository": "pypi-hosted"
  }'
```

### Hämta statistik

```bash
curl http://localhost:3000/stats
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
        - containerPort: 3000
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
  - port: 3000
    targetPort: 3000
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
   # Kontrollera vilken process som använder port 3000
   lsof -i :3000
   ```

2. **Container startar inte**:
   ```bash
   # Kontrollera loggar
   docker logs nexus-api
   ```

3. **API svarar inte**:
   ```bash
   # Kontrollera health check
   curl http://localhost:3000/health
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
