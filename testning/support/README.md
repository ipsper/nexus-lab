# Support-funktioner för testning

Detta bibliotek innehåller små, rena hjälpfunktioner för olika typer av tester i Nexus Lab-projektet.

## Översikt över moduler

### APIClient (`api_client.py`)
Grundläggande HTTP-klient för API-tester.

```python
from support.api_client import APIClient

client = APIClient("http://localhost:3000")
response = client.get("/health")
assert response.status_code == 200
```

### PlaywrightClient (`playwright_client.py`)
Wrapper för Playwright som förenklar GUI-testning.

```python
from support.playwright_client import PlaywrightClient

with PlaywrightClient(headless=True) as client:
    client.navigate_to("http://localhost:3000/docs")
    client.wait_for_selector(".swagger-ui")
    assert client.is_element_visible(".swagger-ui")
```

### FastAPI Support (`fastapi_support.py`)
Små hjälpfunktioner för FastAPI API-tester - bara data-operationer.

```python
from support.fastapi_support import create_test_repository, get_repository_by_name, get_openapi_schema

def test_create_and_get_repo(api_client):
    # Testlogiken är direkt i testet
    repo_data = {"name": "test", "type": "hosted", "format": "pypi", "url": "...", "status": "active"}
    result = create_test_repository(api_client, repo_data)
    assert result["name"] == "test"
    
    # Använd hjälpfunktion för att hämta data
    retrieved = get_repository_by_name(api_client, "test")
    assert retrieved["name"] == "test"
    
    # Hämta schema för validering
    schema = get_openapi_schema(api_client)
    assert "paths" in schema
```

### FastAPI GUI Support (`fastapi_gui_support.py`)
Små hjälpfunktioner för Playwright GUI-tester.

```python
from support.fastapi_gui_support import navigate_to_docs, click_endpoint, try_it_out, execute_request, get_response_status
from support.playwright_client import PlaywrightClient

def test_health_endpoint_gui(api_base_url):
    with PlaywrightClient(headless=True) as client:
        # Testlogiken är direkt i testet
        navigate_to_docs(client, api_base_url)
        click_endpoint(client, "/health")
        try_it_out(client)
        execute_request(client)
        
        status = get_response_status(client)
        assert "200" in status
```

### Nexus Support (`nexus_support.py`)
Små hjälpfunktioner för Nexus Repository Manager-tester - bara data-operationer.

```python
from support.nexus_support import get_nexus_version, is_nexus_ready, get_repositories_list, repository_exists

def test_nexus_info(nexus_client):
    # Testlogiken är direkt i testet
    version = get_nexus_version(nexus_client)
    ready = is_nexus_ready(nexus_client)
    
    if version:
        assert isinstance(version, str)
    assert isinstance(ready, bool)
    
    # Kontrollera repositories
    repos = get_repositories_list(nexus_client)
    assert isinstance(repos, list)
    
    if repos:
        first_repo = repos[0].get("name")
        assert repository_exists(nexus_client, first_repo)
```

## Fixtures

Grundläggande fixtures finns i `conftest.py`:

- `api_client` - APIClient för FastAPI
- `nexus_client` - APIClient för Nexus
- `kong_client` - APIClient för Kong Gateway
- `playwright_browser_type` - Browser typ för Playwright
- `playwright_headless` - Headless-läge för Playwright

## Markers

Använd dessa pytest markers för att kategorisera dina tester:

- `@pytest.mark.api` - API-tester
- `@pytest.mark.gui` - GUI-tester med Playwright
- `@pytest.mark.integration` - Integrationstester
- `@pytest.mark.slow` - Långsamma tester
- `@pytest.mark.k8s` - Kubernetes-tester

## Exempel på testfiler

### API-test med support-funktioner
```python
# test_example_api.py
import pytest
from support.fastapi_support import test_health_endpoint, create_test_repository

@pytest.mark.api
def test_health_endpoint_works(api_client):
    test_health_endpoint(api_client)

@pytest.mark.api  
def test_create_repository_works(api_client):
    repo_data = {
        "name": "test-repo",
        "type": "hosted", 
        "format": "pypi",
        "url": "http://localhost:8081/repository/test-repo/",
        "status": "active"
    }
    created_repo = create_test_repository(api_client, repo_data)
    assert created_repo["name"] == "test-repo"
```

### GUI-test med Playwright
```python
# test_example_gui.py
import pytest
from support.playwright_client import PlaywrightClient
from support.fastapi_gui_support import test_docs_page_loads, execute_health_endpoint_via_swagger

@pytest.mark.gui
def test_swagger_ui_loads(api_base_url):
    with PlaywrightClient(headless=True) as client:
        test_docs_page_loads(client, api_base_url)

@pytest.mark.gui
def test_api_interaction(api_base_url):
    with PlaywrightClient(headless=True) as client:
        execute_health_endpoint_via_swagger(client, api_base_url)
```

## Köra tester

```bash
# Alla tester
pytest

# Endast API-tester
pytest -m api

# Endast GUI-tester  
pytest -m gui

# Exkludera långsamma tester
pytest -m "not slow"

# Specifik testfil
pytest test/test_fastapi_gui.py

# Med verbose output
pytest -v

# Parallell körning
pytest -n auto
```

## Environment-variabler

- `PLAYWRIGHT_HEADLESS=false` - Kör Playwright i icke-headless läge för debugging

## Funktionell design

Denna struktur använder funktionell programmering istället för objektorienterad:

- **Rena funktioner** - Inga klasser, bara funktioner som tar parametrar
- **Enkel import** - Importera bara de funktioner du behöver
- **Tydlig separation** - Support-funktioner är separata från testlogik
- **Flexibilitet** - Lätt att kombinera funktioner på olika sätt

## Fördelar med funktionell approach

1. **Enkelhet** - Inga klasser att hantera, bara funktioner
2. **Tydlighet** - Testlogiken är direkt i test-filerna
3. **Flexibilitet** - Kombinera funktioner som du vill
4. **Mindre kod** - Ingen boilerplate för klasser
5. **Lättare att förstå** - Direkt koppling mellan test och funktion
