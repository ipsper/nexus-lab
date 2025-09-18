# Nexus Lab - Testsystem

Detta är testsystemet för Nexus Lab-projektet som innehåller olika typer av tester för att validera systemets funktionalitet.

## 📋 Översikt

Testsystemet är uppdelat i flera kategorier:

- **Health Checks** - Kontrollerar att miljön är uppe och redo
- **API-tester** - Testar REST API-endpoints
- **GUI-tester** - Testar webbgränssnitt med Playwright
- **Integration-tester** - Testar samspelet mellan tjänster
- **K8s-tester** - Testar Kubernetes-deployment

## 🏗️ Struktur

```
testning/
├── test/                           # Testfiler
│   ├── test_environment_health.py  # Health checks - kör FÖRST
│   ├── test_fastapi_basic.py       # FastAPI grundläggande tester
│   ├── test_fastapi_gui.py         # FastAPI GUI-tester med Playwright
│   ├── test_nexus_integration.py   # Nexus integration-tester
│   ├── test_kong_gateway.py        # Kong Gateway-tester
│   └── test_k8s_integration.py     # Kubernetes-tester
├── support/                        # Support-funktioner
│   ├── api_client.py              # HTTP-klient
│   ├── playwright_client.py       # Playwright wrapper
│   ├── fastapi_support.py         # FastAPI hjälpfunktioner
│   ├── fastapi_gui_support.py     # GUI hjälpfunktioner
│   ├── nexus_support.py           # Nexus hjälpfunktioner
│   ├── kong_support.py            # Kong hjälpfunktioner
│   └── k8s_support.py             # Kubernetes hjälpfunktioner
├── conftest.py                     # Pytest fixtures och konfiguration
├── pytest.ini                     # Pytest inställningar
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image för tester
└── README.md                       # Denna fil
```

## ⚙️ Konfiguration

### Miljövariabler
Systemet kan konfigureras med följande miljövariabler:

| Variabel | Beskrivning | Default |
|----------|-------------|---------|
| `TEST_HOST` | Host för tester | `localhost` |
| `TEST_PORT` | Port för Kong Gateway | `8000` |
| `KONG_ADMIN_PORT` | Port för Kong Admin API | `8001` |
| `NEXUS_DIRECT_PORT` | Port för direkt Nexus-åtkomst | `8081` |

### Exempel på konfiguration
```bash
# Standard (localhost:8000)
./scripts/run-test.sh run-health

# Testa mot annan host
TEST_HOST=192.168.1.100 ./scripts/run-test.sh run-api

# Anpassad port
TEST_PORT=9000 ./scripts/run-test.sh run-gui

# Kombinera flera variabler
TEST_HOST=remote.server TEST_PORT=8080 ./scripts/run-test.sh run-all

# Visa aktuell konfiguration (visas automatiskt vid container-start)
./scripts/run-test.sh run-health  # Visar: TEST_HOST=localhost, TEST_PORT=8000, etc.
```

## 🚀 Snabbstart

### 1. Kontrollera miljön först
```bash
# Kontrollera att alla tjänster är uppe
./scripts/test.sh health
# ELLER direkt:
./scripts/run-test.sh run-health
```

### 2. Kör specifika testtyper
```bash
# Bara API-tester (utan GUI) - stannar vid första fel
./scripts/run-test.sh run-api

# Bara GUI-tester - stannar vid första fel  
./scripts/run-test.sh run-gui

# Health checks - stannar vid första fel
./scripts/run-test.sh run-health

# Kubernetes-tester - stannar vid första fel
./scripts/run-test.sh run-k8s

# Alla tester
./scripts/run-test.sh run-all
```

### 3. Fortsätt vid fel (--to-the-end)
```bash
# API-tester som fortsätter vid fel
./scripts/run-test.sh run-api --to-the-end

# GUI-tester som fortsätter vid fel
./scripts/run-test.sh run-gui --to-the-end

# Health checks som fortsätter vid fel
./scripts/run-test.sh run-health --to-the-end
```

### 4. High-level kommandon (via test.sh)
```bash
# Kör alla tester (health + API + GUI + K8s)
./scripts/test.sh all

# Bara API-tester (utan GUI)
./scripts/test.sh api

# Bara GUI-tester
./scripts/test.sh gui

# Med verbose output
./scripts/test.sh verbose gui
```

## 📝 Testtyper och Markers

### Test Markers

Använd dessa markers för att kategorisera och filtrera tester:

```python
@pytest.mark.health      # Health checks - kör först
@pytest.mark.api         # API-tester
@pytest.mark.gui         # GUI-tester med Playwright
@pytest.mark.integration # Integration-tester
@pytest.mark.slow        # Långsamma tester
@pytest.mark.k8s         # Kubernetes-tester
```

### Exempel på filtrering

```bash
# Direkt med run-test.sh (rekommenderat):
./scripts/run-test.sh run-api                    # API-tester (stannar vid fel)
./scripts/run-test.sh run-gui                    # GUI-tester (stannar vid fel)
./scripts/run-test.sh run-health                 # Health checks (stannar vid fel)
./scripts/run-test.sh run -k test_health         # Specifik test
./scripts/run-test.sh run -m "not slow"          # Bara snabba tester
./scripts/run-test.sh run test/test_fastapi_basic.py  # Specifik fil

# Via test.sh (high-level):
./scripts/test.sh api                            # API-tester utan GUI
./scripts/test.sh gui                            # GUI-tester
./scripts/test.sh verbose gui                    # GUI-tester med verbose
./scripts/test.sh api --to-the-end               # API-tester, fortsätt vid fel
```

## 🏥 Health Checks

**Alltid kör health checks först** för att säkerställa att miljön är redo:

```bash
# Rekommenderat (stannar vid första fel):
./scripts/run-test.sh run-health

# Eller via high-level script:
./scripts/test.sh health
```

Health checks kontrollerar:
- ✅ FastAPI tjänsten svarar
- ✅ Kong Gateway fungerar
- ✅ Nexus är tillgänglig
- ✅ API-endpoints returnerar korrekt data
- ✅ Routing genom Kong fungerar

**Om health checks misslyckas:**
1. Starta tjänsterna: `./scripts/run.sh`
2. Vänta tills alla pods är redo
3. Kör health checks igen

## 🔧 API-tester

Testar REST API-funktionalitet (utan GUI):

```bash
# Alla API-tester (stannar vid första fel)
./scripts/run-test.sh run-api

# API-tester som fortsätter vid fel
./scripts/run-test.sh run-api --to-the-end

# Specifika API-tester
./scripts/run-test.sh run -k fastapi -m "not gui"
./scripts/run-test.sh run -k nexus -m "not gui"
./scripts/run-test.sh run -k kong -m "not gui"

# Via high-level script
./scripts/test.sh api                    # API-tester utan GUI
./scripts/test.sh api --to-the-end       # Fortsätt vid fel
```

### API-test exempel

```python
# test/test_example.py
import pytest
from support.fastapi_support import create_test_repository

@pytest.mark.api
def test_create_repository(api_client):
    repo_data = {
        "name": "test-repo",
        "type": "hosted",
        "format": "pypi", 
        "url": "http://localhost:8081/repository/test-repo/",
        "status": "active"
    }
    result = create_test_repository(api_client, repo_data)
    assert result["name"] == "test-repo"
```

## 🎭 GUI-tester

Testar webbgränssnitt med Playwright:

```bash
# Alla GUI-tester (stannar vid första fel)
./scripts/run-test.sh run-gui

# GUI-tester som fortsätter vid fel
./scripts/run-test.sh run-gui --to-the-end

# Specifika GUI-tester
./scripts/run-test.sh run -k "chromium" -m gui
./scripts/run-test.sh run -k "responsive" -m gui
./scripts/run-test.sh run -k "performance" -m gui

# Via high-level script
./scripts/test.sh gui                    # Alla GUI-tester
./scripts/test.sh verbose gui            # GUI-tester med verbose output
./scripts/test.sh gui --to-the-end       # Fortsätt vid fel
```

### GUI-test exempel

```python
# test/test_gui_example.py
import pytest
from support.playwright_client import PlaywrightClient
from support.fastapi_gui_support import navigate_to_docs

@pytest.mark.gui
def test_docs_page(api_base_url):
    with PlaywrightClient(headless=True) as client:
        navigate_to_docs(client, api_base_url)
        assert client.is_element_visible(".swagger-ui")
        assert "Nexus Repository Manager API" in client.get_title()
```

## 🔄 Docker och Container-hantering

### Test-container hantering

```bash
# Bygg om containern (t.ex. efter dependency-ändringar)
./scripts/test.sh rebuild
./scripts/run-test.sh build

# Stoppa körande test-container
./scripts/run-test.sh stop

# Rensa alla test-containers och images
./scripts/run-test.sh clean
```

### Container-arkitektur

Testerna använder en **persistent container** med `docker exec`:
- **Snabbare:** Container startas en gång och återanvänds
- **Bättre kontroll:** Direkta pytest-kommandon
- **Enklare debugging:** Kan komma åt containern interaktivt
- **Konfigurerbara URL:er:** Miljövariabler sätts automatiskt

### Docker-miljö

Test-containern innehåller:
- Ubuntu 22.04 (bättre Playwright-stöd)
- Python 3.10
- Playwright browsers (Chromium, Firefox, Webkit)
- Alla test-dependencies
- Persistent `/app` volume för snabb uppdatering
- Miljövariabler för URL-konfiguration (TEST_HOST, TEST_PORT, etc.)

### Environment Variables för debugging

```bash
# Playwright i synligt läge (för debugging)
PLAYWRIGHT_HEADLESS=false ./scripts/test.sh api -m gui

# Olika log-nivåer
PYTEST_VERBOSITY=2 ./scripts/test.sh api
```

### Pytest-konfiguration

Redigera `pytest.ini` för att ändra:
- Test-markers
- Default arguments
- Asyncio-läge
- Test-sökvägar

## 🐛 Debugging

### Verbose output

```bash
# Mer detaljerad output
./scripts/test.sh api -v

# Visa alla print-statements
./scripts/test.sh api -s

# Längre traceback
./scripts/test.sh api --tb=long

# Stoppa vid första fel
./scripts/test.sh api -x
```

### GUI-debugging

```bash
# Kör GUI-tester i synligt läge
PLAYWRIGHT_HEADLESS=false ./scripts/test.sh api -m gui

# Ta skärmdumpar vid fel
./scripts/test.sh api -m gui --screenshot=on
```

### Logs och rapporter

```bash
# HTML-rapport genereras automatiskt
# Finns i: testning/report.html

# Visa test-logs
./scripts/test.sh logs
```

## 📊 Test-rapporter

Efter testkörning finns rapporter i:
- `testning/report.html` - HTML-rapport med detaljer
- Terminal output - Realtidsresultat

## 🏃‍♂️ Vanliga kommandon

```bash
# Snabb health check (stannar vid fel)
./scripts/run-test.sh run-health

# API-tester utan GUI (stannar vid fel)
./scripts/run-test.sh run-api

# GUI-tester (stannar vid fel)
./scripts/run-test.sh run-gui

# Fortsätt vid fel
./scripts/run-test.sh run-api --to-the-end
./scripts/run-test.sh run-gui --to-the-end

# Specifika tester
./scripts/run-test.sh run -k test_health
./scripts/run-test.sh run test/test_fastapi_basic.py
./scripts/run-test.sh run -m "not slow"

# Container-hantering
./scripts/run-test.sh stop               # Stoppa container
./scripts/run-test.sh build              # Bygg om container

# High-level kommandon
./scripts/test.sh all                    # Alla tester
./scripts/test.sh verbose gui            # Verbose GUI-tester
```

## 🔍 Felsökning

### Problem: Tester misslyckas med connection errors

**Lösning:**
1. Kontrollera att tjänsterna körs: `kubectl get pods`
2. Starta tjänsterna: `./scripts/run.sh`
3. Kör health check: `./scripts/test.sh health`

### Problem: GUI-tester timeout

**Lösning:**
1. Kontrollera att API:erna svarar: `./scripts/test.sh api -m "not gui"`
2. Testa i synligt läge: `PLAYWRIGHT_HEADLESS=false ./scripts/test.sh api -m gui`
3. Öka timeout i `playwright_client.py`

### Problem: Playwright browsers saknas

**Lösning:**
```bash
# Bygg om containern
./scripts/test.sh rebuild
```

### Problem: Pytest markers okända

**Lösning:**
Kontrollera att alla markers är definierade i `pytest.ini`

## 📚 Utveckling av nya tester

### 1. Skapa testfil

```python
# test/test_my_feature.py
import pytest

@pytest.mark.api
def test_my_feature(api_client):
    response = api_client.get("/my-endpoint")
    assert response.status_code == 200
```

### 2. Skapa support-funktioner vid behov

```python
# support/my_support.py
def create_my_resource(api_client, data):
    """Hjälpfunktion för att skapa resurs"""
    response = api_client.post("/my-resource", data=data)
    return response.json()
```

### 3. Lägg till i conftest.py om nödvändigt

```python
# conftest.py
@pytest.fixture
def my_fixture():
    return "my_value"
```

## 🎯 Best Practices

### Test-struktur
- **En test per funktion** - Testa en sak i taget
- **Tydliga namn** - `test_health_endpoint_returns_200`
- **Arrange-Act-Assert** - Förbered, utför, kontrollera
- **Cleanup** - Städa upp efter tester

### Support-funktioner
- **Rena funktioner** - Inga side-effects
- **Små och fokuserade** - En funktion per uppgift
- **Återanvändbara** - Kan användas i flera tester
- **Dokumenterade** - Tydliga docstrings

### GUI-tester
- **Vänta på element** - Använd `wait_for_selector`
- **Robusta selektorer** - Testa flera selektorer
- **Hantera timeouts** - Graceful degradation
- **Headless default** - Använd synligt läge bara för debugging

## 🔄 CI/CD Integration

För automatiserade tester:

```bash
# I CI/CD pipeline
./scripts/test.sh health          # Kontrollera miljö
./scripts/test.sh api -m "not slow"  # Snabba tester
./scripts/test.sh api -m gui      # GUI-tester
```

## 📞 Support

Om du stöter på problem:
1. Kör health checks först: `./scripts/test.sh health`
2. Kontrollera logs: `kubectl logs <pod-name>`
3. Bygg om test-container: `./scripts/test.sh rebuild`
4. Kontrollera tjänster: `kubectl get pods,svc`

## 🎉 Exempel på komplett workflow

```bash
# 1. Starta miljön
./scripts/run.sh

# 2. Vänta på att tjänsterna startar (några minuter)

# 3. Kontrollera att miljön är redo
./scripts/test.sh health

# 4. Kör alla tester
./scripts/test.sh all

# 5. Eller kör specifika tester
./scripts/test.sh api -m "api and not slow"
./scripts/test.sh api -m gui
```

## 🏆 Testresultat

Ett lyckat test-run ser ut så här:

```
✅ Health checks: 5/5 passed
✅ API-tester: 21/21 passed  
✅ GUI grundfunktioner: 8/14 passed
✅ Integration-tester: 15/15 passed

Total: 49/55 passed (89% success rate)
```

---

**Tips:** Kör alltid `./scripts/test.sh health` först för att spara tid! 🚀