# Nexus Lab - Test Suite

Detta är en omfattande testsvit för Nexus Lab-projektet som testar FastAPI-applikationen, Kong Gateway, Nexus Repository Manager och Kubernetes-integrationen.

## 🚀 Snabbstart

```bash
# 1. Starta tjänsterna
./scripts/run.sh create

# 2. Kör alla tester
./scripts/test.sh all

# 3. Öppna testrapport
open testning/report.html
```

## 📋 Testkommandon

### Gemensamt Interface
```bash
# Kör alla tester (rekommenderat)
./scripts/test.sh all

# Kör bara API-tester (Docker-container)
./scripts/test.sh api

# Kör bara K8s-tester (host-system)
./scripts/test.sh k8s

# Kör specifika tester
./scripts/test.sh api -k test_fastapi
./scripts/test.sh k8s --tb=long
```

### Separata Scripts (avancerat)
```bash
# API/Integration-tester i Docker
./scripts/run-test.sh run

# K8s-tester på host
./scripts/run-k8s-tests.sh run
```

## 🏗️ Testarkitektur

### Två Separata Testmiljöer

**1. Docker-Container (Externa Tester)**
- Testar systemet som en extern klient
- Använder `host.docker.internal` för att nå tjänster
- Kör: API, Kong Gateway, Nexus integration-tester
- Ingen kubectl-tillgång (avsiktligt isolerad)

**2. Host-System (K8s-Tester)**
- Testar Kubernetes-resurser direkt
- Använder kubectl för att inspektera klustret
- Egen isolerad venv (`k8s-test-venv/`)
- Kör: Pod-status, service-tillgänglighet, kluster-hälsa

## 📁 Teststruktur

```
testning/
├── test/                              # Wrapper-funktioner för tester
│   ├── test_fastapi_basic.py         # FastAPI endpoint-tester
│   ├── test_k8s_integration.py       # Kubernetes-tester (@pytest.mark.k8s)
│   ├── test_kong_gateway.py          # Kong Gateway-tester  
│   └── test_nexus_integration.py     # Nexus Repository Manager-tester
├── support/                           # Faktiska testfunktioner
│   ├── api_client.py                 # HTTP API-klient
│   ├── k8s_helper.py                 # Kubernetes-hjälpfunktioner
│   ├── fastapi_support.py            # FastAPI testlogik
│   ├── k8s_support.py                # Kubernetes testlogik
│   ├── kong_support.py               # Kong Gateway testlogik
│   └── nexus_support.py              # Nexus testlogik
├── conftest.py                        # Pytest fixtures och konfiguration
├── pytest.ini                        # Pytest-inställningar (exkluderar k8s-tester)
├── requirements.txt                   # Python-dependencies för Docker
├── Dockerfile                         # Container-definition
└── README.md                          # Denna fil
```

## 🎯 Testkategorier

### 🌐 API-Tester (Docker)
**Körs i:** Docker-container som extern klient  
**Testar:** HTTP-endpoints via Kong Gateway

- **FastAPI Basic Tests** - Root, health, docs, OpenAPI endpoints
- **Kong Gateway Tests** - Routing, health, konfiguration  
- **Nexus Integration Tests** - Repository Manager via Kong

**Markers:** `@pytest.mark.api`, `@pytest.mark.integration`

### ⚙️ K8s-Tester (Host)
**Körs på:** Host-system med kubectl-tillgång  
**Testar:** Kubernetes-resurser direkt

- **Cluster Status** - Kluster körs korrekt
- **Pod Health** - Alla pods är Running och Ready
- **Service Availability** - Services är tillgängliga
- **Resource Status** - Deployments och tjänster fungerar

**Markers:** `@pytest.mark.k8s`, `@pytest.mark.integration`

## 🔧 Konfiguration

### Pytest-inställningar
```ini
# pytest.ini
addopts = -m "not k8s"  # Exkluderar K8s-tester från Docker-körning
```

### Service URLs (Auto-detekterar miljö)
```python
# conftest.py - Automatisk miljödetektering
host = "host.docker.internal" if os.path.exists("/.dockerenv") else "localhost"

# URLs via Kong Gateway
api_base_url = f"http://{host}:8000/api"
kong_base_url = f"http://{host}:8000" 
nexus_base_url = f"http://{host}:8000/nexus"
```

## 📊 Test-markers

```python
@pytest.mark.api          # API endpoint-tester
@pytest.mark.integration  # Integrationstester
@pytest.mark.k8s          # Kubernetes-tester (endast host)
@pytest.mark.slow         # Långsamma tester
@pytest.mark.unit         # Unit-tester
```

## 🐳 Docker-testning

### Automatisk Container-byggning
```bash
# Bygger automatiskt nexus-test:latest
./scripts/run-test.sh build

# Kör tester i container
./scripts/run-test.sh run
```

### Container-funktioner
- **Isolerad miljö** - Ingen påverkan på host-system
- **Host-nätverksåtkomst** - Kan nå Kong Gateway på host
- **Automatisk rapport** - Genererar HTML-rapport
- **Miljödetektering** - Använder `host.docker.internal` automatiskt

## ⚙️ K8s-testning

### Automatisk Venv-hantering
```bash
# Skapar automatiskt k8s-test-venv/ och installerar dependencies
./scripts/run-k8s-tests.sh run

# Rensa venv
./scripts/run-k8s-tests.sh clean
```

### Krav för K8s-tester
- `kubectl` installerat och konfigurerat
- Kind-kluster `nexus-cluster` körs
- Tillgång till Kubernetes API

## 📈 Rapporter

### HTML-rapport
```bash
# Genereras automatiskt efter test-körning
open testning/report.html
```

### Rapport innehåller:
- ✅ Antal passerade/misslyckade tester
- 📊 Teststatistik per kategori  
- 🕒 Körningstider
- 📝 Detaljerade felmeddelanden
- 🔍 Testresultat per endpoint

## 🚨 Felsökning

### Docker-tester misslyckas
```bash
# Kontrollera att tjänsterna körs
curl http://localhost:8000/api/health

# Kontrollera Docker-container
./scripts/run-test.sh build --no-cache
```

### K8s-tester misslyckas
```bash
# Kontrollera kluster-status
kubectl cluster-info --context kind-nexus-cluster

# Kontrollera pods
kubectl get pods --all-namespaces

# Kontrollera miljön
./scripts/run-k8s-tests.sh check
```

### Vanliga problem

**"Connection refused"**
- Tjänsterna är inte startade: `./scripts/run.sh create`
- Kong Gateway inte tillgänglig: Kontrollera NodePort-mappningar

**"kubectl not found"**
- Installera kubectl eller använd bara API-tester: `./scripts/test.sh api`

**"No module named pytest"**
- Docker: Bygg om imagen: `./scripts/run-test.sh build`
- Host: Installeras automatiskt i venv

## 🎯 Best Practices

### Test-utveckling
- **Wrapper-funktioner** i `test/` - håller tester enkla
- **Testlogik** i `support/` - återanvändbar kod
- **Fixtures** i `conftest.py` - gemensam setup
- **Markers** för kategorisering och filtrering

### Körning
- Använd `./scripts/test.sh all` för komplett testning
- Använd `./scripts/test.sh api` för snabb feedback
- Använd specifika markers för fokuserad testning

### Miljöhantering
- Docker-tester: Automatisk isolation
- K8s-tester: Automatisk venv-hantering  
- Inga manuella installations-steg krävs

## 🔗 Relaterade Scripts

- `./scripts/run.sh` - Hantera Kind-kluster och tjänster
- `./scripts/test.sh` - Gemensamt test-interface (REKOMMENDERAT)
- `./scripts/run-test.sh` - Docker-tester direkt
- `./scripts/run-k8s-tests.sh` - K8s-tester direkt