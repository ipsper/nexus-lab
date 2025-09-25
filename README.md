# Nexus Repository Manager - Container Installation Guide

Denna guide visar hur du installerar och konfigurerar en Nexus Repository Manager i en Docker-container för att lagra olika typer av paket och artefakter.

## Översikt

Nexus Repository Manager är en kraftfull artefakt-hantering som stöder:
- **Python pip-paket** (PyPI)
- **APT-paket** (Debian/Ubuntu)
- **RPM-paket** (Red Hat/CentOS)
- **Docker-containers** (Docker Registry)
- **Maven, npm, NuGet** och många fler format

## Förutsättningar

- Docker installerat på systemet
- Kind (Kubernetes in Docker) installerat
- kubectl installerat
- Minst 4GB RAM tillgängligt
- Minst 20GB ledigt diskutrymme

## 📦 Pip-paket Distribution

FastAPI-applikationen kan också distribueras som ett pip-paket för enklare installation och användning:

👉 **[Se detaljerad guide: build-pip/README.md](build-pip/README.md)**  
🔧 **[Felsökningsguide: build-pip/TROUBLESHOOTING.md](build-pip/TROUBLESHOOTING.md)**

### Snabbstart med pip-paket

```bash
# Bygg pip-paketet
./scripts/build-pip.sh build

# Bygg Docker-image med pip-paketet
./scripts/build-pip.sh docker

# Installera lokalt för testning
./scripts/build-pip.sh install

# Starta applikationen
nexus-api --port 3000
```

## Snabbstart med Kind

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

### 1. Installera Kind

```bash
# macOS med Homebrew
brew install kind

# Eller ladda ner från GitHub
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-darwin-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### 2. Skapa Kind-kluster

```bash
# Skapa ett Kind-kluster med port-forwarding
kind create cluster --name nexus-cluster --config k8s/kind-config.yaml
```

### 3. Skapa Kind-konfigurationsfil

Skapa `k8s/kind-config.yaml`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: nexus-cluster
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  - containerPort: 30080
    hostPort: 8081
    protocol: TCP
```

### 4. Skapa Kubernetes-manifester

Skapa `k8s/nexus-deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nexus
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nexus-data
  namespace: nexus
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
  namespace: nexus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nexus
  template:
    metadata:
      labels:
        app: nexus
    spec:
      containers:
      - name: nexus
        image: sonatype/nexus3:latest
        ports:
        - containerPort: 8081
        env:
        - name: INSTALL4J_ADD_VM_PARAMS
          value: "-Xms2g -Xmx2g -XX:MaxDirectMemorySize=3g"
        volumeMounts:
        - name: nexus-data
          mountPath: /nexus-data
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "1000m"
      volumes:
      - name: nexus-data
        persistentVolumeClaim:
          claimName: nexus-data
---
apiVersion: v1
kind: Service
metadata:
  name: nexus-service
  namespace: nexus
spec:
  selector:
    app: nexus
  ports:
  - port: 8081
    targetPort: 8081
    nodePort: 30080
  type: NodePort
```

### 5. Deploya Nexus

```bash
# Deploya Nexus till Kind-klustret
kubectl apply -f k8s/nexus-deployment.yaml

# Kontrollera att podden startar
kubectl get pods -n nexus -w

# Följ loggarna
kubectl logs -f deployment/nexus -n nexus
```

### 6. Vänta på att servern startar

Nexus tar några minuter att starta första gången. Du kan följa förloppet med:

```bash
kubectl logs -f deployment/nexus -n nexus
```

När servern är redo ser du meddelandet: `Started Sonatype Nexus`

## Konfiguration

### 1. Åtkomst till webbgränssnittet

Öppna din webbläsare och gå till: `http://localhost:8081`

### 2. Hämta admin-lösenordet

```bash
# Hitta admin-lösenordet
kubectl exec -n nexus deployment/nexus -- cat /nexus-data/admin.password
```

### 3. Logga in

- Användarnamn: `admin`
- Lösenord: (kopiera från steg 2 ovan)
- Följ guiden för att skapa ett nytt lösenord

## Konfigurera Repository-format

### Python (PyPI) Repository

1. Gå till **Settings** → **Repositories**
2. Klicka **Create repository**
3. Välj **pypi (hosted)**
4. Konfigurera:
   - **Name**: `pypi-hosted`
   - **Version policy**: `Mixed`
   - **Storage**: `Default`

### APT Repository

1. Gå till **Settings** → **Repositories**
2. Klicka **Create repository**
3. Välj **apt (hosted)**
4. Konfigurera:
   - **Name**: `apt-hosted`
   - **Distribution**: `stable`
   - **Signing key**: (generera ny eller använd befintlig)

### RPM Repository

1. Gå till **Settings** → **Repositories**
2. Klicka **Create repository**
3. Välj **yum (hosted)**
4. Konfigurera:
   - **Name**: `rpm-hosted`
   - **Version policy**: `Mixed`

### Docker Registry

1. Gå till **Settings** → **Repositories**
2. Klicka **Create repository**
3. Välj **docker (hosted)**
4. Konfigurera:
   - **Name**: `docker-hosted`
   - **HTTP**: `8082` (eller annan port)
   - **Enable Docker V1 API**: `true`

## Användning

### Python (pip)

```bash
# Konfigurera pip för att använda Nexus
pip install --index-url http://localhost:8081/repository/pypi-hosted/simple/ package-name

# Eller skapa ~/.pip/pip.conf:
[global]
index-url = http://localhost:8081/repository/pypi-hosted/simple/
trusted-host = localhost
```

### APT (Debian/Ubuntu)

```bash
# Lägg till Nexus som APT-källa
echo "deb http://localhost:8081/repository/apt-hosted/ stable main" | sudo tee /etc/apt/sources.list.d/nexus.list

# Uppdatera paketlistan
sudo apt update
```

### RPM (Red Hat/CentOS)

```bash
# Skapa repo-fil
sudo tee /etc/yum.repos.d/nexus.repo << EOF
[nexus]
name=Nexus Repository
baseurl=http://localhost:8081/repository/rpm-hosted/
enabled=1
gpgcheck=0
EOF

# Installera paket
sudo yum install package-name
```

### Docker

```bash
# Konfigurera Docker för att använda Nexus
docker login localhost:8082

# Tagga och pusha images
docker tag myimage:latest localhost:8082/docker-hosted/myimage:latest
docker push localhost:8082/docker-hosted/myimage:latest

# Hämta images
docker pull localhost:8082/docker-hosted/myimage:latest
```

## Avancerad konfiguration

### Backup och återställning

```bash
# Backup av data
kubectl exec -n nexus deployment/nexus -- tar czf /tmp/nexus-backup.tar.gz -C /nexus-data .
kubectl cp nexus/$(kubectl get pods -n nexus -l app=nexus -o jsonpath='{.items[0].metadata.name}'):/tmp/nexus-backup.tar.gz ./nexus-backup.tar.gz

# Återställning
kubectl cp ./nexus-backup.tar.gz nexus/$(kubectl get pods -n nexus -l app=nexus -o jsonpath='{.items[0].metadata.name}'):/tmp/nexus-backup.tar.gz
kubectl exec -n nexus deployment/nexus -- tar xzf /tmp/nexus-backup.tar.gz -C /nexus-data
```

### SSL/TLS-konfiguration

För produktionsmiljöer, konfigurera SSL:

```yaml
# I k8s/nexus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
  namespace: nexus
spec:
  template:
    spec:
      containers:
      - name: nexus
        # ... existing config ...
        volumeMounts:
        - name: nexus-data
          mountPath: /nexus-data
        - name: ssl-certs
          mountPath: /opt/sonatype/nexus/etc/ssl
        env:
        - name: INSTALL4J_ADD_VM_PARAMS
          value: "-Djavax.net.ssl.trustStore=/opt/sonatype/nexus/etc/ssl/truststore.jks"
      volumes:
      - name: nexus-data
        persistentVolumeClaim:
          claimName: nexus-data
      - name: ssl-certs
        secret:
          secretName: nexus-ssl-certs
```

### Prestanda-optimering

```yaml
# För produktionsmiljöer i k8s/nexus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus
  namespace: nexus
spec:
  template:
    spec:
      containers:
      - name: nexus
        env:
        - name: INSTALL4J_ADD_VM_PARAMS
          value: "-Xms4g -Xmx4g -XX:MaxDirectMemorySize=6g"
        resources:
          requests:
            memory: "4Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "2000m"
```

## Felsökning

### Snabb felsökning

För snabb felsökning, använd debug-skriptet:
```bash
# Kör fullständig debug-analys
./scripts/k8s-debug.sh full-debug

# Felsöka specifika komponenter
./scripts/k8s-debug.sh api-status
./scripts/k8s-debug.sh nexus-status
./scripts/k8s-debug.sh api-logs
./scripts/k8s-debug.sh events
```

**Se:** [k8s-debug.sh README](scripts/k8s-debug-README.md) för detaljerad felsökningsguide.

### Vanliga problem

1. **Pod startar inte**
   ```bash
   # Använd debug-skriptet
   ./scripts/k8s-debug.sh api-status
   ./scripts/k8s-debug.sh api-describe
   ./scripts/k8s-debug.sh events
   ```

2. **Åtkomst nekad**
   ```bash
   # Kontrollera nätverk
   ./scripts/k8s-debug.sh network
   ./scripts/k8s-debug.sh ports
   
   # Kontrollera services
   ./scripts/k8s-debug.sh api-status
   ./scripts/k8s-debug.sh nexus-status
   ```

3. **Långsam prestanda**
   ```bash
   # Kontrollera resurser
   ./scripts/k8s-debug.sh resources
   
   # Öka resurser i k8s/nexus-deployment.yaml
   kubectl apply -f k8s/nexus-deployment.yaml
   ```

### Loggar och övervakning

```bash
# Använd debug-skriptet för loggar
./scripts/k8s-debug.sh api-logs
./scripts/k8s-debug.sh nexus-logs

# Eller använd kubectl direkt
kubectl logs -f deployment/nexus -n nexus
kubectl logs -f deployment/nexus-api -n nexus-api
```

## Säkerhet

### Grundläggande säkerhetsåtgärder

1. **Ändra standardlösenord** omedelbart
2. **Aktivera anonym åtkomst** endast för publika repositories
3. **Konfigurera användarroller** och behörigheter
4. **Använd HTTPS** i produktionsmiljöer
5. **Regelbundna backups** av konfiguration och data

### Användarhantering

1. Gå till **Settings** → **Security** → **Users**
2. Skapa användare med specifika roller
3. Konfigurera LDAP/Active Directory (valfritt)

## Underhåll

### Uppdateringar

```bash
# Uppdatera image i deployment
kubectl set image deployment/nexus nexus=sonatype/nexus3:latest -n nexus

# Kontrollera rollout-status
kubectl rollout status deployment/nexus -n nexus

# Om något går fel, rollback
kubectl rollout undo deployment/nexus -n nexus
```

### Rensning av gamla artefakter

1. Gå till **Settings** → **Repositories**
2. Välj repository → **Cleanup policies**
3. Konfigurera regler för borttagning av gamla artefakter

### Ta bort Kind-klustret

```bash
# Ta bort hela Kind-klustret
kind delete cluster --name nexus-cluster

# Eller ta bort bara Nexus-deploymentet
kubectl delete namespace nexus
```

## 📚 Dokumentation och Guider

Projektet innehåller omfattande dokumentation för alla komponenter:

### 🎯 Huvudguider
- **[📋 Scripts Guide](scripts/README.md)** - Översikt av alla scripts och verktyg
- **[🔧 run.sh Guide](scripts/run-README.md)** - Huvudhanteringsskript för installation och konfiguration
- **[🐛 k8s-debug.sh Guide](scripts/k8s-debug-README.md)** - Avancerat debug-skript för felsökning
- **[🧪 Testsystem Guide](testning/README.md)** - Komplett guide för testsystemet
- **[🚀 App Guide](app/README.md)** - FastAPI-applikationens struktur och endpoints

### 🧪 Testsystem
Projektet har ett omfattande testsystem med:
- **Health checks** - Kontrollerar miljöns status
- **API-tester** - Testar REST endpoints
- **GUI-tester** - Playwright-baserade UI-tester  
- **Integration-tester** - Testar samspelet mellan tjänster
- **K8s-tester** - Kubernetes deployment-tester
- **🆕 Smart endpoint-tester** - Dynamisk validering av API endpoints

**➡️ [Läs hela testguiden](testning/README.md)** för detaljerad information om:
- Hur man kör olika typer av tester
- Docker exec arkitektur
- Verbose mode och debugging
- --to-the-end flaggor
- Playwright GUI-testning
- Nya smarta endpoint-URL tester

### Snabböversikt

**Snabbkommandon:**
```bash
# Miljöhantering
./scripts/run.sh create                      # Komplett setup
./scripts/run.sh delete                      # Ta bort allt
./scripts/k8s-debug.sh full-debug           # Felsöka problem

# Testning
./scripts/run-test.sh run-health             # Health checks
./scripts/run-test.sh run-api                # API-tester (utan GUI)
./scripts/run-test.sh run-gui                # GUI-tester
./scripts/run-test.sh run-endpoints          # 🆕 Smarta endpoint-URL tester
./scripts/test.sh all                        # Alla tester

# Testning mot annan miljö
TEST_HOST=192.168.1.100 ./scripts/run-test.sh run-api    # Annan host
TEST_PORT=9000 ./scripts/run-test.sh run-gui             # Annan port
```

**📖 Detaljerade guider:**
- **[🔧 run.sh README](scripts/run-README.md)** - Komplett guide för huvudskriptet
- **[🐛 k8s-debug.sh README](scripts/k8s-debug-README.md)** - Avancerad felsökningsguide  
- **[🧪 Testsystem README](testning/README.md)** - Komplett testguide med konfigurerbara URL:er
- **[🚀 App README](app/README.md)** - FastAPI-applikationens struktur och endpoints

### 🎯 Snabbkommandon per README

**📋 [Scripts Guide](scripts/README.md)**
```bash
./scripts/run.sh help                        # Visa alla kommandon
./scripts/k8s-debug.sh help                  # Debug-kommandon
./scripts/run-test.sh help                   # Test-kommandon
```

**🔧 [run.sh Guide](scripts/run-README.md)**
```bash
./scripts/run.sh create                      # Komplett setup
./scripts/run.sh restart-api-local           # Bygg om och starta API
./scripts/run.sh status                      # Visa status
./scripts/run.sh logs                        # Visa loggar
```

**🐛 [k8s-debug.sh Guide](scripts/k8s-debug-README.md)**
```bash
./scripts/k8s-debug.sh full-debug           # Komplett debug-analys
./scripts/k8s-debug.sh api-status           # API-status
./scripts/k8s-debug.sh nexus-status         # Nexus-status
./scripts/k8s-debug.sh network              # Nätverksdiagnostik
```

**🧪 [Testsystem Guide](testning/README.md)**
```bash
./scripts/run-test.sh run-health             # Health checks
./scripts/run-test.sh run-api                # API-tester
./scripts/run-test.sh run-gui                # GUI-tester
./scripts/run-test.sh run-endpoints          # Smarta endpoint-tester
./scripts/run-test.sh run-k8s                # K8s-tester
```

**🚀 [App Guide](app/README.md)**
```bash
# Lokal utveckling
cd app && python -m uvicorn main:app --reload

# Testa endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/docs
```

**📦 [Pip-paket Guide](build-pip/README.md)**
```bash
./scripts/build-pip.sh build                # Bygg pip-paket
./scripts/build-pip.sh docker               # Bygg Docker-image
./scripts/build-pip.sh install              # Installera lokalt
nexus-api --port 3000                       # Starta applikation
```

### Skriptfunktioner:

#### run.sh (Huvudskript)
- **Färgad output** för bättre läsbarhet
- **Felhantering** med automatisk avslutning vid fel
- **Säkerhetskontroller** innan destruktiva operationer
- **Plattformsdetektering** för automatisk Kind-installation
- **Timeout-hantering** för långsamma operationer
- **Backup/återställning** med tidsstämplar

#### k8s-debug.sh (Debug-skript)
- **Detaljerad statuskontroll** för alla komponenter
- **Logganalys** och felsökning
- **Resursövervakning** och prestanda
- **Nätverksdiagnostik** och anslutningstester
- **Event-analys** för att identifiera problem
- **Health check-verifiering** för alla tjänster

#### run-test.sh (Testsystem)
- **Konfigurerbara URL:er** via miljövariabler (TEST_HOST, TEST_PORT)
- **Persistent Docker-container** med docker exec för snabbare tester
- **Separata testtyper**: Health, API, GUI, K8s, Endpoints
- **Stop-on-failure** som standard med `--to-the-end` flagga
- **Playwright GUI-tester** med Chromium, Firefox support
- **🆕 Smarta endpoint-tester** med dynamisk validering
- **Automatisk miljökonfiguration** visas vid container-start

## Support och dokumentation

- [Officiell Nexus-dokumentation](https://help.sonatype.com/repomanager3)
- [Docker Hub - Nexus3](https://hub.docker.com/r/sonatype/nexus3/)
- [Sonatype Community](https://community.sonatype.com/)
- [Pip-paket Guide](build-pip/README.md) - Detaljerad guide för att bygga och distribuera FastAPI-appen som pip-paket
- [Pip-paket Felsökning](build-pip/TROUBLESHOOTING.md) - Omfattande felsökningsguide för pip-paket och Docker-problem

## Licens

Nexus Repository Manager OSS är licensierad under [Eclipse Public License 1.0](https://www.eclipse.org/legal/epl-v10.html).

---

**OBS**: Denna guide är avsedd för utvecklings- och testmiljöer. För produktionsmiljöer, se till att följa säkerhetsbest practices och överväg att använda en hanterad lösning.
