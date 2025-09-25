# Felsökningsguide för Nexus Repository API Pip-paket

## Översikt

Denna guide hjälper dig att lösa vanliga problem när du arbetar med Nexus Repository API pip-paketet.

## Innehåll

- [Vanliga problem](#vanliga-problem)
- [Byggproblem](#byggproblem)
- [Upload-problem](#upload-problem)
- [Docker-problem](#docker-problem)
- [Kubernetes-problem](#kubernetes-problem)
- [Debug-kommandon](#debug-kommandon)

## Vanliga problem

### 1. Pip-paketet byggs inte korrekt

**Symptom:**
```
ERROR: Failed to build package
```

**Lösningar:**
1. Kontrollera att du är i rätt katalog:
   ```bash
   cd /Users/pnehlin/repo/nexus-lab/build-pip
   ```

2. Rensa och bygg om:
   ```bash
   rm -rf dist/ venv/ *.egg-info/
   ./scripts/build-pip.sh build
   ```

3. Kontrollera Python-version:
   ```bash
   python3 --version  # Ska vara 3.13+
   ```

### 2. Docker image byggs inte

**Symptom:**
```
ERROR: failed to solve: failed to read dockerfile
```

**Lösningar:**
1. Kontrollera att Dockerfile finns:
   ```bash
   ls -la Dockerfile
   ```

2. Bygg från rätt katalog (projektets root):
   ```bash
   cd /Users/pnehlin/repo/nexus-lab
   docker build -f Dockerfile -t nexus-api:latest .
   ```

3. Rensa Docker cache:
   ```bash
   docker system prune -f
   ```

### 3. API endpoint fungerar inte

**Symptom:**
```
{"detail":"Not Found"}
```

**Lösningar:**
1. Kontrollera att pip-paketet är uppdaterat:
   ```bash
   ./scripts/build-pip.sh build
   ./scripts/run.sh restart-api-local
   ```

2. Kontrollera att containern använder rätt version:
   ```bash
   kubectl exec -n nexus-api <pod-name> -- pip list | grep nexus
   ```

3. Kontrollera pod-loggarna:
   ```bash
   kubectl logs -n nexus-api <pod-name>
   ```

## Byggproblem

### Python-version konflikt

**Problem:** Containern använder fel Python-version

**Lösning:**
1. Kontrollera Dockerfile använder rätt version:
   ```dockerfile
   FROM python:3.13-slim
   ```

2. Bygg om pip-paketet med rätt Python-version:
   ```bash
   python3.13 -m build
   ```

### Dependency-problem

**Problem:** Paketberoenden kan inte installeras

**Lösning:**
1. Uppdatera pip till version 25.2:
   ```bash
   pip install --upgrade pip==25.2
   ```

2. Installera build-verktyg:
   ```bash
   pip install build twine
   ```

3. Kontrollera requirements.txt:
   ```bash
   cat build-pip/pyproject.toml
   ```

## Upload-problem

### GitLab Package Registry

**Problem:** 404 Not Found vid upload

**Lösningar:**
1. Kontrollera att Package Registry är aktiverat för projektet
2. Verifiera projekt-ID:
   ```bash
   echo $GITLAB_PROJECT_ID  # Ska vara 10
   ```

3. Kontrollera repository URL:
   ```bash
   echo "https://git.idp.ip-solutions.se/api/v4/projects/10/packages/pypi"
   ```

**Problem:** 401 Unauthorized

**Lösningar:**
1. Kontrollera GitLab token:
   ```bash
   echo $TWINE_PASSWORD
   ```

2. Använd rätt användarnamn:
   ```bash
   export TWINE_USERNAME="pnehlin"
   export TWINE_PASSWORD="your_gitlab_token"
   ```

3. Testa anslutning:
   ```bash
   curl -H "PRIVATE-TOKEN: $TWINE_PASSWORD" \
        "https://git.idp.ip-solutions.se/api/v4/projects/10"
   ```

### TestPyPI Upload

**Problem:** EOFError vid upload

**Lösning:**
Använd non-interactive mode:
```bash
twine upload --non-interactive --repository testpypi dist/*
```

## Docker-problem

### Port-konflikt

**Problem:** Port already allocated

**Lösning:**
1. Hitta vilken container som använder porten:
   ```bash
   docker ps | grep 3000
   ```

2. Stoppa containern:
   ```bash
   docker stop <container-id>
   ```

3. Eller använd annan port:
   ```bash
   docker run -p 3001:3000 nexus-api:latest
   ```

### Image cache-problem

**Problem:** Gamla ändringar visas inte

**Lösning:**
1. Tvinga ombyggnad:
   ```bash
   docker rmi -f nexus-api:latest
   docker build --no-cache -f Dockerfile -t nexus-api:latest .
   ```

2. Eller använd restart-kommandot:
   ```bash
   ./scripts/run.sh restart-api-local
   ```

## Kubernetes-problem

### Pod startar inte

**Problem:** Pod hänger i Pending eller CrashLoopBackOff

**Lösningar:**
1. Kontrollera pod-status:
   ```bash
   kubectl get pods -n nexus-api
   kubectl describe pod <pod-name> -n nexus-api
   ```

2. Kontrollera resurser:
   ```bash
   kubectl top nodes
   kubectl top pods -n nexus-api
   ```

3. Kontrollera events:
   ```bash
   kubectl get events -n nexus-api --sort-by='.lastTimestamp'
   ```

### Image pull problem

**Problem:** ImagePullBackOff

**Lösningar:**
1. Ladda image till Kind-klustret:
   ```bash
   kind load docker-image nexus-api:latest --name nexus-cluster
   ```

2. Kontrollera att image finns:
   ```bash
   docker images | grep nexus-api
   ```

### Service inte tillgänglig

**Problem:** API svarar inte via Kong Gateway

**Lösningar:**
1. Kontrollera Kong Gateway:
   ```bash
   kubectl get pods -n kong
   kubectl logs -n kong <kong-pod>
   ```

2. Kontrollera ingress:
   ```bash
   kubectl get ingress -n nexus-api
   kubectl describe ingress nexus-api-ingress -n nexus-api
   ```

3. Testa direkt mot pod:
   ```bash
   kubectl port-forward -n nexus-api <pod-name> 3000:3000
   curl http://localhost:3000/health
   ```

## Debug-kommandon

### Kontrollera pip-paket

```bash
# Lista installerade paket
pip list | grep nexus

# Kontrollera paketinformation
pip show nexus-repository-api

# Verifiera paketinnehåll
unzip -l build-pip/dist/nexus_repository_api-1.0.0-py3-none-any.whl
```

### Kontrollera Docker

```bash
# Lista images
docker images | grep nexus

# Kontrollera image-innehåll
docker run --rm nexus-api:latest pip list

# Kör container interaktivt
docker run -it --rm nexus-api:latest /bin/bash
```

### Kontrollera Kubernetes

```bash
# Pod-status
kubectl get pods -n nexus-api -o wide

# Pod-loggarna
kubectl logs -n nexus-api <pod-name> --tail=50

# Pod-beskrivning
kubectl describe pod <pod-name> -n nexus-api

# Service-status
kubectl get svc -n nexus-api

# Ingress-status
kubectl get ingress -n nexus-api
```

### Kontrollera API

```bash
# Health check
curl http://localhost:8000/api/health

# API-dokumentation
curl http://localhost:8000/api/docs

# Pip-paket information
curl http://localhost:8000/api/pip-package

# OpenAPI spec
curl http://localhost:8000/api/openapi.json | jq '.paths | keys'
```

## Vanliga kommandon

### Fullständig omstart

```bash
# Stoppa allt
./scripts/run.sh stop-all

# Rensa Docker
docker system prune -f

# Bygg om allt
./scripts/run.sh install-all-local
```

### Snabb felsökning

```bash
# Kontrollera status
./scripts/run.sh status

# Visa loggar
./scripts/run.sh get-logs

# Restart API
./scripts/run.sh restart-api-local
```

## Kontakt

Om du fortfarande har problem, kontrollera:

1. Alla loggar: `./scripts/run.sh get-logs`
2. System-status: `./scripts/run.sh status`
3. Docker-status: `docker ps -a`
4. Kubernetes-status: `kubectl get all -n nexus-api`

För mer detaljerad hjälp, se huvudprojektets README.md.
