# Pip-paket för Nexus Repository API

Denna fil listar alla pip-paket som används i Nexus Repository API-projektet, både för applikationen och testerna.

## Applikationspaket (Production)

Dessa paket används i själva FastAPI-applikationen:

| Paket | Version | Ursprung | Användning |
|-------|---------|----------|------------|
| fastapi | >=0.117.1 | [PyPI](https://pypi.org/project/fastapi/) | Web framework för API |
| uvicorn | >=0.37.0 | [PyPI](https://pypi.org/project/uvicorn/) | ASGI server |
| pydantic | >=2.11.9 | [PyPI](https://pypi.org/project/pydantic/) | Data validation och serialization |
| python-multipart | >=0.0.20 | [PyPI](https://pypi.org/project/python-multipart/) | Multipart form data support |
| httpx | >=0.28.1 | [PyPI](https://pypi.org/project/httpx/) | HTTP client för schemaläggning |
| python-dotenv | >=1.1.1 | [PyPI](https://pypi.org/project/python-dotenv/) | Environment variable loading |

## Testpaket (Development/Testing)

Dessa paket används för testning och utveckling:

| Paket | Version | Ursprung | Användning |
|-------|---------|----------|------------|
| pytest | 7.4.3 | [PyPI](https://pypi.org/project/pytest/) | Test framework |
| pytest-asyncio | 0.21.1 | [PyPI](https://pypi.org/project/pytest-asyncio/) | Async test support |
| pytest-cov | 4.1.0 | [PyPI](https://pypi.org/project/pytest-cov/) | Code coverage |
| pytest-html | 4.1.1 | [PyPI](https://pypi.org/project/pytest-html/) | HTML test reports |
| pytest-xdist | 3.3.1 | [PyPI](https://pypi.org/project/pytest-xdist/) | Parallel test execution |
| requests | 2.31.0 | [PyPI](https://pypi.org/project/requests/) | HTTP client för tester |
| httpx | 0.25.2 | [PyPI](https://pypi.org/project/httpx/) | Modern HTTP client för tester |
| pydantic | 2.5.0 | [PyPI](https://pypi.org/project/pydantic/) | Data validation (test version) |
| pytest-json-report | 1.5.0 | [PyPI](https://pypi.org/project/pytest-json-report/) | JSON test reports |
| pytest-benchmark | 4.0.0 | [PyPI](https://pypi.org/project/pytest-benchmark/) | Performance benchmarking |
| pytest-order | 1.2.0 | [PyPI](https://pypi.org/project/pytest-order/) | Test execution order control |
| playwright | 1.40.0 | [PyPI](https://pypi.org/project/playwright/) | Browser automation |
| pytest-playwright | 0.4.3 | [PyPI](https://pypi.org/project/pytest-playwright/) | Playwright integration för pytest |
| colorama | 0.4.6 | [PyPI](https://pypi.org/project/colorama/) | Colored terminal output |
| rich | 13.7.0 | [PyPI](https://pypi.org/project/rich/) | Rich text and beautiful formatting |

## Optional Dependencies (Development)

Dessa paket är definierade som optional dependencies i pyproject.toml:

| Paket | Version | Ursprung | Användning |
|-------|---------|----------|------------|
| black | >=23.0.0 | [PyPI](https://pypi.org/project/black/) | Code formatter |
| flake8 | >=6.0.0 | [PyPI](https://pypi.org/project/flake8/) | Linter |
| mypy | >=1.0.0 | [PyPI](https://pypi.org/project/mypy/) | Type checker |
| gunicorn | >=21.0.0 | [PyPI](https://pypi.org/project/gunicorn/) | WSGI server (Docker) |
| kubernetes | >=28.0.0 | [PyPI](https://pypi.org/project/kubernetes/) | Kubernetes client |

## Build System Dependencies

| Paket | Version | Ursprung | Användning |
|-------|---------|----------|------------|
| setuptools | >=61.0 | [PyPI](https://pypi.org/project/setuptools/) | Build system |
| wheel | - | [PyPI](https://pypi.org/project/wheel/) | Wheel package format |

## Sammanfattning

- **Total antal unika paket**: 25
- **Production paket**: 6
- **Test/Development paket**: 15
- **Optional paket**: 5
- **Build system paket**: 2

## För binär repository

För att skapa en input-fil till en binär repository (som Nexus Repository Manager), använd följande format:

```
# Production dependencies
fastapi>=0.117.1
uvicorn>=0.37.0
pydantic>=2.11.9
python-multipart>=0.0.20
httpx>=0.28.1
python-dotenv>=1.1.1

# Test dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-html==4.1.1
pytest-xdist==3.3.1
requests==2.31.0
httpx==0.25.2
pydantic==2.5.0
pytest-json-report==1.5.0
pytest-benchmark==4.0.0
pytest-order==1.2.0
playwright==1.40.0
pytest-playwright==0.4.3
colorama==0.4.6
rich==13.7.0

# Optional dependencies
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
gunicorn>=21.0.0
kubernetes>=28.0.0

# Build system
setuptools>=61.0
wheel
```

## Noteringar

- Alla paket kommer från PyPI (Python Package Index)
- Versioner är specificerade enligt PEP 440
- `httpx` och `pydantic` finns i både production och test med olika versioner
- `playwright` kräver ytterligare browser binaries som laddas ner automatiskt
- `uvicorn[standard]` inkluderar extra dependencies för production use
