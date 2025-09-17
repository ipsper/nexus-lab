# run.sh - Huvudhanteringsskript

Detta är det primära skriptet för att hantera Nexus Repository Manager och FastAPI-applikationen i Kind-klustret.

## Översikt

`run.sh` automatiserar alla operationer för att:
- Installera och konfigurera Kind-kluster
- Deploya Nexus Repository Manager
- Bygga och deploya FastAPI-applikation
- Hantera applikationer (starta, stoppa, omstarta)
- Skapa backups och återställa data
- Rensa systemet

## Användning

```bash
./scripts/run.sh [KOMMANDO]
```

## Kommandon

### Komplett setup (REKOMMENDERAT)

#### `create` - Skapa allt
Skapar hela systemet på en gång:
1. Installerar Kind (om inte redan installerat)
2. Skapar Kind-kluster
3. Deployar Nexus Repository Manager
4. Bygger API Docker image
5. Deployar FastAPI-applikation
6. Visar admin-lösenord och status

```bash
./scripts/run.sh create
```

#### `delete` - Ta bort allt
Tar bort hela systemet och rensar allt:
1. Stoppar alla applikationer
2. Tar bort alla namespaces
3. Tar bort Kind-kluster
4. Rensar Docker images
5. Rensar Docker system

```bash
./scripts/run.sh delete
```

### Grundläggande operationer

#### Kind-hantering
- `install-kind` - Installera Kind
- `create-cluster` - Skapa Kind-kluster

#### Nexus-hantering
- `deploy-nexus` - Deploya Nexus till klustret
- `start-nexus` - Alias för deploy-nexus
- `stop-nexus` - Stoppa Nexus
- `restart-nexus` - Starta om Nexus

#### API-hantering
- `build-api` - Bygg API Docker image
- `deploy-api` - Deploya API till klustret
- `start-api` - Alias för deploy-api
- `stop-api` - Stoppa API
- `restart-api` - Starta om API

### Övervakning och felsökning

#### Status och loggar
- `get-logs` - Visa Nexus-loggar
- `get-password` - Hämta admin-lösenord
- `check-status` - Kontrollera status på alla tjänster
- `port-forward` - Port-forward till Nexus

#### Backup och underhåll
- `backup` - Skapa backup av Nexus-data
- `restore <file>` - Återställ från backup
- `update-nexus` - Uppdatera Nexus-image
- `cleanup` - Rensa gamla artefakter

### Rensning
- `delete-cluster` - Ta bort Kind-kluster
- `delete-nexus` - Ta bort bara Nexus (behåll kluster)

## Exempel

### Snabbstart
```bash
# Komplett setup
./scripts/run.sh create

# Kontrollera status
./scripts/run.sh check-status

# Ta bort allt
./scripts/run.sh delete
```

### Steg-för-steg
```bash
# 1. Installera Kind
./scripts/run.sh install-kind

# 2. Skapa kluster
./scripts/run.sh create-cluster

# 3. Deploya Nexus
./scripts/run.sh deploy-nexus

# 4. Bygga och deploya API
./scripts/run.sh build-api
./scripts/run.sh deploy-api

# 5. Kontrollera status
./scripts/run.sh check-status
```

### Felsökning
```bash
# Visa loggar
./scripts/run.sh get-logs

# Kontrollera status
./scripts/run.sh check-status

# Hämta admin-lösenord
./scripts/run.sh get-password
```

## Funktioner

### Färgad output
- **Blå** - Information
- **Grön** - Framgång
- **Gul** - Varningar
- **Röd** - Fel

### Felhantering
- Automatisk avslutning vid fel (`set -e`)
- Validering av beroenden
- Säkerhetskontroller för destruktiva operationer

### Plattformsstöd
- **macOS**: Homebrew och manuell installation
- **Linux**: Manuell installation från GitHub

### Timeout-hantering
- Väntar på pod-ready med timeout
- Automatisk omstart vid fel

## Miljövariabler

Skriptet använder följande miljövariabler:
- `KUBECONFIG` - Kubernetes konfigurationsfil
- `DOCKER_HOST` - Docker daemon-anslutning

## Säkerhet

### Säkerhetskontroller
- Bekräftelse innan destruktiva operationer
- Validering av användarinput
- Säker hantering av lösenord

### Bästa praxis
- Kör inte som root
- Kontrollera miljö innan körning
- Backup innan större ändringar

## Felsökning

### Vanliga problem

1. **Skriptet är inte körbart**
   ```bash
   chmod +x scripts/run.sh
   ```

2. **Kind är inte installerat**
   ```bash
   ./scripts/run.sh install-kind
   ```

3. **Kubectl är inte installerat**
   - Installera kubectl först
   - Kontrollera att det är i PATH

4. **Port-konflikter**
   ```bash
   # Kontrollera port-användning
   lsof -i :8081
   lsof -i :3000
   ```

### Debug-kommandon

För avancerad felsökning, använd `k8s-debug.sh`:
```bash
./scripts/k8s-debug.sh full-debug
```

## Utveckling

### Lägga till nya kommandon

1. Lägg till funktion i skriptet
2. Lägg till case i huvudlogiken
3. Uppdatera hjälptexten
4. Testa funktionaliteten

### Testning

```bash
# Testa hjälp
./scripts/run.sh help

# Testa status
./scripts/run.sh check-status

# Testa fullständig debug
./scripts/k8s-debug.sh full-debug
```

## Licens

Detta skript är en del av Nexus Repository Manager-projektet och följer samma licens som huvudprojektet.

## Support

För problem eller frågor:
1. Kör `./scripts/k8s-debug.sh full-debug`
2. Granska output för felmeddelanden
3. Kontrollera loggar
4. Se `k8s-debug-README.md` för avancerad felsökning
