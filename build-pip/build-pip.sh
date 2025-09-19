#!/bin/bash

# Nexus Repository API - Pip Package Build Script
# Detta skript bygger pip-paketet med hjälp av en virtuell miljö

set -e  # Avsluta vid fel

# Sätt arbetskatalog till build-pip mappen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

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
    echo "  docker            Bygg Docker-image med pip-paketet"
    echo "  help              Visa denna hjälp"
    echo ""
    echo "Exempel:"
    echo "  $0 build"
    echo "  $0 build test"
    echo "  $0 clean build install"
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
    source venv/bin/activate
    print_success "Virtuell miljö aktiverad"
}

# Installera build-verktyg
install_build_tools() {
    print_info "Installerar build-verktyg..."
    pip install --upgrade pip
    pip install build twine
    print_success "Build-verktyg installerade"
}

# Rensa build-artefakter
clean_build() {
    print_info "Rensar build-artefakter..."
    
    # Ta bort gamla builds
    rm -rf dist/
    rm -rf build/
    rm -rf *.egg-info/
    
    # Ta bort virtuell miljö om den finns
    if [ -d "venv" ]; then
        rm -rf venv/
        print_info "Virtuell miljö borttagen"
    fi
    
    print_success "Build-artefakter rensade"
}

# Bygg paketet
build_package() {
    print_info "Bygger pip-paketet..."
    
    # Kontrollera att vi är i virtuell miljö
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtuell miljö är inte aktiverad. Kör skriptet igen."
        exit 1
    fi
    
    # Bygg paketet
    python -m build
    
    # Kontrollera att bygget lyckades
    if [ -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_success "Wheel-paket byggt: dist/nexus_repository_api-1.0.0-py3-none-any.whl"
    else
        print_error "Wheel-paketet kunde inte byggas"
        exit 1
    fi
    
    if [ -f "dist/nexus_repository_api-1.0.0.tar.gz" ]; then
        print_success "Source distribution byggd: dist/nexus_repository_api-1.0.0.tar.gz"
    else
        print_error "Source distribution kunde inte byggas"
        exit 1
    fi
    
    # Visa paketinformation
    print_info "Paketinformation:"
    ls -la dist/
    
    # Kontrollera paketets innehåll
    print_info "Kontrollerar paketets innehåll..."
    python -m twine check dist/*
    
    print_success "Pip-paketet byggt framgångsrikt!"
}

# Kör tester
run_tests() {
    print_info "Kör tester..."
    
    # Kontrollera att vi är i virtuell miljö
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtuell miljö är inte aktiverad. Kör skriptet igen."
        exit 1
    fi
    
    # Installera test-dependencies
    pip install -e ".[dev]"
    
    # Kör tester
    python -m pytest tests/ -v
    
    print_success "Tester körda framgångsrikt!"
}

# Installera paketet lokalt
install_package() {
    print_info "Installerar paketet lokalt för testning..."
    
    # Kontrollera att vi är i virtuell miljö
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtuell miljö är inte aktiverad. Kör skriptet igen."
        exit 1
    fi
    
    # Installera från wheel-fil
    pip install dist/nexus_repository_api-1.0.0-py3-none-any.whl
    
    print_success "Paketet installerat lokalt"
    
    # Testa att kommandot fungerar
    print_info "Testar att nexus-api kommandot fungerar..."
    nexus-api --version
    
    print_success "Installation verifierad!"
}

# Avinstallera paketet
uninstall_package() {
    print_info "Avinstallerar paketet..."
    
    # Kontrollera att vi är i virtuell miljö
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtuell miljö är inte aktiverad. Kör skriptet igen."
        exit 1
    fi
    
    pip uninstall -y nexus-repository-api
    
    print_success "Paketet avinstallerat"
}

# Kontrollera paketets innehåll
check_package() {
    print_info "Kontrollerar paketets innehåll..."
    
    if [ ! -f "dist/nexus_repository_api-1.0.0-py3-none-any.whl" ]; then
        print_error "Wheel-paketet finns inte. Bygg paketet först med 'build'"
        exit 1
    fi
    
    # Visa innehållet i wheel-filen
    print_info "Innehåll i wheel-paketet:"
    python -m zipfile -l dist/nexus_repository_api-1.0.0-py3-none-any.whl
    
    # Kontrollera med twine
    print_info "Twine-kontroll:"
    python -m twine check dist/*
    
    print_success "Paketkontroll klar!"
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
    docker build -t nexus-repository-api:latest .
    
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

# Huvudfunktion
main() {
    print_info "🚀 Nexus Repository API - Pip Package Builder"
    print_info "============================================="
    
    # Kontrollera Python
    check_python
    
    # Hantera kommandon
    case "${1:-build}" in
        build)
            create_venv
            activate_venv
            install_build_tools
            build_package
            ;;
        clean)
            clean_build
            ;;
        test)
            if [ -z "$VIRTUAL_ENV" ]; then
                print_error "Virtuell miljö är inte aktiverad. Kör 'build' först."
                exit 1
            fi
            run_tests
            ;;
        install)
            if [ -z "$VIRTUAL_ENV" ]; then
                print_error "Virtuell miljö är inte aktiverad. Kör 'build' först."
                exit 1
            fi
            install_package
            ;;
        uninstall)
            if [ -z "$VIRTUAL_ENV" ]; then
                print_error "Virtuell miljö är inte aktiverad. Kör 'build' först."
                exit 1
            fi
            uninstall_package
            ;;
        check)
            check_package
            ;;
        docker)
            build_docker
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Okänt kommando: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Kör huvudfunktionen med alla argument
main "$@"
