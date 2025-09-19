# Nexus Repository API - Pip-paket Guide

Denna guide beskriver hur du bygger, distribuerar och använder FastAPI-appen som ett pip-paket.

## 📦 Paketstruktur

Projektet har omstruktureras för att fungera som ett pip-paket:

```
nexus-lab/
├── nexus_repository_api/          # Huvudpaket
│   ├── __init__.py               # Paket-initialisering
│   ├── main.py                   # FastAPI-applikation
│   ├── models.py                 # Pydantic-modeller
│   └── cli.py                    # Kommandorad-interface
├── tests/                        # Tester
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml               # Modern Python-paketkonfiguration
├── MANIFEST.in                  # Filer att inkludera i paketet
├── LICENSE                      # MIT-licens
└── README_to_pip.md            # Denna guide
```

## 🔧 Förberedelser

### 1. Använd build-skriptet (Rekommenderat)

Vi har skapat ett `build-pip.sh` skript som hanterar allt automatiskt:

```bash
# Gör skriptet körbart
chmod +x build-pip.sh

# Visa hjälp
./build-pip.sh help

# Bygg paketet (skapar venv automatiskt)
./build-pip.sh build

# Bygg och testa
./build-pip.sh build test

# Bygg, testa och installera lokalt
./build-pip.sh build test install
```

### 2. Manuell installation (alternativ)

```bash
# Installera build-verktyg
pip install build twine

# För utveckling (valfritt)
pip install -e ".[dev]"
```

### 3. Kontrollera projektstrukturen

```bash
# Visa paketstruktur
tree nexus_repository_api/

# Kontrollera att alla filer finns
ls -la nexus_repository_api/
```

## 🏗️ Bygga paketet

### 1. Med build-skriptet (Enkelt)

```bash
# Bygg paketet med virtuell miljö
./build-pip.sh build

# Bygg och kör tester
./build-pip.sh build test

# Bygg, testa och installera lokalt
./build-pip.sh build test install

# Rensa build-artefakter
./build-pip.sh clean
```

### 2. Manuell build (Avancerat)

```bash
# Rensa gamla builds (om de finns)
rm -rf dist/ build/ *.egg-info/

# Bygg paketet
python -m build

# Kontrollera vad som skapades
ls -la dist/
```

Detta skapar två filer i `dist/`-mappen:
- `nexus_repository_api-1.0.0-py3-none-any.whl` (wheel-format)
- `nexus_repository_api-1.0.0.tar.gz` (source distribution)

### 2. Verifiera paketet

```bash
# Kontrollera paketets innehåll
python -m twine check dist/*

# Visa innehållet i wheel-filen
python -m zipfile -l dist/nexus_repository_api-1.0.0-py3-none-any.whl
```

## 📋 Installation och användning

### 1. Installera från lokal fil

```bash
# Installera från wheel-fil
pip install dist/nexus_repository_api-1.0.0-py3-none-any.whl

# Eller från source distribution
pip install dist/nexus_repository_api-1.0.0.tar.gz

# Eller installera i utvecklingsläge
pip install -e .
```

### 2. Använda kommandoradsverktyget

Efter installation är `nexus-api` kommandot tillgängligt:

```bash
# Starta servern (standard: localhost:3000)
nexus-api

# Starta på annan port
nexus-api --port 8080

# Starta bara på localhost
nexus-api --host 127.0.0.1

# Starta med auto-reload för utveckling
nexus-api --reload

# Starta med debug-loggning
nexus-api --log-level debug

# Visa hjälp
nexus-api --help

# Visa version
nexus-api --version
```

### 3. Använda som Python-modul

```python
# Importera och använda direkt
from nexus_repository_api import app, run_server
from nexus_repository_api.models import RepositoryInfo

# Starta servern programmatiskt
run_server(host="0.0.0.0", port=3000)

# Eller använd FastAPI-appen direkt
# (t.ex. med Gunicorn i produktion)
```

### 4. Använda med ASGI-server

```bash
# Med Uvicorn
uvicorn nexus_repository_api.main:app --host 0.0.0.0 --port 3000

# Med Gunicorn (installera först: pip install gunicorn)
gunicorn nexus_repository_api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000
```

## 🧪 Testning

### 1. Kör tester

```bash
# Installera test-dependencies
pip install -e ".[dev]"

# Kör alla tester
pytest

# Kör med coverage
pytest --cov=nexus_repository_api

# Kör specifikt test
pytest tests/test_main.py::test_health_check
```

### 2. Testa installerat paket

```bash
# Testa att kommandot fungerar
nexus-api --version

# Starta servern kort
timeout 5 nexus-api &

# Testa API
curl http://localhost:3000/health
```

## 🚀 Distribution

### 1. Ladda upp till PyPI (Test)

```bash
# Skapa konto på https://test.pypi.org/
# Konfigurera credentials

# Ladda upp till Test PyPI
python -m twine upload --repository testpypi dist/*

# Testa installation från Test PyPI
pip install --index-url https://test.pypi.org/simple/ nexus-repository-api
```

### 2. Ladda upp till PyPI (Produktion)

```bash
# Skapa konto på https://pypi.org/
# Konfigurera credentials

# Ladda upp till PyPI
python -m twine upload dist/*

# Installera från PyPI
pip install nexus-repository-api
```

### 3. Automatisk distribution med GitHub Actions

Skapa `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}
```

## 🔧 Utveckling

### 1. Utvecklingsinstallation

```bash
# Klona repo
git clone <your-repo>
cd nexus-lab

# Installera i utvecklingsläge
pip install -e ".[dev]"

# Kör tester
pytest

# Formatera kod
black nexus_repository_api/

# Linta kod
flake8 nexus_repository_api/

# Type checking
mypy nexus_repository_api/
```

### 2. Uppdatera version

1. Uppdatera version i `pyproject.toml`
2. Uppdatera version i `nexus_repository_api/__init__.py`
3. Uppdatera version i `nexus_repository_api/cli.py`
4. Bygg nytt paket: `python -m build`

### 3. Lägga till nya funktioner

```python
# Lägg till nya endpoints i main.py
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "New feature"}

# Lägg till nya modeller i models.py
class NewModel(BaseModel):
    field: str

# Lägg till tester i tests/
def test_new_endpoint():
    response = client.get("/new-endpoint")
    assert response.status_code == 200
```

## 📖 Användningsexempel

### 1. Som webbserver

```bash
# Starta server
nexus-api --port 8080

# API är tillgängligt på:
# http://localhost:8080/docs     # Swagger UI
# http://localhost:8080/health   # Health check
# http://localhost:8080/repositories  # API endpoints
```

### 2. Som Python-bibliotek

```python
from nexus_repository_api import app
from fastapi.testclient import TestClient

# Skapa test client
client = TestClient(app)

# Använd API programmatiskt
response = client.get("/repositories")
repositories = response.json()

for repo in repositories:
    print(f"Repository: {repo['name']} ({repo['format']})")
```

### 3. I Docker

```dockerfile
FROM python:3.11-slim

# Installera från PyPI
RUN pip install nexus-repository-api

# Starta server
CMD ["nexus-api", "--host", "0.0.0.0", "--port", "3000"]
```

### 4. Med Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexus-api
  template:
    metadata:
      labels:
        app: nexus-api
    spec:
      containers:
      - name: nexus-api
        image: python:3.11-slim
        command: ["pip", "install", "nexus-repository-api", "&&", "nexus-api"]
        ports:
        - containerPort: 3000
```

## 🐛 Felsökning

### Vanliga problem

1. **ModuleNotFoundError**: 
   ```bash
   # Kontrollera installation
   pip list | grep nexus-repository-api
   
   # Reinstallera
   pip uninstall nexus-repository-api
   pip install nexus-repository-api
   ```

2. **Kommandot `nexus-api` hittas inte**:
   ```bash
   # Kontrollera PATH
   python -m pip show nexus-repository-api
   
   # Eller kör direkt
   python -m nexus_repository_api.cli
   ```

3. **Port redan används**:
   ```bash
   # Använd annan port
   nexus-api --port 8080
   
   # Eller hitta process som använder porten
   lsof -i :3000
   ```

## 📚 Ytterligare resurser

- [Python Packaging Guide](https://packaging.python.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyPI Help](https://pypi.org/help/)
- [Setuptools Documentation](https://setuptools.pypa.io/)

## 🤝 Bidrag

1. Forka projektet
2. Skapa feature branch: `git checkout -b feature/amazing-feature`
3. Commita ändringar: `git commit -m 'Add amazing feature'`
4. Pusha branch: `git push origin feature/amazing-feature`
5. Öppna Pull Request

## 📄 Licens

Detta projekt är licensierat under MIT License - se [LICENSE](LICENSE) filen för detaljer.

---

**Utvecklat av IP-solutions Lab Team** 🚀
