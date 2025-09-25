# Nexus Lab - Test Suite

## 📁 Teststruktur

### **Grundläggande API-tester** (`test_fastapi_basic.py`)
- **Markör:** `@pytest.mark.basic`
- **Kommando:** `./scripts/run-test.sh run-basic`
- **Innehåll:**
  - Root endpoint (`/`)
  - Health endpoint (`/health`)
  - Documentation (`/docs`, `/openapi.json`)
  - Stats endpoint (`/stats`)
  - Formats endpoint (`/formats`)
  - Config endpoint (`/config`)
  - Pip package endpoint (`/pip-package`)
  - Repositories endpoints (`/repositories/`, `/repositories/{name}`)
  - Packages endpoints (`/packages/`, `/repositories/{name}/packages`)
  - Response headers och timing

### **Error Handling-tester** (`test_api_errors.py`)
- **Markör:** `@pytest.mark.errors`
- **Kommando:** `./scripts/run-test.sh run-errors`
- **Innehåll:**
  - 404 Not Found errors
  - 405 Method Not Allowed errors
  - 422 Validation errors
  - Invalid JSON handling
  - Missing Content-Type headers
  - Large request bodies
  - Special characters i paths
  - Unicode handling
  - Malformed URLs
  - Timeout handling
  - Concurrent error handling

### **Data Validation-tester** (`test_api_validation.py`)
- **Markör:** `@pytest.mark.validation`
- **Kommando:** `./scripts/run-test.sh run-validation`
- **Innehåll:**
  - Repository name validation
  - Package name validation
  - JSON schema validation
  - Content-Type validation
  - Character encoding validation
  - Unicode validation
  - Numeric validation
  - Boolean validation
  - Array validation
  - Object validation
  - Required fields validation
  - Field length validation
  - SQL injection protection
  - XSS protection

### **Workflow-tester** (`test_api_workflows.py`)
- **Markör:** `@pytest.mark.workflows`
- **Kommando:** `./scripts/run-test.sh run-workflows`
- **Innehåll:**
  - Complete repository workflow
  - API health monitoring workflow
  - API documentation workflow
  - API configuration workflow
  - Pip package workflow
  - Statistics workflow
  - Error recovery workflow
  - Concurrent access workflow
  - Performance workflow
  - Data consistency workflow

### **Integration-tester** (`test_nexus_integration.py`, `test_kong_gateway.py`)
- **Markör:** `@pytest.mark.integration`
- **Kommando:** `./scripts/run-test.sh run-api`
- **Innehåll:**
  - Nexus Repository Manager integration
  - Kong Gateway integration
  - Service health checks

### **K8s-tester** (`test_k8s_integration.py`)
- **Markör:** `@pytest.mark.k8s`
- **Kommando:** `./scripts/run-k8s-tests.sh run`
- **Innehåll:**
  - Kubernetes cluster status
  - Pod health checks
  - Service availability
  - Resource monitoring

### **GUI-tester** (`test_fastapi_gui.py`, `test_endpoint_urls.py`)
- **Markör:** `@pytest.mark.gui`
- **Kommando:** `./scripts/run-test.sh run-gui`
- **Innehåll:**
  - Swagger UI testing
  - Endpoint discovery
  - Interactive testing

## 🚀 Användning

### **Kör alla tester:**
```bash
./scripts/run-test.sh run-all
```

### **Kör specifika test-kategorier:**
```bash
# Grundläggande API-tester
./scripts/run-test.sh run-basic

# Error handling-tester
./scripts/run-test.sh run-errors

# Data validation-tester
./scripts/run-test.sh run-validation

# Workflow-tester
./scripts/run-test.sh run-workflows

# Integration-tester
./scripts/run-test.sh run-api

# K8s-tester
./scripts/run-k8s-tests.sh run
```

### **Kör med --to-the-end (fortsätt vid fel):**
```bash
./scripts/run-test.sh run-basic --to-the-end
```

### **Kör custom pytest-kommando:**
```bash
./scripts/run-test.sh run -m "basic and not slow"
```

## 📊 Test Coverage

### **API Endpoints:**
- ✅ Root (`/`)
- ✅ Health (`/health`)
- ✅ Documentation (`/docs`, `/openapi.json`)
- ✅ Stats (`/stats`)
- ✅ Formats (`/formats`)
- ✅ Config (`/config`)
- ✅ Pip Package (`/pip-package`)
- ✅ Repositories (`/repositories/`, `/repositories/{name}`)
- ✅ Packages (`/packages/`, `/repositories/{name}/packages`)

### **Test Categories:**
- ✅ **Basic Functionality** - Alla endpoints fungerar
- ✅ **Error Handling** - Felhantering och edge cases
- ✅ **Data Validation** - Input-validering och säkerhet
- ✅ **Workflows** - Kompletta arbetsflöden
- ✅ **Integration** - Tjänsteintegration
- ✅ **K8s** - Kubernetes-integration
- ✅ **GUI** - Swagger UI och interaktivitet

## 🔧 Konfiguration

### **Test Markers:**
```ini
basic: Basic API functionality tests
errors: Error handling tests
validation: Data validation tests
workflows: End-to-end workflow tests
integration: Integration tests
k8s: Kubernetes integration tests
gui: GUI tests with Playwright
health: Environment health checks
```

### **Environment Variables:**
```bash
TEST_HOST=localhost          # Host för tester
TEST_PORT=8000              # Port för Kong Gateway
KONG_ADMIN_PORT=8001        # Port för Kong Admin API
NEXUS_DIRECT_PORT=8081      # Port för direkt Nexus-åtkomst
```

## 📈 Rapporter

Alla tester genererar HTML-rapporter i `testning/report.html` med:
- Test results
- Execution times
- Error details
- Coverage information

## 🐛 Felsökning

### **Vanliga problem:**
1. **Test container startar inte:** `./scripts/run-test.sh build`
2. **K8s-tester misslyckas:** Kontrollera att klustret körs med `./scripts/run.sh isalive`
3. **GUI-tester misslyckas:** Installera Playwright dependencies
4. **Integration-tester misslyckas:** Kontrollera att alla tjänster är uppe

### **Debug-kommandon:**
```bash
# Visa test-logs
./scripts/run-test.sh logs

# Stoppa test-container
./scripts/run-test.sh stop

# Rensa test-artifakter
./scripts/run-test.sh clean
```