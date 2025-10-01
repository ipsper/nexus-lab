# 🧠 Komihåg-lapp för Nexus Lab utveckling

## 🔄 Alltid bygg om pip-paketet och containern
**REGEL 1:** Om vi har ändrat NÅGOT i applikationen (app/, build-pip/, eller testning/), bygg ALLTID om pip-paketet och containern först:
```bash
./scripts/run.sh rebuild-api
```

**VIKTIGT:** Även om du bara ändrar test-kod, kör alltid `rebuild-api` för att säkerställa att allt är synkroniserat!

## 🐳 Kör alltid i test-containern
**REGEL 2:** Alla tester ska köras i test-containern, aldrig lokalt:
```bash
./scripts/run-test.sh [kommando]
```

## 📜 Använd funktioner i script
**REGEL 3:** Använd alltid de funktioner vi har byggt i scripten:
- `./scripts/run.sh` - för API-hantering
- `./scripts/run-test.sh` - för testning
- `./scripts/build-pip.sh` - för pip-paket

## 🚫 ALDRIG port-forward
**REGEL 4:** Använd ALDRIG `kubectl port-forward`. Använd alltid Kong Gateway:
- API: `http://localhost:8000/api` (via Kong)
- Nexus: `http://localhost:8000/nexus` (via Kong)
- Swagger: `http://localhost:8000/api/docs` (via Kong)

## 🔧 Vanliga arbetsflöden

### När du ändrar NÅGOT (API, test, eller annan kod):
1. Gör ändringar i `build-pip/nexus_repository_api/` eller `testning/`
2. Kör **ALLTID** `./scripts/run.sh rebuild-api` först
3. Testa med `./scripts/run-test.sh [test-typ]`

**Enkel regel:** Ändra kod → `rebuild-api` → testa

### När du debuggar:
1. Använd `./scripts/run-test.sh debug-env` för att kontrollera miljön
2. Använd Kong Gateway för att testa API:et manuellt
3. Kolla loggar med `kubectl logs -n nexus-api deployment/nexus-api`

## 🎯 Test-kommandon
- `./scripts/run-test.sh run-all` - alla tester
- `./scripts/run-test.sh run-scheduler` - schemaläggningstester
- `./scripts/run-test.sh run-api` - API-tester
- `./scripts/run-test.sh run-gui` - GUI-tester

## ⚠️ Viktiga påminnelser
- Testerna använder `host.docker.internal:8000` för att nå Kong Gateway
- API:et körs på port 3000 internt, men exponeras via Kong på port 8000
- Alltid vänta på att API:et startar efter `rebuild-api`
- Kontrollera att Kong Gateway fungerar innan du kör tester

## 🧪 Test-struktur
**REGEL 5:** Använd INGA klasser i testfiler, bara funktioner:
- ✅ `def test_something():` - funktioner
- ❌ `class TestSomething:` - inga klasser
- Klasser får bara finnas i `support/` mappen

## 🔍 Felsökning
Om testerna misslyckas:
1. Kontrollera att API:et körs: `curl http://localhost:8000/api/health`
2. Kontrollera Kong Gateway: `curl http://localhost:8000/`
3. Kolla test-miljön: `./scripts/run-test.sh debug-env`
4. Bygg om allt: `./scripts/run.sh rebuild-api`
