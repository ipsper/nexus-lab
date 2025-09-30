# 🚀 Snabbstart - Frontend + Backend med Kind

Denna guide visar hur du snabbt startar både React frontend och FastAPI backend med Kind-klustret.

## 📋 Förutsättningar

### Backend (Kind-kluster)
- Docker installerat
- Kind (Kubernetes in Docker) installerat
- kubectl installerat
- Minst 4GB RAM tillgängligt

### Frontend (React-applikation)
- Node.js 18+ installerat
- npm eller yarn

## 🚀 Steg-för-steg installation

### Steg 1: Komplett Setup (Rekommenderat)

```bash
# Gå till projektets root-mapp
cd /Users/pnehlin/repo/nexus-lab

# Komplett setup - skapar kluster och deployar allt på en gång
./scripts/run.sh setup

# Detta kommer att:
# ✅ Installera Kind (om inte redan installerat)
# ✅ Skapa Kind-kluster
# ✅ Deploya Nexus Repository Manager
# ✅ Deploya Kong Gateway
# ✅ Bygga backend (lokal build)
# ✅ Deploya backend till klustret
# ✅ Bygga frontend (lokal build)
# ✅ Deploya frontend till klustret
# ✅ Visa admin-lösenord och status

# Vänta tills allt är klart (ca 5-7 minuter)
```

### Alternativ: Steg-för-steg Setup

```bash
# Steg 1: Skapa kluster
./scripts/run.sh create

# Steg 2: Deploya applikationer
./scripts/run.sh deploy-all

# Eller deploya separat:
# ./scripts/run.sh deploy-backend   # Bara backend
# ./scripts/run.sh deploy-frontend  # Bara frontend
```

### Alternativ: Starta bara Frontend

```bash
# Om backend redan körs, starta bara frontend
./scripts/run.sh start-frontend

# Eller manuellt
cd frontend
npm install
npm run dev
```

### Steg 3: Verifiera installationen

Öppna webbläsaren och gå till:

- **Frontend**: `http://localhost:8000` - React-applikation med IP-Solutions design
- **Backend API**: `http://localhost:8000/api/health` - FastAPI health check
- **Swagger UI**: `http://localhost:8000/docs` - API-dokumentation
- **Nexus UI**: `http://localhost:8081` - Repository Manager

## 🎯 Vad du får

### Frontend (React)
- **Dashboard** - Systemöversikt med health status och statistik
- **Repositories** - Hantera paketarkiv (PyPI, Docker, Maven, etc.)
- **Schedules** - Automatiska schemaläggningar
- **Statistics** - Detaljerad statistik och analytics
- **Settings** - Systemkonfiguration

### Backend (FastAPI)
- **REST API** - Komplett API för repository-hantering
- **Health checks** - Systemövervakning
- **Swagger UI** - Interaktiv API-dokumentation
- **Kong Gateway** - API-gateway med routing

### Kind-kluster
- **Nexus Repository Manager** - Artefakt-hantering
- **FastAPI** - Backend API
- **Kong Gateway** - API-gateway
- **Kubernetes** - Container-orchestrering

## 🔧 Utveckling

### Frontend utveckling

```bash
cd frontend

# Starta utvecklingsserver med hot reload
npm run dev

# Bygga för produktion
npm run build

# Bygga som npm-paket
npm run build:lib
```

### Backend utveckling (Kind-kluster)

```bash
# Bygga om API efter ändringar
./scripts/run.sh rebuild-api

# Felsöka API
./scripts/k8s-debug.sh api-status

# Visa API-loggar
kubectl logs -n nexus-api deployment/nexus-api

# Felsöka Kind-kluster
./scripts/k8s-debug.sh full-debug
```

## 🧪 Testning

```bash
# Kör alla tester
./scripts/run-test.sh run-all

# Kör specifika tester
./scripts/run-test.sh run-api
./scripts/run-test.sh run-gui
```

## 🛑 Stoppa allt

```bash
# Stoppa frontend
# Tryck Ctrl+C i terminalen där npm run dev körs

# Stoppa backend och ta bort Kind-kluster
./scripts/run.sh delete
```

## 🐛 Felsökning

### Frontend startar inte

```bash
# Kontrollera Node.js version
node --version  # Ska vara 18+

# Installera om dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend startar inte

```bash
# Felsöka Kind-kluster
./scripts/k8s-debug.sh full-debug

# Kontrollera Kind-kluster
kind get clusters
kubectl get nodes

# Kontrollera Docker
docker ps
docker images
```

### API-svar inte

```bash
# Kontrollera Kong Gateway
kubectl get pods -n kong

# Kontrollera API
kubectl get pods -n nexus-api

# Testa direkt
curl http://localhost:8000/api/health
```

## 📚 Ytterligare resurser

- **[Huvud-README](README.md)** - Komplett dokumentation
- **[Frontend Guide](frontend/README.md)** - Detaljerad frontend-dokumentation
- **[Backend Guide](build-pip/nexus_repository_api/README.md)** - API-dokumentation
- **[Testsystem Guide](testning/README.md)** - Testning och kvalitetssäkring

## 🎉 Klar!

Du har nu en fullständig React frontend + FastAPI backend lösning som körs i Kind-klustret med professionell IP-Solutions design!
