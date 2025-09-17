#!/bin/bash

# Gemensamt test-script för alla typer av tester
# Användning: ./scripts/test.sh [TESTTYP] [EXTRA_ARGS...]

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

# Visa hjälp
show_help() {
    echo "Nexus Lab Test Runner"
    echo ""
    echo "Användning: $0 [TESTTYP] [EXTRA_ARGS...]"
    echo ""
    echo "TESTTYPER:"
    echo "  health       Kontrollera att miljön är uppe och redo"
    echo "  api          Kör API/integration-tester i Docker-container"
    echo "  k8s          Kör Kubernetes-integrationstester på host"
    echo "  all          Kör alla tester (både api och k8s)"
    echo "  rebuild      Stoppa, bygg om och starta test-containern"
    echo "  help         Visa denna hjälp"
    echo ""
    echo "EXTRA_ARGS:"
    echo "  Alla extra argument skickas vidare till pytest"
    echo ""
    echo "EXEMPEL:"
    echo "  $0 health                 # Kontrollera miljön först"
    echo "  $0 api                    # Kör alla API-tester i Docker"
    echo "  $0 k8s                    # Kör alla K8s-tester på host"
    echo "  $0 api -k test_fastapi    # Kör bara FastAPI-tester"
    echo "  $0 k8s --tb=long          # Kör K8s-tester med verbose traceback"
    echo "  $0 all                    # Kör alla tester"
    echo "  $0 rebuild                # Bygg om test-containern"
    echo "  $0 rebuild -k test_gui    # Bygg om och kör GUI-tester"
    echo ""
    echo "MILJÖER:"
    echo "  API-tester   - Körs i Docker-container som extern klient"
    echo "  K8s-tester   - Körs på host-systemet med kubectl-tillgång"
    echo ""
}

# Kör health checks
run_health_checks() {
    local pytest_args="$*"
    
    print_info "🏥 Kontrollerar miljöns hälsa..."
    print_info "Args: $pytest_args"
    
    # Kör bara health check-tester
    ./scripts/run-test.sh run -m health $pytest_args
}

# Kör API-tester i Docker
run_api_tests() {
    local pytest_args="$*"
    
    print_info "🐳 Kör API/integration-tester i Docker-container..."
    print_info "Args: $pytest_args"
    
    # Anropa befintligt run-test.sh script
    ./scripts/run-test.sh run $pytest_args
}

# Kör K8s-tester på host
run_k8s_tests() {
    local pytest_args="$*"
    
    print_info "⚙️  Kör Kubernetes-integrationstester på host..."
    print_info "Args: $pytest_args"
    
    # Anropa befintligt run-k8s-tests.sh script
    ./scripts/run-k8s-tests.sh run $pytest_args
}

# Kör alla tester
run_all_tests() {
    local pytest_args="$*"
    
    print_info "🚀 Kör alla tester (Health + API + K8s)..."
    echo ""
    
    # Kör health checks först
    print_info "=== STEG 1: Health Checks ==="
    if run_health_checks $pytest_args; then
        print_success "Health checks slutförda ✅"
    else
        print_error "Health checks misslyckades ❌ - Miljön är inte redo"
        print_warning "💡 Starta tjänsterna först med: ./scripts/run.sh"
        return 1
    fi
    
    echo ""
    
    # Kör API-tester sedan
    print_info "=== STEG 2: API/Integration-tester ==="
    if run_api_tests $pytest_args; then
        print_success "API-tester slutförda ✅"
    else
        print_error "API-tester misslyckades ❌"
        return 1
    fi
    
    echo ""
    
    # Kör K8s-tester sist
    print_info "=== STEG 3: Kubernetes-integrationstester ==="
    if run_k8s_tests $pytest_args; then
        print_success "K8s-tester slutförda ✅"
    else
        print_error "K8s-tester misslyckades ❌"
        return 1
    fi
    
    echo ""
    print_success "🎉 Alla tester slutförda framgångsrikt!"
}

# Stoppa, bygg om och starta test-containern
rebuild_test_container() {
    print_info "🔄 Bygger om test-containern..."
    
    # Stoppa och ta bort befintliga containers
    print_info "Stoppar befintliga test-containers..."
    docker stop $(docker ps -q --filter ancestor=nexus-test:latest) 2>/dev/null || true
    docker rm $(docker ps -aq --filter ancestor=nexus-test:latest) 2>/dev/null || true
    
    # Ta bort befintlig image
    print_info "Tar bort befintlig test-image..."
    docker rmi nexus-test:latest 2>/dev/null || true
    
    # Bygg ny image
    print_info "Bygger ny test-container..."
    ./scripts/run-test.sh build
    
    print_success "✅ Test-container ombyggd och redo!"
    
    # Kör tester om extra argument givits
    if [[ $# -gt 0 ]]; then
        print_info "Kör tester med nya containern..."
        run_api_tests "$@"
    fi
}

# Kontrollera att nödvändiga scripts finns
check_scripts() {
    if [[ ! -f "./scripts/run-test.sh" ]]; then
        print_error "run-test.sh hittades inte"
        exit 1
    fi
    
    if [[ ! -f "./scripts/run-k8s-tests.sh" ]]; then
        print_error "run-k8s-tests.sh hittades inte"
        exit 1
    fi
    
    # Gör scripts körbara
    chmod +x ./scripts/run-test.sh
    chmod +x ./scripts/run-k8s-tests.sh
}

# Huvudlogik
main() {
    check_scripts
    
    case "${1:-help}" in
        health)
            shift  # Ta bort 'health' från argument-listan
            run_health_checks "$@"
            ;;
        api)
            shift  # Ta bort 'api' från argument-listan
            run_api_tests "$@"
            ;;
        k8s)
            shift  # Ta bort 'k8s' från argument-listan
            run_k8s_tests "$@"
            ;;
        all)
            shift  # Ta bort 'all' från argument-listan
            run_all_tests "$@"
            ;;
        rebuild)
            shift  # Ta bort 'rebuild' från argument-listan
            rebuild_test_container "$@"
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
