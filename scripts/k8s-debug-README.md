# k8s-debug.sh - Debug och felsökningsskript

Detta är ett avancerat debug-skript för att felsöka Kubernetes-problem steg för steg. Det är designat för att hjälpa dig att identifiera och lösa problem med Nexus Repository Manager och FastAPI-applikationen i Kind-klustret.

## Översikt

`k8s-debug.sh` tillhandahåller:
- Detaljerad statuskontroll för alla komponenter
- Logganalys och felsökning
- Resursövervakning
- Nätverksdiagnostik
- Event-analys
- Health check-verifiering

## Användning

```bash
./scripts/k8s-debug.sh [KOMMANDO]
```

## Kommandon

### Komplett analys

#### `full-debug` - Kör alla debug-kommandon
Kör en fullständig analys av hela systemet:
- Kluster-status
- Pod-status för alla tjänster
- Events och loggar
- Resursanvändning
- Nätverksanslutningar
- Health checks

```bash
./scripts/k8s-debug.sh full-debug
```

### Statuskontroll

#### `cluster-status` - Kontrollera Kind-kluster
- Verifierar att Kind-klustret finns
- Visar kluster-information
- Listar noder och namespaces

```bash
./scripts/k8s-debug.sh cluster-status
```

#### `nexus-status` - Kontrollera Nexus
- Pod-status och tillstånd
- Services och deployments
- Persistent volumes
- Detaljerad pod-information

```bash
./scripts/k8s-debug.sh nexus-status
```

#### `api-status` - Kontrollera API
- API pod-status
- Services och ingress
- Deployment-status
- Pod-tillgänglighet

```bash
./scripts/k8s-debug.sh api-status
```

### Logganalys

#### `nexus-logs` - Visa Nexus-loggar
- Senaste 50 raderna av pod-loggar
- Deployment-loggar
- Felmeddelanden och varningar

```bash
./scripts/k8s-debug.sh nexus-logs
```

#### `api-logs` - Visa API-loggar
- API pod-loggar
- Deployment-loggar
- Startfel och konfigurationsproblem

```bash
./scripts/k8s-debug.sh api-logs
```

### Detaljerad analys

#### `nexus-describe` - Beskriv Nexus pod
- Detaljerad pod-beskrivning
- Events och status
- Resursbegränsningar
- Volume-mounts

```bash
./scripts/k8s-debug.sh nexus-describe
```

#### `api-describe` - Beskriv API pod
- API pod-detaljer
- Deployment-information
- Konfigurationsproblem
- Resursanvändning

```bash
./scripts/k8s-debug.sh api-describe
```

### Systemanalys

#### `events` - Visa Kubernetes events
- Alla events sorterade efter tid
- Namespace-specifika events
- Fel och varningar
- Pod-ändringar

```bash
./scripts/k8s-debug.sh events
```

#### `resources` - Visa resursanvändning
- Nod-resursanvändning
- Pod-resursanvändning
- CPU och minnesanvändning
- Resursbegränsningar

```bash
./scripts/k8s-debug.sh resources
```

#### `ports` - Kontrollera port-användning
- Port 8081 (Nexus) användning
- Port 3000 (API) användning
- Kind port-mapping
- Docker container-portar

```bash
./scripts/k8s-debug.sh ports
```

#### `images` - Visa Docker images
- Images i Kind-klustret
- Lokala Docker images
- Image-storlekar och taggar

```bash
./scripts/k8s-debug.sh images
```

#### `network` - Kontrollera nätverksanslutningar
- HTTP-anslutningar till tjänster
- Service-discovery
- Port-tillgänglighet
- Nätverkskonfiguration

```bash
./scripts/k8s-debug.sh network
```

#### `health` - Kontrollera health checks
- Pod-running status
- Readiness checks
- Liveness probes
- Service-tillgänglighet

```bash
./scripts/k8s-debug.sh health
```

## Felsökningsflöde

### 1. Snabb översikt
```bash
./scripts/k8s-debug.sh full-debug
```

### 2. Specifik komponent
```bash
# Om API inte fungerar
./scripts/k8s-debug.sh api-status
./scripts/k8s-debug.sh api-logs
./scripts/k8s-debug.sh api-describe

# Om Nexus inte fungerar
./scripts/k8s-debug.sh nexus-status
./scripts/k8s-debug.sh nexus-logs
./scripts/k8s-debug.sh nexus-describe
```

### 3. Systemnivå
```bash
# Kontrollera events
./scripts/k8s-debug.sh events

# Kontrollera resurser
./scripts/k8s-debug.sh resources

# Kontrollera nätverk
./scripts/k8s-debug.sh network
```

## Vanliga problem och lösningar

### API startar inte

1. **Kontrollera status:**
   ```bash
   ./scripts/k8s-debug.sh api-status
   ```

2. **Visa loggar:**
   ```bash
   ./scripts/k8s-debug.sh api-logs
   ```

3. **Beskriv pod:**
   ```bash
   ./scripts/k8s-debug.sh api-describe
   ```

**Vanliga orsaker:**
- Image pull-fel
- Resursbrist
- Port-konflikt
- Konfigurationsfel

### Nexus startar inte

1. **Kontrollera status:**
   ```bash
   ./scripts/k8s-debug.sh nexus-status
   ```

2. **Visa loggar:**
   ```bash
   ./scripts/k8s-debug.sh nexus-logs
   ```

3. **Beskriv pod:**
   ```bash
   ./scripts/k8s-debug.sh nexus-describe
   ```

**Vanliga orsaker:**
- Persistent volume-problem
- Resursbrist
- Konfigurationsfel
- Image pull-fel

### Nätverksproblem

1. **Kontrollera portar:**
   ```bash
   ./scripts/k8s-debug.sh ports
   ```

2. **Kontrollera nätverk:**
   ```bash
   ./scripts/k8s-debug.sh network
   ```

3. **Kontrollera services:**
   ```bash
   ./scripts/k8s-debug.sh api-status
   ./scripts/k8s-debug.sh nexus-status
   ```

## Output-tolkning

### Färgkodning
- **Blå** - Information
- **Grön** - Framgång
- **Gul** - Varningar
- **Röd** - Fel
- **Cyan** - Debug-information

### Status-indikatorer
- `Running` - Pod körs normalt
- `Pending` - Pod väntar på resurser
- `CrashLoopBackOff` - Pod kraschar kontinuerligt
- `ImagePullBackOff` - Kan inte hämta image
- `ErrImagePull` - Image pull-fel

### Event-typer
- `Normal` - Normal operation
- `Warning` - Varning
- `Failed` - Fel

## Avancerad felsökning

### Pod-problem
```bash
# Beskriv pod för detaljer
kubectl describe pod -n nexus-api -l app=nexus-api

# Följ loggar i realtid
kubectl logs -f -n nexus-api -l app=nexus-api

# Kör kommandon i pod
kubectl exec -it -n nexus-api -l app=nexus-api -- /bin/bash
```

### Service-problem
```bash
# Beskriv service
kubectl describe svc -n nexus-api nexus-api-service

# Testa service internt
kubectl port-forward -n nexus-api svc/nexus-api-service 3000:3000
```

### Nätverksproblem
```bash
# Testa DNS
kubectl run test-pod --image=busybox --rm -it -- nslookup nexus-api-service.nexus-api.svc.cluster.local

# Testa anslutning
kubectl run test-pod --image=busybox --rm -it -- wget -O- http://nexus-api-service.nexus-api.svc.cluster.local:3000/health
```

## Säkerhet

### Säkerhetskontroller
- Skriptet körs med användarens behörigheter
- Ingen root-åtkomst krävs
- Säker hantering av känslig information

### Bästa praxis
- Kör debug-kommandon i säker miljö
- Granska output innan delning
- Använd `full-debug` först för översikt

## Prestanda

### Optimering
- Skriptet använder effektiva kubectl-kommandon
- Parallell körning där möjligt
- Timeout-hantering för långsamma operationer

### Resursanvändning
- Minimal CPU-användning
- Effektiv minneshantering
- Snabb körning

## Support

### Felsökning
1. Kör `full-debug` först
2. Identifiera problemområde
3. Använd specifika kommandon
4. Granska loggar och events

### Hjälp
- Se `run-README.md` för huvudskript
- Kontrollera Kubernetes-dokumentation
- Granska Kind-dokumentation

## Licens

Detta skript är en del av Nexus Repository Manager-projektet och följer samma licens som huvudprojektet.
