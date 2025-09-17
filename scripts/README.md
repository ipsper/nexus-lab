# Scripts Directory

Denna mapp innehåller alla skript för att hantera Nexus Repository Manager och FastAPI-applikationen i Kind-klustret.

## Skript

### 1. `run.sh` - Huvudhanteringsskript
Det primära skriptet för att installera, konfigurera och hantera hela systemet.

**Användning:**
```bash
./scripts/run.sh [KOMMANDO]
```

**Huvudkommandon:**
- `create` - Komplett setup (kluster + applikationer)
- `delete` - Ta bort allt och rensa systemet
- `check-status` - Kontrollera status på alla tjänster
- `get-logs` - Visa loggar
- `get-password` - Hämta admin-lösenord

**Se:** [run.sh README](run-README.md) för detaljerad dokumentation.

### 2. `k8s-debug.sh` - Debug och felsökning
Avancerat debug-skript för att felsöka Kubernetes-problem steg för steg.

**Användning:**
```bash
./scripts/k8s-debug.sh [KOMMANDO]
```

**Debug-kommandon:**
- `full-debug` - Kör alla debug-kommandon
- `api-status` - Kontrollera API status
- `nexus-status` - Kontrollera Nexus status
- `api-logs` - Visa API loggar
- `events` - Visa Kubernetes events

**Se:** [k8s-debug.sh README](k8s-debug-README.md) för detaljerad dokumentation.

## Snabbstart

### Komplett setup:
```bash
# Gör skripten körbara
chmod +x scripts/*.sh

# Skapa allt
./scripts/run.sh create

# Felsöka om problem uppstår
./scripts/k8s-debug.sh full-debug

# Ta bort allt när klar
./scripts/run.sh delete
```

### Steg-för-steg:
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

## Felsökning

Om något inte fungerar som förväntat:

1. **Kör fullständig debug:**
   ```bash
   ./scripts/k8s-debug.sh full-debug
   ```

2. **Kontrollera specifika komponenter:**
   ```bash
   ./scripts/k8s-debug.sh api-status
   ./scripts/k8s-debug.sh nexus-status
   ```

3. **Visa loggar:**
   ```bash
   ./scripts/k8s-debug.sh api-logs
   ./scripts/k8s-debug.sh nexus-logs
   ```

## Säkerhet

- Alla skript inkluderar säkerhetskontroller
- Destruktiva operationer kräver bekräftelse
- Skripten validerar miljö och beroenden

## Support

För problem eller frågor:
1. Kör `./scripts/k8s-debug.sh full-debug`
2. Granska output för felmeddelanden
3. Kontrollera loggar med `./scripts/k8s-debug.sh [service]-logs`
4. Se individuella README-filer för detaljerad hjälp
