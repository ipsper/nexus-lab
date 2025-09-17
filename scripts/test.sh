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
    echo "  api          Kör API/integration-tester i Docker-container (utan GUI)"
    echo "  gui          Kör GUI-tester med Playwright i Docker-container"
    echo "  k8s          Kör Kubernetes-integrationstester på host"
    echo "  all          Kör alla tester (api + gui + k8s)"
    echo "  health       Kontrollera att miljön är uppe och redo"
    echo "  rebuild      Stoppa, bygg om och starta test-containern"
    echo "  verbose      Kör med verbose output (lägg till före testtyp)"
    echo "  help         Visa denna hjälp"
    echo ""
    echo "EXTRA_ARGS:"
    echo "  Alla extra argument skickas vidare till pytest"
    echo "  --to-the-end     Fortsätt även om tester misslyckas (default: stopp vid första fel)"
    echo ""
    echo "EXEMPEL:"
    echo "  $0 api                    # Kör alla API-tester i Docker (utan GUI)"
    echo "  $0 gui                    # Kör alla GUI-tester med Playwright"
    echo "  $0 k8s                    # Kör alla K8s-tester på host"
    echo "  $0 api -k test_fastapi    # Kör bara FastAPI-tester"
    echo "  $0 gui -k test_docs       # Kör bara docs GUI-tester"
    echo "  $0 k8s --tb=long          # Kör K8s-tester med verbose traceback"
    echo "  $0 all                    # Kör alla tester (api + gui + k8s)"
    echo "  $0 health                 # Kontrollera miljön först"
    echo "  $0 rebuild                # Bygg om test-containern"
    echo "  $0 verbose gui            # Kör GUI-tester med verbose output"
    echo "  $0 api -v -s              # Verbose + visa print statements"
    echo "  $0 all --to-the-end       # Kör alla tester utan att stanna vid fel"
    echo "  $0 api -x                 # Stoppa vid första fel (default)"
    echo ""
    echo "MILJÖER:"
    echo "  API-tester   - Körs i Docker-container som extern klient"
    echo "  K8s-tester   - Körs på host-systemet med kubectl-tillgång"
    echo ""
}

# Hantera flaggor och returnera processed args
process_args() {
    local to_the_end=false
    local processed_args=()
    
    for arg in "$@"; do
        case "$arg" in
            --to-the-end)
                to_the_end=true
                ;;
            *)
                processed_args+=("$arg")
                ;;
        esac
    done
    
    # Lägg till -x (stopp vid första fel) som default om inte --to-the-end
    if [[ "$to_the_end" == false ]]; then
        processed_args=("-x" "${processed_args[@]}")
    fi
    
    echo "${processed_args[@]}"
}

# Kör API-tester i Docker (utan GUI)
run_api_tests() {
    local pytest_args
    pytest_args=$(process_args "$@")
    
    print_info "🐳 Kör API/integration-tester i Docker-container (utan GUI)..."
    print_info "Args: $pytest_args"
    
    # Anropa befintligt run-test.sh script med exkludering av GUI-tester
    ./scripts/run-test.sh run $pytest_args -m "not gui"
}

# Kör GUI-tester i Docker
run_gui_tests() {
    local pytest_args
    pytest_args=$(process_args "$@")
    
    print_info "🎭 Kör GUI-tester med Playwright i Docker-container..."
    print_info "Args: $pytest_args"
    
    # Anropa befintligt run-test.sh script med bara GUI-tester
    ./scripts/run-test.sh run $pytest_args -m gui
}

# Kör health checks
run_health_checks() {
    local pytest_args
    pytest_args=$(process_args "$@")
    print_info "🏥 Kontrollerar miljöns hälsa..."
    print_info "Args: $pytest_args"
    ./scripts/run-test.sh run $pytest_args -m health
}

# Bygg om test-container
rebuild_test_container() {
    print_info "🔄 Bygger om test-containern..."
    print_info "Stoppar befintliga test-containers..."
    docker stop $(docker ps -q --filter ancestor=nexus-test:latest) 2>/dev/null || true
    docker rm $(docker ps -aq --filter ancestor=nexus-test:latest) 2>/dev/null || true
    print_info "Tar bort befintlig test-image..."
    docker rmi nexus-test:latest 2>/dev/null || true
    print_info "Bygger ny test-container..."
    ./scripts/run-test.sh build
    print_success "✅ Test-container ombyggd och redo!"
    if [[ $# -gt 0 ]]; then
        print_info "Kör tester med nya containern..."
        run_api_tests "$@"
    fi
}

# Kör med verbose output
run_verbose() {
    local test_type="$1"
    shift
    
    # Separera --to-the-end från andra args
    local to_the_end_args=()
    local other_args=()
    
    for arg in "$@"; do
        case "$arg" in
            --to-the-end)
                to_the_end_args+=("$arg")
                ;;
            *)
                other_args+=("$arg")
                ;;
        esac
    done
    
    local pytest_args=("-v" "-s" "--tb=long" "${other_args[@]}" "${to_the_end_args[@]}")
    
    print_info "🔊 Verbose mode aktiverat"
    
    case "$test_type" in
        api)
            run_api_tests "${pytest_args[@]}"
            ;;
        gui)
            run_gui_tests "${pytest_args[@]}"
            ;;
        k8s)
            run_k8s_tests "${pytest_args[@]}"
            ;;
        all)
            run_all_tests "${pytest_args[@]}"
            ;;
        health)
            run_health_checks "${pytest_args[@]}"
            ;;
        *)
            print_error "Okänt testtyp för verbose mode: $test_type"
            show_help
            exit 1
            ;;
    esac
}

# Kör K8s-tester på host
run_k8s_tests() {
    local pytest_args
    pytest_args=$(process_args "$@")
    
    print_info "⚙️  Kör Kubernetes-integrationstester på host..."
    print_info "Args: $pytest_args"
    
    # Anropa befintligt run-k8s-tests.sh script
    ./scripts/run-k8s-tests.sh run $pytest_args
}

# Kör alla tester
run_all_tests() {
    local to_the_end=false
    local pytest_args=()
    
    # Kontrollera om --to-the-end finns
    for arg in "$@"; do
        case "$arg" in
            --to-the-end)
                to_the_end=true
                ;;
            *)
                pytest_args+=("$arg")
                ;;
        esac
    done
    
    print_info "🚀 Kör alla tester (Health + API + GUI + K8s)..."
    if [[ "$to_the_end" == true ]]; then
        print_info "🔄 --to-the-end aktiverat: Fortsätter även om steg misslyckas"
    else
        print_info "⏹️  Default: Stoppar vid första fel"
    fi
    echo ""
    
    local health_success=true
    local api_success=true
    local gui_success=true
    local k8s_success=true
    
    print_info "=== STEG 1: Health Checks ==="
    if run_health_checks "${pytest_args[@]}"; then
        print_success "Health checks slutförda ✅"
    else
        print_error "Health checks misslyckades ❌ - Miljön är inte redo"
        print_warning "💡 Starta tjänsterna först med: ./scripts/run.sh"
        health_success=false
        if [[ "$to_the_end" == false ]]; then
            return 1
        fi
    fi
    echo ""
    
    print_info "=== STEG 2: API/Integration-tester ==="
    if run_api_tests "${pytest_args[@]}"; then
        print_success "API-tester slutförda ✅"
    else
        print_error "API-tester misslyckades ❌"
        api_success=false
        if [[ "$to_the_end" == false ]]; then
            return 1
        fi
    fi
    echo ""
    
    print_info "=== STEG 3: GUI-tester ==="
    if run_gui_tests "${pytest_args[@]}"; then
        print_success "GUI-tester slutförda ✅"
    else
        print_error "GUI-tester misslyckades ❌"
        gui_success=false
        if [[ "$to_the_end" == false ]]; then
            return 1
        fi
    fi
    echo ""
    
    print_info "=== STEG 4: Kubernetes-integrationstester ==="
    if run_k8s_tests "${pytest_args[@]}"; then
        print_success "K8s-tester slutförda ✅"
    else
        print_error "K8s-tester misslyckades ❌"
        k8s_success=false
        if [[ "$to_the_end" == false ]]; then
            return 1
        fi
    fi
    echo ""
    
    # Sammanfattning
    if [[ "$health_success" == true && "$api_success" == true && "$gui_success" == true && "$k8s_success" == true ]]; then
        print_success "🎉 Alla tester slutförda framgångsrikt!"
        return 0
    else
        print_warning "⚠️  Sammanfattning:"
        [[ "$health_success" == true ]] && print_success "  ✅ Health checks" || print_error "  ❌ Health checks"
        [[ "$api_success" == true ]] && print_success "  ✅ API-tester" || print_error "  ❌ API-tester"
        [[ "$gui_success" == true ]] && print_success "  ✅ GUI-tester" || print_error "  ❌ GUI-tester"
        [[ "$k8s_success" == true ]] && print_success "  ✅ K8s-tester" || print_error "  ❌ K8s-tester"
        return 1
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
        api)
            shift  # Ta bort 'api' från argument-listan
            run_api_tests "$@"
            ;;
        gui)
            shift  # Ta bort 'gui' från argument-listan
            run_gui_tests "$@"
            ;;
        k8s)
            shift  # Ta bort 'k8s' från argument-listan
            run_k8s_tests "$@"
            ;;
        all)
            shift  # Ta bort 'all' från argument-listan
            run_all_tests "$@"
            ;;
        health)
            shift
            run_health_checks "$@"
            ;;
        rebuild)
            shift
            rebuild_test_container "$@"
            ;;
        verbose)
            shift
            if [[ $# -eq 0 ]]; then
                print_error "Verbose kräver en testtyp (api, k8s, all, health)"
                show_help
                exit 1
            fi
            run_verbose "$@"
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
