#!/bin/bash

# Nexus Repository API - Pip Package Build Script
# Detta skript bygger pip-paketet med hjälp av en virtuell miljö

set -e  # Avsluta vid fel

# Sätt arbetskatalog till build-pip mappen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT/build-pip"

# GitLab projekt ID (kan överridas med environment variabel)
GITLAB_PROJECT_ID="${GITLAB_PROJECT_ID:-10}"

# Paketnamn (kan överridas med environment variabel)
PACKAGE_NAME="${PACKAGE_NAME:-nexus-lab}"

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktioner för färgad output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Hjälpfunktion
show_help() {
    echo "Nexus Repository API - Pip Package Build Script"
    echo ""
    echo "Användning: $0 [KOMMANDO]"
    echo ""
    echo "Kommandon:"
    echo "  build             Bygg pip-paketet (standard)"
    echo "  clean             Rensa build-artefakter"
    echo "  test              Kör tester efter build"
    echo "  install           Installera paketet lokalt för testning"
    echo "  uninstall         Avinstallera paketet"
    echo "  check             Kontrollera paketets innehåll"
    echo "  docker            Bygg Docker-image med pip-paketet (lokal)"
    echo "  docker-gitlab     Bygg Docker-image för GitLab CI/CD"
    echo "  upload            Ladda upp paketet till privat PyPI-repository"
    echo "  upload-testpypi   Ladda upp paketet till TestPyPI för testning"
    echo "  local-install     Installera paketet lokalt för testning"
    echo "  help              Visa denna hjälp"
    echo ""
    echo "Environment variabler:"
    echo "  GITLAB_PROJECT_ID GitLab projekt ID (standard: 10)"
    echo "  PACKAGE_NAME      Paketnamn (standard: nexus-lab)"
    echo "  TWINE_USERNAME    GitLab användarnamn för upload"
    echo "  TWINE_PASSWORD    GitLab access token för upload"
    echo ""
    echo "GitLab CI/CD variabler (automatiskt satta i CI):"
    echo "  CI_API_V4_URL     GitLab API URL (automatiskt satt)"
    echo "  CI_PROJECT_ID     GitLab projekt ID (automatiskt satt)"
    echo ""
    echo "Exempel:"
    echo "  $0 build"
    echo "  $0 build test"
    echo "  $0 clean build install"
    echo "  $0 build upload"
    echo "  $0 build docker"
    echo "  $0 build docker-gitlab"
    echo "  $0 upload-testpypi"
    echo "  GITLAB_PROJECT_ID=123 $0 upload"
    echo "  PACKAGE_NAME=my-package $0 upload"
    echo "  TWINE_USERNAME=user TWINE_PASSWORD=token $0 upload"
    echo ""
    echo "GitLab CI/CD pipeline exempel:"
    echo "  script:"
    echo "    - pip install build twine"
    echo "    - python -m build"
    echo "    - python -m twine upload --repository-url \${CI_API_V4_URL}/projects/\${CI_PROJECT_ID}/packages/pypi --verbose dist/*"
}

# Kontrollera om Python 3 är tillgängligt
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 är inte installerat. Installera det först."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_info "Använder Python $PYTHON_VERSION"
}

# Skapa virtuell miljö
create_venv() {
    print_info "Skapar virtuell miljö..."
    
    if [ -d "venv" ]; then
        print_warning "Virtuell miljö finns redan. Tar bort den först..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    print_success "Virtuell miljö skapad"
}

# Aktivera virtuell miljö
activate_venv() {
    print_info "Aktiverar virtuell miljö..."
    
    if [ ! -d "venv" ]; then
        print_error "Virtuell miljö finns inte. Kör 'build' först."
        exit 1
    fi
    
    source venv/bin/activate
    print_success "Virtuell miljö aktiverad"
}

# Installera build-verktyg
install_build_tools() {
    print_info "Installerar build-verktyg..."
    pip install --upgrade pip==25.2
    pip install build twine
    print_success "Build-verktyg installerade"
}

# Bygg pip-paketet
build_package() {
    print_info "Bygger pip-paketet..."
    python -m build
    
    print_success "Wheel-paket byggt: dist/nexus_repository_api-1.0.0-py3-none-any.whl"
    print_success "Source distribution byggd: dist/nexus_repository_api-1.0.0.tar.gz"
    
    print_info "Paketinformation:"
    ls -la dist/
    
    print_info "Kontrollerar paketets innehåll..."
    python -m twine check dist/*
    
    print_success "Pip-paketet byggt framgångsrikt!"
}

# Rensa build-artefakter
clean_build() {
    print_info "Rensar build-artefakter..."
    
    if [ -d "dist" ]; then
        rm -rf dist/
        print_info "Tar bort dist/ mapp"
    fi
    
    if [ -d "build" ]; then
        rm -rf build/
        print_info "Tar bort build/ mapp"
    fi
    
    if [ -d "*.egg-info" ]; then
        rm -rf *.egg-info/
        print_info "Tar bort egg-info mappar"
    fi
    
    if [ -d "venv" ]; then
        rm -rf venv/
        print_info "Tar bort virtuell miljö"
    fi
    
    print_success "Build-artefakter rensade"
}

# Kör tester
run_tests() {
    print_info "Kör tester..."
    
    if [ ! -d "venv" ]; then
        print_error "Virtuell miljö finns inte. Kör 'build' först."
        exit 1
    fi
    
    source venv/bin/activate
    pip install -e ".[dev]"
    pytest
    
    print_success "Tester körda framgångsrikt!"
}

# Installera paketet lokalt för testning
local_install() {
    print_info "Installerar paketet lokalt för testning..."
    
    if [ ! -d "venv" ]; then
        print_error "Virtuell miljö finns inte. Kör 'build' först."
        exit 1
    fi
    
    source venv/bin/activate
    
    if [ -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_info "Installerar från wheel-paket..."
        pip install dist/nexus_repository_api-1.0.0-py3-none-any.whl --force-reinstall
        
        print_success "Paketet installerat lokalt!"
        
        print_info "Testa att kommandot fungerar:"
        echo "  nexus-api --help"
        echo "  nexus-api --version"
        
        print_info "För att avinstallera:"
        echo "  pip uninstall nexus-repository-api -y"
    else
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
}

# Installera paketet lokalt
install_package() {
    print_info "Installerar paketet lokalt..."
    
    if [ ! -d "venv" ]; then
        print_error "Virtuell miljö finns inte. Kör 'build' först."
        exit 1
    fi
    
    source venv/bin/activate
    
    if [ -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        pip install dist/nexus_repository_api-1.0.0-py3-none-any.whl
        print_success "Paketet installerat lokalt"
        
        print_info "Testa att kommandot fungerar:"
        echo "  nexus-api --help"
        echo "  nexus-api --version"
    else
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
}

# Avinstallera paketet
uninstall_package() {
    print_info "Avinstallerar paketet..."
    
    if [ ! -d "venv" ]; then
        print_error "Virtuell miljö finns inte."
        exit 1
    fi
    
    source venv/bin/activate
    pip uninstall nexus-repository-api -y
    
    print_success "Paketet avinstallerat"
}

# Kontrollera paketets innehåll
check_package() {
    print_info "Kontrollerar paketets innehåll..."
    
    if [ -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        python -m twine check dist/*
        print_success "Paketet verifierat"
        
        print_info "Innehåll i wheel-paketet:"
        python -m zipfile -l dist/nexus_repository_api-1.0.0-py3-none-any.whl
    else
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
}

# Bygg Docker-image för GitLab CI/CD
build_docker_gitlab() {
    print_info "Bygger Docker-image för GitLab CI/CD..."
    
    # Kontrollera att wheel-paketet finns
    if [ ! -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
    
    # Bygg Docker-image med GitLab Dockerfile
    docker build -f "$PROJECT_ROOT/Dockerfile.gitlab" -t nexus-lab-gitlab:latest "$PROJECT_ROOT"
    
    if [ $? -eq 0 ]; then
        print_success "GitLab Docker-image byggd: nexus-lab-gitlab:latest"
        
        # Visa image-information
        print_info "Docker-image information:"
        docker images nexus-lab-gitlab:latest
        
        print_info "För att testa GitLab Docker-image:"
        print_info "  docker run -p 3000:3000 nexus-lab-gitlab:latest"
        print_info "  curl http://localhost:3000/health"
        
        print_info "För att testa upload i GitLab CI/CD miljö:"
        print_info "  docker run -e CI_PROJECT_ID=10 -e TWINE_USERNAME=__token__ -e TWINE_PASSWORD=your_token nexus-lab-gitlab:latest /app/upload.sh"
    else
        print_error "GitLab Docker-image kunde inte byggas"
        exit 1
    fi
}

# Bygg Docker-image
build_docker() {
    print_info "Bygger Docker-image med pip-paketet..."
    
    # Kontrollera att wheel-paketet finns
    if [ ! -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
    
    # Bygg Docker-image
    docker build -t nexus-repository-api:latest "$PROJECT_ROOT"
    
    if [ $? -eq 0 ]; then
        print_success "Docker-image byggd: nexus-repository-api:latest"
        
        # Visa image-information
        print_info "Docker-image information:"
        docker images nexus-repository-api:latest
        
        print_info "För att testa Docker-image:"
        print_info "  docker run -p 3000:3000 nexus-repository-api:latest"
        print_info "  curl http://localhost:3000/health"
    else
        print_error "Docker-image kunde inte byggas"
        exit 1
    fi
}

# Ladda upp paketet till TestPyPI för testning
upload_testpypi() {
    print_info "Laddar upp paketet till TestPyPI för testning..."
    
    # Kontrollera att wheel-paketet finns
    if [ ! -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
    
    # Kontrollera att twine är installerat
    if ! command -v twine &> /dev/null; then
        print_info "Installerar twine för upload..."
        if [ -d "venv" ]; then
            source venv/bin/activate
            pip install twine
        else
            pip3 install twine
        fi
    fi
    
    print_info "Uploading to TestPyPI..."
    print_info "Du behöver skapa ett konto på https://test.pypi.org/"
    print_info "och skapa en API token för att ladda upp"
    
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Ladda upp till TestPyPI
    twine upload --repository testpypi --verbose dist/*
    
    upload_result=$?
    
    if [ $upload_result -eq 0 ]; then
        print_success "Paketet har laddats upp till TestPyPI!"
        
        print_info "För att installera från TestPyPI:"
        print_info "  pip install --index-url https://test.pypi.org/simple/ nexus-repository-api"
        print_info ""
        print_info "För att använda som extra index:"
        print_info "  pip install --extra-index-url https://test.pypi.org/simple/ nexus-repository-api"
    else
        print_error "Upload till TestPyPI misslyckades."
        print_info "Tips: Kontrollera att du har rätt TestPyPI credentials"
        exit 1
    fi
}

# Ladda upp paketet till privat PyPI-repository
upload_package() {
    print_info "Laddar upp paketet till privat PyPI-repository..."
    
    # Kontrollera att wheel-paketet finns
    if [ ! -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
    
    # Kontrollera att twine är installerat
    if ! command -v twine &> /dev/null; then
        print_info "Installerar twine för upload..."
        if [ -d "venv" ]; then
            source venv/bin/activate
            pip install twine
        else
            pip3 install twine
        fi
    fi
    
    # Repository URL
    if [ -n "$CI_API_V4_URL" ] && [ -n "$CI_PROJECT_ID" ]; then
        # GitLab CI/CD environment - använd CI variabler
        REPO_URL="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi"
        print_info "Using GitLab CI/CD environment variables"
    else
        # Lokal utveckling - använd hårdkodad URL
        REPO_URL="https://git.idp.ip-solutions.se/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi"
    fi
    
    print_info "Repository URL: $REPO_URL"
    
    # Kontrollera om environment variabler finns (GitLab CI/CD stil)
    if [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ]; then
        print_success "Hittade TWINE environment variabler!"
        print_info "Använder TWINE_USERNAME och TWINE_PASSWORD"
        print_info "För GitLab Package Registry använd användarnamn som TWINE_USERNAME"
        print_info "och access token som TWINE_PASSWORD"
        USE_ENV_VARS=true
    # Kontrollera om .pypirc finns eller om vi kan skapa en från credentials
    elif [ -f ".pypirc" ] && ! grep -q "din_gitlab_username_här" .pypirc && ! grep -q "din_gitlab_token_här" .pypirc; then
        print_success "Hittade .pypirc konfigurationsfil med giltiga credentials!"
        print_info "Använder autentisering från .pypirc"
        USE_ENV_VARS=false
    elif [ -f "../mina-credentials.txt" ]; then
        print_info "Hittade mina-credentials.txt fil!"
        print_info "Skapar .pypirc från credentials..."
        
        # Läs credentials från filen
        source ../mina-credentials.txt
        
        # Kontrollera att credentials är satta
        if [ -z "$GITLAB_USERNAME" ] || [ -z "$GITLAB_TOKEN" ] || [ "$GITLAB_USERNAME" = "din_gitlab_username_här" ] || [ "$GITLAB_TOKEN" = "din_gitlab_token_här" ]; then
            print_error "mina-credentials.txt innehåller inte giltiga credentials!"
            print_info "Uppdatera filen med dina riktiga GitLab uppgifter:"
            print_info "  GITLAB_USERNAME=din_riktiga_username"
            print_info "  GITLAB_TOKEN=din_riktiga_token"
            exit 1
        fi
        
        # Skapa temporär .pypirc fil
        cat > .pypirc.tmp << EOF
[distutils]
index-servers = gitlab

[gitlab]
repository = https://git.idp.ip-solutions.se/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi/simple
username = $GITLAB_USERNAME
password = $GITLAB_TOKEN
EOF
        
        print_success "Skapade temporär .pypirc med dina credentials!"
    else
        print_warning "Ingen .pypirc eller mina-credentials.txt fil hittades!"
        print_info ""
        print_info "Du kan antingen:"
        print_info "1. Skapa en mina-credentials.txt fil med dina credentials (rekommenderat)"
        print_info "2. Skapa en .pypirc fil direkt"
        print_info "3. Använda dina GitLab credentials när twine frågar efter dem"
        print_info "4. Ställa in environment variabler:"
        print_info "   export TWINE_USERNAME=din_gitlab_username"
        print_info "   export TWINE_PASSWORD=din_gitlab_token"
        print_info ""
        print_info "För att skapa en GitLab access token:"
        print_info "  1. Gå till GitLab > Settings > Access Tokens"
        print_info "  2. Skapa en token med 'write_repository' scope"
        print_info "  3. Använd token som lösenord i twine"
        print_info ""
    fi
    
    print_info "Uploading packages..."
    
    # Debug-information
    print_info "=== DEBUG INFORMATION ==="
    print_info "GitLab Project ID: $GITLAB_PROJECT_ID"
    print_info "Package Name: $PACKAGE_NAME"
    print_info "Repository URL: $REPO_URL"
    print_info "Working directory: $(pwd)"
    print_info "Dist files:"
    ls -la dist/
    print_info "Virtual environment exists: $([ -d "venv" ] && echo "Yes" || echo "No")"
    print_info "Environment variables:"
    [ -n "$TWINE_USERNAME" ] && print_info "  TWINE_USERNAME: Set" || print_info "  TWINE_USERNAME: Not set"
    [ -n "$TWINE_PASSWORD" ] && print_info "  TWINE_PASSWORD: Set" || print_info "  TWINE_PASSWORD: Not set"
    [ -n "$CI_API_V4_URL" ] && print_info "  CI_API_V4_URL: Set" || print_info "  CI_API_V4_URL: Not set"
    [ -n "$CI_PROJECT_ID" ] && print_info "  CI_PROJECT_ID: Set" || print_info "  CI_PROJECT_ID: Not set"
    print_info "Config files:"
    [ -f ".pypirc" ] && print_info "  .pypirc: $(wc -l < .pypirc) lines" || print_info "  .pypirc: Not found"
    [ -f ".pypirc.tmp" ] && print_info "  .pypirc.tmp: $(wc -l < .pypirc.tmp) lines" || print_info "  .pypirc.tmp: Not found"
    
    # Testa anslutning först
    print_info "Testing connection to repository..."
    if curl -s -I "$REPO_URL" > /dev/null 2>&1; then
        print_success "Repository URL is reachable"
    else
        print_warning "Repository URL might not be reachable"
        print_info "Trying alternative URL formats..."
        ALT_URL1="https://git.idp.ip-solutions.se/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi/simple"
        ALT_URL2="https://git.idp.ip-solutions.se/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi/simple/nexus_repository_api"
        
        if curl -s -I "$ALT_URL1" > /dev/null 2>&1; then
            print_success "Alternative URL 1 is reachable: $ALT_URL1"
        else
            print_warning "Alternative URL 1 not reachable: $ALT_URL1"
        fi
        
        if curl -s -I "$ALT_URL2" > /dev/null 2>&1; then
            print_success "Alternative URL 2 is reachable: $ALT_URL2"
        else
            print_warning "Alternative URL 2 not reachable: $ALT_URL2"
        fi
    fi
    
    print_info "=== END DEBUG ==="
    
    # Ladda upp med twine
    if [ -d "venv" ]; then
        source venv/bin/activate
        print_info "Using virtual environment"
    else
        print_info "No virtual environment, using system Python"
    fi
    
    # Välj upload-metod baserat på tillgängliga credentials
    if [ "$USE_ENV_VARS" = true ]; then
        print_info "Using environment variables for authentication"
        print_info "TWINE_USERNAME: $TWINE_USERNAME"
        print_info "TWINE_PASSWORD: [HIDDEN]"
        twine upload --non-interactive --repository-url "$REPO_URL" --username "$TWINE_USERNAME" --password "$TWINE_PASSWORD" --verbose dist/*
    elif [ -f ".pypirc.tmp" ]; then
        print_info "Using temporary .pypirc file"
        print_info "Config file contents:"
        cat .pypirc.tmp
        twine upload --non-interactive --config-file .pypirc.tmp --repository gitlab --verbose dist/*
    elif [ -f ".pypirc" ]; then
        print_info "Using existing .pypirc file"
        print_info "Config file contents:"
        cat .pypirc
        twine upload --non-interactive --repository gitlab --verbose dist/*
    else
        print_info "Using direct repository URL"
        twine upload --non-interactive --repository-url "$REPO_URL" --verbose dist/*
    fi
    
    # Spara upload-resultatet
    upload_result=$?
    
    print_info "=== UPLOAD RESULT DEBUG ==="
    print_info "Upload exit code: $upload_result"
    print_info "Last command status: $?"
    
    # Rensa upp temporär .pypirc fil
    if [ -f ".pypirc.tmp" ]; then
        rm -f .pypirc.tmp
        print_info "Rensade temporär .pypirc fil"
    fi
    
    if [ $upload_result -eq 0 ]; then
        print_success "Paketet har laddats upp till privat PyPI-repository!"
        
        print_info "För att installera från privat repository:"
        print_info "  pip install --index-url $REPO_URL nexus-repository-api"
        print_info ""
        print_info "För att använda som extra index:"
        print_info "  pip install --extra-index-url $REPO_URL nexus-repository-api"
    else
        print_error "Upload misslyckades. Kontrollera autentisering och nätverksanslutning."
        print_info "=== TROUBLESHOOTING TIPS ==="
        print_info "1. Kontrollera att GitLab credentials är korrekta"
        print_info "2. Verifiera att PyPI-paketet är aktiverat för projektet (ID: $GITLAB_PROJECT_ID)"
        print_info "3. Kontrollera att du har rätt behörigheter (write_repository)"
        print_info "4. Testa repository URL:en manuellt:"
        print_info "   curl -I $REPO_URL"
        print_info "5. Kontrollera GitLab project settings för Package Registry"
        print_info "6. Kontrollera att GITLAB_PROJECT_ID är korrekt:"
        print_info "   GITLAB_PROJECT_ID=123 $0 upload"
        print_info "7. Kontrollera att PACKAGE_NAME är korrekt:"
        print_info "   PACKAGE_NAME=my-package $0 upload"
        print_info "=== END TROUBLESHOOTING ==="
        exit 1
    fi
}

# Huvudfunktion
main() {
    print_info "🚀 Nexus Repository API - Pip Package Builder"
    print_info "============================================="
    
    check_python
    
    case "${1:-build}" in
        "build")
            create_venv
            activate_venv
            install_build_tools
            build_package
            ;;
        "clean")
            clean_build
            ;;
        "test")
            run_tests
            ;;
        "install")
            install_package
            ;;
        "uninstall")
            uninstall_package
            ;;
        "check")
            check_package
            ;;
        "docker")
            build_docker
            ;;
        "docker-gitlab")
            build_docker_gitlab
            ;;
        "upload")
            upload_package
            ;;
        "upload-testpypi")
            upload_testpypi
            ;;
        "local-install")
            local_install
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Okänt kommando: $1"
            show_help
            exit 1
            ;;
    esac
}

# Kör huvudfunktionen med alla argument
main "$@"