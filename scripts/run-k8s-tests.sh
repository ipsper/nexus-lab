#!/bin/bash

# Script för att köra Kubernetes-integrationstester på host-systemet
# Dessa tester kräver kubectl och tillgång till Kind-klustret

set -e

# Färgkoder
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hjälpfunktioner för utskrifter
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

# Kontrollera att kubectl finns
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl kunde inte hittas. Installera kubectl först."
        exit 1
    fi
}

# Kontrollera att Kind-klustret körs
check_cluster() {
    if ! kubectl cluster-info --context kind-nexus-cluster &> /dev/null; then
        print_error "Kind-kluster 'nexus-cluster' är inte tillgängligt."
        print_info "Starta klustret med: ./scripts/run.sh create"
        exit 1
    fi
}

# Skapa och aktivera virtual environment för K8s-tester
setup_venv() {
    local venv_dir="$(dirname "$0")/../k8s-test-venv"
    
    if [[ ! -d "$venv_dir" ]]; then
        print_info "Skapar virtual environment för K8s-tester..."
        python3 -m venv "$venv_dir"
        
        if [[ $? -ne 0 ]]; then
            print_error "Kunde inte skapa virtual environment"
            exit 1
        fi
        
        print_success "Virtual environment skapad: $venv_dir"
    fi
    
    print_info "Aktiverar virtual environment..."
    source "$venv_dir/bin/activate"
    
    # Kontrollera om dependencies behöver installeras
    if ! python -c "import pytest" 2>/dev/null; then
        print_info "Installerar test dependencies..."
        pip install --quiet pytest requests kubernetes
        
        if [[ $? -ne 0 ]]; then
            print_error "Kunde inte installera dependencies"
            exit 1
        fi
        
        print_success "Dependencies installerade"
    fi
}

# Kontrollera att Python finns
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "python3 kunde inte hittas."
        exit 1
    fi
    
    setup_venv
    
    print_success "Python miljö är redo"
}

# Huvudfunktion för att köra K8s-tester
run_k8s_tests() {
    print_info "Kör Kubernetes-integrationstester på host-systemet..."
    
    # Gå till testning-katalogen
    cd "$(dirname "$0")/../testning"
    
    # Kör bara K8s-tester
    python3 -m pytest -v -m k8s --tb=short --color=yes
    
    print_success "K8s-tester slutförda!"
}

# Rensa virtual environment
clean_venv() {
    local venv_dir="$(dirname "$0")/../k8s-test-venv"
    
    if [[ -d "$venv_dir" ]]; then
        print_info "Tar bort virtual environment: $venv_dir"
        rm -rf "$venv_dir"
        print_success "Virtual environment borttagen"
    else
        print_info "Ingen virtual environment att rensa"
    fi
}

# Visa hjälp
show_help() {
    echo "Kubernetes Integration Test Runner"
    echo ""
    echo "Användning: $0 [KOMMANDO]"
    echo ""
    echo "Kommandon:"
    echo "  run          Kör K8s-integrationstester"
    echo "  check        Kontrollera att miljön är redo"
    echo "  clean        Rensa virtual environment"
    echo "  help         Visa denna hjälp"
    echo ""
    echo "Exempel:"
    echo "  $0 run       # Kör alla K8s-tester"
    echo "  $0 clean     # Rensa venv (kommer skapas igen vid nästa körning)"
    echo ""
    echo "Notera:"
    echo "  - Skapar automatiskt en isolerad venv i k8s-test-venv/"
    echo "  - Installerar endast nödvändiga dependencies (pytest, requests, kubernetes)"
    echo "  - Kräver kubectl och tillgång till Kind-klustret"
    echo ""
}

# Kontrollera miljön
check_environment() {
    print_info "Kontrollerar testmiljö..."
    
    check_kubectl
    print_success "kubectl är tillgängligt"
    
    check_cluster
    print_success "Kind-kluster är tillgängligt"
    
    check_python
    print_success "Python och pytest är tillgängliga"
    
    print_success "Miljön är redo för K8s-tester!"
}

# Huvudlogik
case "${1:-run}" in
    run)
        check_environment
        run_k8s_tests
        ;;
    check)
        check_environment
        ;;
    clean)
        clean_venv
        ;;
    help)
        show_help
        ;;
    *)
        print_error "Okänt kommando: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
