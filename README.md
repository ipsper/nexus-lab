# Nexus Repository Manager - Container Installation Guide

En komplett lösning för att köra Nexus Repository Manager med FastAPI i Kubernetes, inklusive automatiserad testning och pip-paket distribution.

## 🚀 Snabbstart

### Komplett setup med Frontend + Backend

```bash
# 1. Starta Kind-kluster och Backend
./scripts/run.sh create

# 2. Starta Frontend (i nytt terminalfönster)
cd frontend
npm install
npm run dev

# 3. Kör alla tester
./scripts/run-test.sh run-all

# 4. Ta bort allt när du är klar
./scripts/run.sh delete
```

### Åtkomst till tjänster

- **Frontend**: `http://localhost:3000` (React-applikation)
- **Backend API**: `http://localhost:8000/api` (FastAPI via Kong)
- **Swagger UI**: `http://localhost:8000/docs` (API-dokumentation)
- **Nexus UI**: `http://localhost:8081` (Repository Manager)

## 📋 Översikt

Nexus Repository Manager är en kraftfull artefakt-hantering som stöder:
- **Python pip-paket** (PyPI)
- **APT-paket** (Debian/Ubuntu) 
- **RPM-paket** (Red Hat/CentOS)
- **Docker-containers** (Docker Registry)
- **Maven, npm, NuGet** och många fler format

## ⚙️ Förutsättningar

### Backend (Kind-kluster)
- Docker installerat på systemet
- Kind (Kubernetes in Docker) installerat
- kubectl installerat
- Minst 4GB RAM tillgängligt
- Minst 20GB ledigt diskutrymme

### Frontend (React-applikation)
- Node.js 18+ installerat
- npm eller yarn
- Modern webbläsare (Chrome, Firefox, Safari, Edge)

## 📦 Pip-paket Distribution

FastAPI-applikationen kan distribueras som pip-paket:

👉 **[Detaljerad guide: build-pip/README.md](build-pip/README.md)**  
🔧 **[Felsökningsguide: build-pip/TROUBLESHOOTING.md](build-pip/TROUBLESHOOTING.md)**

```bash
# Snabbstart med pip-paket
./scripts/build-pip.sh build install
nexus-api --port 3000
```

## 🚀 Installation

### Alternativ 1: Komplett setup (Rekommenderat)

```bash
# Skapa allt på en gång (kluster + applikationer)
./scripts/run.sh create

# När du är klar, ta bort allt för en ren start
./scripts/run.sh delete
```

### Alternativ 2: Steg-för-steg setup

```bash
# Installera Kind
./scripts/run.sh install-kind

# Skapa Kind-kluster
./scripts/run.sh create-cluster

# Deploya Nexus
./scripts/run.sh deploy-nexus

# Bygga och deploya API
./scripts/run.sh build-api
./scripts/run.sh deploy-api

# Hämta admin-lösenord
./scripts/run.sh get-password

# Visa alla tillgängliga kommandon
./scripts/run.sh help
```

### Alternativ 3: Manuell installation

👉 **[Se detaljerad manuell guide: MANUAL_INSTALLATION.md](MANUAL_INSTALLATION.md)**

## ⚙️ Konfiguration

### Åtkomst till tjänster

- **Frontend**: `http://localhost:3000` (React-applikation)
- **Backend API**: `http://localhost:8000/api` (FastAPI via Kong)
- **Swagger UI**: `http://localhost:8000/docs` (API-dokumentation)
- **Nexus UI**: `http://localhost:8081` (Repository Manager)

### Hämta admin-lösenord

```bash
# Hitta admin-lösenordet
kubectl exec -n nexus deployment/nexus -- cat /nexus-data/admin.password
```

### Logga in

- Användarnamn: `admin`
- Lösenord: (kopiera från ovan)
- Följ guiden för att skapa ett nytt lösenord

👉 **[Se detaljerad konfigurationsguide: CONFIGURATION.md](CONFIGURATION.md)**

## 📖 Användning

### Snabbstart med Frontend

```bash
# Öppna React-applikationen
open http://localhost:3000

# Frontend innehåller:
# - Dashboard med systemöversikt
# - Repository-hantering
# - Schema-hantering
# - Statistik och konfiguration
```

### Snabbstart med API

```bash
# Testa API:et direkt
curl http://localhost:8000/api/health

# Öppna Swagger UI
open http://localhost:8000/docs
```

### Python (pip)

```bash
# Konfigurera pip för att använda Nexus
pip install --index-url http://localhost:8081/repository/pypi-hosted/simple/ package-name
```

### Docker

```bash
# Konfigurera Docker för att använda Nexus
docker login localhost:8082
docker tag myimage:latest localhost:8082/docker-hosted/myimage:latest
docker push localhost:8082/docker-hosted/myimage:latest
```

👉 **[Se detaljerad användningsguide: USAGE.md](USAGE.md)**

## 🔧 Avancerad konfiguration

### Backup och återställning

```bash
# Backup av data
kubectl exec -n nexus deployment/nexus -- tar czf /tmp/nexus-backup.tar.gz -C /nexus-data .
kubectl cp nexus/$(kubectl get pods -n nexus -l app=nexus -o jsonpath='{.items[0].metadata.name}'):/tmp/nexus-backup.tar.gz ./nexus-backup.tar.gz
```

### SSL/TLS och prestanda

👉 **[Se avancerad konfigurationsguide: ADVANCED_CONFIG.md](ADVANCED_CONFIG.md)**

## 🐛 Felsökning

### Snabb felsökning

```bash
# Kör fullständig debug-analys
./scripts/k8s-debug.sh full-debug

# Felsöka specifika komponenter
./scripts/k8s-debug.sh api-status
./scripts/k8s-debug.sh nexus-status
```

### Vanliga problem

1. **Pod startar inte**: `./scripts/k8s-debug.sh api-status`
2. **Åtkomst nekad**: `./scripts/k8s-debug.sh network`
3. **Långsam prestanda**: `./scripts/k8s-debug.sh resources`

👉 **[Se detaljerad felsökningsguide: scripts/k8s-debug-README.md](scripts/k8s-debug-README.md)**

## 🔒 Säkerhet

### Grundläggande säkerhetsåtgärder

1. **Ändra standardlösenord** omedelbart
2. **Aktivera anonym åtkomst** endast för publika repositories
3. **Konfigurera användarroller** och behörigheter
4. **Använd HTTPS** i produktionsmiljöer

## 🔧 Underhåll

### Uppdateringar

```bash
# Uppdatera image i deployment
kubectl set image deployment/nexus nexus=sonatype/nexus3:latest -n nexus

# Kontrollera rollout-status
kubectl rollout status deployment/nexus -n nexus
```

### Ta bort Kind-klustret

```bash
# Ta bort hela Kind-klustret
kind delete cluster --name nexus-cluster
```

## 📚 Dokumentation

### 🎯 Huvudguider
- **[📋 Scripts Guide](scripts/README.md)** - Översikt av alla scripts och verktyg
- **[🔧 run.sh Guide](scripts/run-README.md)** - Huvudhanteringsskript för installation och konfiguration
- **[🐛 k8s-debug.sh Guide](scripts/k8s-debug-README.md)** - Avancerat debug-skript för felsökning
- **[🧪 Testsystem Guide](testning/README.md)** - Komplett guide för testsystemet
- **[🚀 Backend Guide](build-pip/nexus_repository_api/README.md)** - FastAPI-applikationens struktur och endpoints
- **[🎨 Frontend Guide](frontend/README.md)** - React-applikationens struktur och komponenter
- **[📅 Schemaläggare Guide](build-pip/nexus_repository_api/api/v1/SCHEDULER_README.md)** - Automatisk schemaläggning av API-anrop

### 🧪 Testsystem
Projektet har ett omfattande testsystem med:
- **Health checks** - Kontrollerar miljöns status
- **API-tester** - Testar REST endpoints
- **GUI-tester** - Playwright-baserade UI-tester  
- **Integration-tester** - Testar samspelet mellan tjänster
- **K8s-tester** - Kubernetes deployment-tester

### Snabbkommandon

```bash
# Miljöhantering
./scripts/run.sh create                      # Komplett setup
./scripts/run.sh delete                      # Ta bort allt
./scripts/k8s-debug.sh full-debug           # Felsöka problem

# Testning
./scripts/run-test.sh run-all                # Alla tester
./scripts/run-test.sh run-api                # API-tester
./scripts/run-test.sh run-gui                # GUI-tester
```

## 🌐 API-exempel

### Grundläggande API-anrop

```bash
# Health check
curl -X GET "http://localhost:8000/api/health"

# API-konfiguration
curl -X GET "http://localhost:8000/api/config"

# Statistik
curl -X GET "http://localhost:8000/api/stats"

# Swagger UI
open http://localhost:8000/docs
```

### Repository-hantering

```bash
# Hämta alla repositories
curl -X GET "http://localhost:8000/api/repositories/"

# Skapa ny repository
curl -X POST "http://localhost:8000/api/repositories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "test-repo", "format": "pypi", "type": "hosted"}'
```

👉 **[Se detaljerade API-exempel: API_EXAMPLES.md](API_EXAMPLES.md)**

## 📞 Support

- [Officiell Nexus-dokumentation](https://help.sonatype.com/repomanager3)
- [Docker Hub - Nexus3](https://hub.docker.com/r/sonatype/nexus3/)
- [Sonatype Community](https://community.sonatype.com/)

## 📄 Licens

Nexus Repository Manager OSS är licensierad under [Eclipse Public License 1.0](https://www.eclipse.org/legal/epl-v10.html).

---

**OBS**: Denna guide är avsedd för utvecklings- och testmiljöer. För produktionsmiljöer, se till att följa säkerhetsbest practices.
