#!/bin/bash

# Nexus Lab - Test Runner Script
# Kör pytest i en egen container utanför Kubernetes-klustret

set -e

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
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

# Help function
show_help() {
    echo "Nexus Lab - Test Runner"
    echo ""
    echo "Användning: $0 [KOMANDO]"
    echo ""
    echo "Kommandon:"
    echo "  run                 Kör custom pytest-kommando"
    echo "  run-all             Kör alla tester"
    echo "  run-health          Kör health checks (stannar vid första fel)"
    echo "  run-api             Kör API-tester utan GUI (stannar vid första fel)"
    echo "  run-gui             Kör GUI-tester (stannar vid första fel)"
    echo "  run-endpoints       Kör smarta endpoint-URL tester (stannar vid första fel)"
    echo "  run-basic           Kör grundläggande API-tester (stannar vid första fel)"
    echo "  run-errors          Kör error handling-tester (stannar vid första fel)"
    echo "  run-validation      Kör data-valideringstester (stannar vid första fel)"
    echo "  run-workflows       Kör end-to-end workflow-tester (stannar vid första fel)"
    echo "  run-scheduler       Kör schemaläggningstester (stannar vid första fel)"
    echo "  debug-env           Debugga test-miljön och URL:er"
    echo "  run-k8s             Kör K8s-tester (stannar vid första fel)"
    echo "  build               Bygg test-container (utan cache)"
    echo "  build --with-cache  Bygg test-container med cache"
    echo "  rebuild             Stoppa och bygg om test-container (utan cache)"
    echo "  rebuild --with-cache Stoppa och bygg om test-container med cache"
    echo "  restart             Starta om test-container (behåller kod-ändringar)"
    echo "  stop                Stoppa test-container"
    echo "  clean               Rensa test-containers och images"
    echo "  logs                Visa test-logs"
    echo "  help                Visa denna hjälp"
    echo ""
    echo "Miljövariabler (för att konfigurera test-URLs):"
    echo "  TEST_HOST           Host för tester (default: localhost)"
    echo "  TEST_PORT           Port för Kong Gateway (default: 8000)"
    echo "  KONG_ADMIN_PORT     Port för Kong Admin API (default: 8001)"
    echo "  NEXUS_DIRECT_PORT   Port för direkt Nexus-åtkomst (default: 8081)"
    echo ""
    echo "Exempel:"
    echo "  $0 run-health                  # Kör health checks (stannar vid fel)"
    echo "  $0 run-api                     # Kör API-tester (utan GUI)"
    echo "  $0 run-gui                     # Kör bara GUI-tester"
    echo "  $0 run-api --to-the-end        # Kör API-tester (fortsätt vid fel)"
    echo "  $0 run-gui --to-the-end        # Kör GUI-tester (fortsätt vid fel)"
    echo "  $0 run-endpoints               # Kör smarta endpoint-URL tester"
    echo "  $0 run -k test_health          # Kör custom pytest-kommando"
    echo "  TEST_HOST=192.168.1.100 $0 run-api  # Kör API-tester mot annan host"
    echo "  $0 build --with-cache          # Bygg test-container med cache"
    echo "  $0 rebuild                     # Stoppa och bygg om test-container"
    echo "  $0 restart                     # Starta om test-container (snabbare för kod-ändringar)"
    echo "  $0 stop                        # Stoppa test-container"
    echo ""
    echo "Tips:"
    echo "  - Test-containern monterar testning/ som volume, så kod-ändringar"
    echo "    i test/ och support/ mapparna är automatiskt tillgängliga"
    echo "  - Använd 'restart' istället för 'rebuild' när du bara ändrat test-kod"
    echo "  - Använd 'rebuild' när du ändrat requirements.txt eller Dockerfile"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker är inte igång. Starta Docker först."
        exit 1
    fi
}

# Check if Kind cluster exists
check_kind_cluster() {
    if ! kind get clusters | grep -q nexus-cluster; then
        print_warning "Kind-klustret 'nexus-cluster' finns inte."
        print_info "Kör './scripts/run.sh create' först för att skapa klustret."
        exit 1
    fi
}

# Build test container
build_test_container() {
    local no_cache="--no-cache"  # Default: no cache
    
    # Check for --with-cache argument
    for arg in "$@"; do
        if [[ "$arg" == "--with-cache" ]]; then
            no_cache=""
            break
        fi
    done
    
    print_info "Bygger test-container..."
    
    cd testning
    docker build $no_cache -t nexus-test:latest .
    cd ..
    
    print_success "Test-container byggd!"
}

# Start test container if not running
start_test_container() {
    local container_name="nexus-test-runner"
    
    # Check if container is already running
    if docker ps --filter "name=$container_name" --filter "status=running" | grep -q $container_name; then
        print_info "Test-container körs redan"
        return 0
    fi
    
    # Check if test image exists
    if ! docker image inspect nexus-test:latest >/dev/null 2>&1; then
        print_info "Test-container finns inte, bygger den..."
        build_test_container
    fi
    
    # Set default test environment variables
    local test_host="${TEST_HOST:-localhost}"
    local test_port="${TEST_PORT:-8000}"
    local kong_admin_port="${KONG_ADMIN_PORT:-8001}"
    local nexus_direct_port="${NEXUS_DIRECT_PORT:-8081}"
    
    # Start container in background
    print_info "Startar test-container i bakgrunden..."
    docker run -d \
        --name $container_name \
        --network host \
        -v "$(pwd)/testning:/app" \
        -v "$HOME/.kube:/root/.kube" \
        -e KUBECONFIG=/root/.kube/config \
        -e TEST_HOST="$test_host" \
        -e TEST_PORT="$test_port" \
        -e KONG_ADMIN_PORT="$kong_admin_port" \
        -e NEXUS_DIRECT_PORT="$nexus_direct_port" \
        nexus-test:latest \
        sleep infinity
    
    print_success "Test-container startad som '$container_name'"
    print_info "Konfiguration:"
    print_info "  TEST_HOST=$test_host"
    print_info "  TEST_PORT=$test_port"
    print_info "  KONG_ADMIN_PORT=$kong_admin_port"
    print_info "  NEXUS_DIRECT_PORT=$nexus_direct_port"
}

# Execute pytest command in container
exec_pytest() {
    local container_name="nexus-test-runner"
    local pytest_cmd="$*"
    
    # Start test container if needed
    start_test_container
    
    print_info "Exekverar: python3 -m pytest $pytest_cmd"
    
    docker exec $container_name \
        python3 -m pytest $pytest_cmd
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        print_success "Tester slutförda framgångsrikt!"
    else
        print_error "Tester misslyckades (exit code: $exit_code)"
    fi
    
    return $exit_code
}

# Run all tests
run_all_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail --html=report.html --self-contained-html
}

# Run health checks
run_health_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m health --html=report.html --self-contained-html
}

# Run API tests (without GUI)
run_api_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m api --html=report.html --self-contained-html
}

# Run GUI tests only
run_gui_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m gui --html=report.html --self-contained-html
}

# Run smart endpoint URL tests
run_endpoint_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail test/test_endpoint_urls.py --html=report.html --self-contained-html
}

# Run basic API tests
run_basic_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m basic --html=report.html --self-contained-html
}

# Run error handling tests
run_errors_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m errors --html=report.html --self-contained-html
}

# Run data validation tests
run_validation_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m validation --html=report.html --self-contained-html
}

# Run workflow tests
run_workflows_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m workflows --html=report.html --self-contained-html
}

# Run scheduler tests
run_scheduler_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m scheduler --html=report.html --self-contained-html
}

# Run K8s tests
run_k8s_tests() {
    local stop_on_fail="-x"
    
    # Check for --to-the-end argument
    for arg in "$@"; do
        if [[ "$arg" == "--to-the-end" ]]; then
            stop_on_fail=""
            break
        fi
    done
    
    exec_pytest -v $stop_on_fail -m k8s --html=report.html --self-contained-html
}

# Run custom pytest command
run_custom_tests() {
    shift  # Ta bort 'run' från argumenten
    exec_pytest -v --html=report.html --self-contained-html "$@"
}

# Stop test container
stop_test_container() {
    local container_name="nexus-test-runner"
    
    if docker ps --filter "name=$container_name" | grep -q $container_name; then
        print_info "Stoppar test-container '$container_name'..."
        docker stop $container_name
        docker rm $container_name
        print_success "Test-container stoppad!"
    else
        print_info "Test-container körs inte"
    fi
}

# Restart test container (preserves code changes via volume mount)
restart_test_container() {
    local container_name="nexus-test-runner"
    
    print_info "Startar om test-container (behåller kod-ändringar via volume mount)..."
    
    # Stop existing container if running
    if docker ps --filter "name=$container_name" | grep -q $container_name; then
        print_info "Stoppar befintlig test-container..."
        docker stop $container_name
        docker rm $container_name
    fi
    
    # Start new container
    start_test_container
    
    print_success "Test-container omstartad! Kod-ändringar är automatiskt tillgängliga."
}

# Clean up
clean_test_artifacts() {
    print_info "Rensar test-artifakter..."
    
    # Stop running test container
    stop_test_container
    
    # Remove any remaining test containers
    docker ps -a --filter "ancestor=nexus-test:latest" -q | xargs -r docker rm -f
    
    # Remove test images
    docker images nexus-test -q | xargs -r docker rmi -f
    
    # Clean up test reports
    rm -f testning/report.html
    rm -rf testning/.pytest_cache
    rm -rf testning/__pycache__
    rm -rf testning/test/__pycache__
    rm -rf testning/support/__pycache__
    
    print_success "Rensning slutförd!"
}

# Show test logs
show_logs() {
    print_info "Visar test-logs..."
    
    if docker ps -a --filter "ancestor=nexus-test:latest" --format "table {{.Names}}" | grep -q nexus-test; then
        docker logs $(docker ps -a --filter "ancestor=nexus-test:latest" --format "{{.Names}}" | head -1)
    else
        print_warning "Inga test-containers hittades."
    fi
}

# Debug test environment
debug_test_environment() {
    print_info "Debuggar test-miljön..."
    
    # Check if test container is running
    if ! docker ps --filter "name=test-container" --format "{{.Names}}" | grep -q test-container; then
        print_error "Test-container körs inte. Starta den först med: $0 build"
        return 1
    fi
    
    print_info "Kontrollerar miljövariabler och URL:er i test-container..."
    docker exec test-container python3 -c "
import os
print('=== MILJÖVARIABLER ===')
print('Docker env:', os.path.exists('/.dockerenv'))
print('TEST_HOST:', os.getenv('TEST_HOST', 'localhost'))
print('TEST_PORT:', os.getenv('TEST_PORT', '8000'))

print('\n=== BERÄKNAT API_BASE_URL ===')
host = os.getenv('TEST_HOST', 'localhost')
port = os.getenv('TEST_PORT', '8000')
if os.path.exists('/.dockerenv'):
    host = 'host.docker.internal'
api_base_url = f'http://{host}:{port}/api'
print('api_base_url:', api_base_url)

print('\n=== TESTAR ANSLUTNING ===')
import requests
try:
    response = requests.get(f'{api_base_url}/health', timeout=5)
    print(f'Health check: {response.status_code} - {response.text[:100]}')
except Exception as e:
    print(f'Health check failed: {e}')

try:
    response = requests.get(f'{api_base_url}/schedule/', timeout=5)
    print(f'Schedule endpoint: {response.status_code} - {response.text[:100]}')
except Exception as e:
    print(f'Schedule endpoint failed: {e}')
"
}

# Main script logic
main() {
    case "${1:-help}" in
        "run")
            check_docker
            check_kind_cluster
            run_custom_tests "$@"
            ;;
        "run-all")
            check_docker
            check_kind_cluster
            shift
            run_all_tests "$@"
            ;;
        "run-health")
            check_docker
            check_kind_cluster
            shift
            run_health_tests "$@"
            ;;
        "run-api")
            check_docker
            check_kind_cluster
            shift
            run_api_tests "$@"
            ;;
        "run-gui")
            check_docker
            check_kind_cluster
            shift
            run_gui_tests "$@"
            ;;
        "run-endpoints")
            check_docker
            check_kind_cluster
            shift
            run_endpoint_tests "$@"
            ;;
        "run-basic")
            check_docker
            check_kind_cluster
            shift
            run_basic_tests "$@"
            ;;
        "run-errors")
            check_docker
            check_kind_cluster
            shift
            run_errors_tests "$@"
            ;;
        "run-validation")
            check_docker
            check_kind_cluster
            shift
            run_validation_tests "$@"
            ;;
        "run-workflows")
            check_docker
            check_kind_cluster
            shift
            run_workflows_tests "$@"
            ;;
        "run-scheduler")
            check_docker
            check_kind_cluster
            shift
            run_scheduler_tests "$@"
            ;;
        "debug-env")
            check_docker
            check_kind_cluster
            debug_test_environment
            ;;
        "run-k8s")
            check_docker
            check_kind_cluster
            shift
            run_k8s_tests "$@"
            ;;
        "stop")
            stop_test_container
            ;;
        "build")
            check_docker
            shift
            build_test_container "$@"
            ;;
        "rebuild")
            check_docker
            shift
            stop_test_container
            build_test_container "$@"
            ;;
        "restart")
            check_docker
            restart_test_container
            ;;
        "clean")
            check_docker
            clean_test_artifacts
            ;;
        "logs")
            check_docker
            show_logs
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function
main "$@"
