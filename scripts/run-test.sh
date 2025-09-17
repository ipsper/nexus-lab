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
    echo "  run                 Kör alla tester"
    echo "  run-unit            Kör endast unit-tester"
    echo "  run-integration     Kör endast integration-tester"
    echo "  run-api             Kör endast API-tester"
    echo "  run-slow            Kör inklusive långsamma tester"
    echo "  build               Bygg test-container"
    echo "  clean               Rensa test-containers och images"
    echo "  logs                Visa test-logs"
    echo "  help                Visa denna hjälp"
    echo ""
    echo "Exempel:"
    echo "  $0 run              # Kör alla tester"
    echo "  $0 run-unit         # Kör endast unit-tester"
    echo "  $0 run-integration  # Kör integration-tester"
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
    print_info "Bygger test-container..."
    
    cd testning
    docker build -t nexus-test:latest .
    cd ..
    
    print_success "Test-container byggd!"
}

# Run tests
run_tests() {
    local test_type="$1"
    local pytest_args=""
    
    case "$test_type" in
        "unit")
            pytest_args="-m unit"
            print_info "Kör unit-tester..."
            ;;
        "integration")
            pytest_args="-m integration"
            print_info "Kör integration-tester..."
            ;;
        "api")
            pytest_args="-m api"
            print_info "Kör API-tester..."
            ;;
        "slow")
            pytest_args="-m slow"
            print_info "Kör långsamma tester..."
            ;;
        "all")
            pytest_args=""
            print_info "Kör alla tester..."
            ;;
    esac
    
    # Check if test container exists
    if ! docker image inspect nexus-test:latest >/dev/null 2>&1; then
        print_info "Test-container finns inte, bygger den..."
        build_test_container
    fi
    
    # Run tests in container
    print_info "Startar tester i container..."
    
    docker run --rm \
        --network host \
        -v "$(pwd)/testning:/app" \
        -v "$HOME/.kube:/root/.kube" \
        -e KUBECONFIG=/root/.kube/config \
        nexus-test:latest \
        pytest -v --tb=short --html=report.html --self-contained-html $pytest_args
    
    print_success "Tester slutförda!"
}

# Clean up
clean_test_artifacts() {
    print_info "Rensar test-artifakter..."
    
    # Remove test containers
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

# Main script logic
main() {
    case "${1:-help}" in
        "run")
            check_docker
            check_kind_cluster
            run_tests "all"
            ;;
        "run-unit")
            check_docker
            check_kind_cluster
            run_tests "unit"
            ;;
        "run-integration")
            check_docker
            check_kind_cluster
            run_tests "integration"
            ;;
        "run-api")
            check_docker
            check_kind_cluster
            run_tests "api"
            ;;
        "run-slow")
            check_docker
            check_kind_cluster
            run_tests "slow"
            ;;
        "build")
            check_docker
            build_test_container
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
