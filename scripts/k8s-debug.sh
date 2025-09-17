#!/bin/bash

# Kubernetes Debug Script för Nexus Repository Manager + API
# Detta skript hjälper dig att felsöka Kubernetes-problem steg för steg

set -e  # Avsluta vid fel

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_debug() {
    echo -e "${CYAN}[DEBUG]${NC} $1"
}

# Hjälpfunktion
show_help() {
    echo "Kubernetes Debug Script för Nexus Repository Manager + API"
    echo ""
    echo "Användning: $0 [KOMMANDO]"
    echo ""
    echo "Debug-kommandon:"
    echo "  cluster-status    Kontrollera Kind-kluster status"
    echo "  nexus-status      Kontrollera Nexus pods och services"
    echo "  api-status        Kontrollera API pods och services"
    echo "  nexus-logs        Visa Nexus loggar"
    echo "  api-logs          Visa API loggar"
    echo "  nexus-describe    Beskriv Nexus pod (detaljerad info)"
    echo "  api-describe      Beskriv API pod (detaljerad info)"
    echo "  events            Visa alla events (sorterade efter tid)"
    echo "  resources         Visa resursanvändning"
    echo "  ports             Kontrollera port-användning"
    echo "  images            Visa Docker images i Kind-klustret"
    echo "  network           Kontrollera nätverksanslutningar"
    echo "  health            Kontrollera health checks"
    echo "  full-debug        Kör alla debug-kommandon"
    echo "  fix-image-pull    Analysera och fixa ImagePullBackOff-problem"
    echo "  help              Visa denna hjälp"
    echo ""
    echo "Exempel:"
    echo "  $0 cluster-status"
    echo "  $0 api-logs"
    echo "  $0 full-debug"
}

# Kontrollera om kubectl är installerat
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl är inte installerat. Installera det först."
        exit 1
    fi
}

# Kontrollera om Kind är installerat
check_kind() {
    if ! command -v kind &> /dev/null; then
        print_error "Kind är inte installerat. Installera det först."
        exit 1
    fi
}

# Kontrollera Kind-kluster status
cluster_status() {
    print_debug "=== KIND-KLUSTER STATUS ==="
    
    if ! kind get clusters | grep -q nexus-cluster; then
        print_error "Kind-klustret 'nexus-cluster' finns inte!"
        print_info "Kör: ./scripts/run.sh create-cluster"
        return 1
    fi
    
    print_success "Kind-kluster 'nexus-cluster' finns"
    
    echo ""
    print_info "Kind-kluster:"
    kind get clusters
    
    echo ""
    print_info "Kind-noder:"
    kubectl get nodes -o wide
    
    echo ""
    print_info "Namespaces:"
    kubectl get namespaces
}

# Kontrollera Nexus status
nexus_status() {
    print_debug "=== NEXUS STATUS ==="
    
    if ! kubectl get namespace nexus &> /dev/null; then
        print_error "Nexus namespace finns inte!"
        print_info "Kör: ./scripts/run.sh deploy-nexus"
        return 1
    fi
    
    echo ""
    print_info "Nexus pods:"
    kubectl get pods -n nexus -o wide
    
    echo ""
    print_info "Nexus services:"
    kubectl get svc -n nexus
    
    echo ""
    print_info "Nexus deployments:"
    kubectl get deployments -n nexus
    
    echo ""
    print_info "Nexus persistent volumes:"
    kubectl get pvc -n nexus
}

# Kontrollera API status
api_status() {
    print_debug "=== API STATUS ==="
    
    if ! kubectl get namespace nexus-api &> /dev/null; then
        print_error "API namespace finns inte!"
        print_info "Kör: ./scripts/run.sh deploy-api"
        return 1
    fi
    
    echo ""
    print_info "API pods:"
    kubectl get pods -n nexus-api -o wide
    
    echo ""
    print_info "API services:"
    kubectl get svc -n nexus-api
    
    echo ""
    print_info "API deployments:"
    kubectl get deployments -n nexus-api
    
    echo ""
    print_info "API ingress:"
    kubectl get ingress -n nexus-api
}

# Visa Nexus loggar
nexus_logs() {
    print_debug "=== NEXUS LOGGAR ==="
    
    if ! kubectl get namespace nexus &> /dev/null; then
        print_error "Nexus namespace finns inte!"
        return 1
    fi
    
    print_info "Nexus pod loggar (senaste 50 raderna):"
    kubectl logs -n nexus -l app=nexus --tail=50
    
    echo ""
    print_info "Nexus deployment loggar:"
    kubectl logs -n nexus deployment/nexus --tail=50
}

# Visa API loggar
api_logs() {
    print_debug "=== API LOGGAR ==="
    
    if ! kubectl get namespace nexus-api &> /dev/null; then
        print_error "API namespace finns inte!"
        return 1
    fi
    
    print_info "API pod loggar (senaste 50 raderna):"
    kubectl logs -n nexus-api -l app=nexus-api --tail=50
    
    echo ""
    print_info "API deployment loggar:"
    kubectl logs -n nexus-api deployment/nexus-api --tail=50
}

# Beskriv Nexus pod
nexus_describe() {
    print_debug "=== NEXUS POD DETALJER ==="
    
    if ! kubectl get namespace nexus &> /dev/null; then
        print_error "Nexus namespace finns inte!"
        return 1
    fi
    
    print_info "Nexus pod beskrivning:"
    kubectl describe pod -n nexus -l app=nexus
    
    echo ""
    print_info "Nexus deployment beskrivning:"
    kubectl describe deployment -n nexus nexus
}

# Beskriv API pod
api_describe() {
    print_debug "=== API POD DETALJER ==="
    
    if ! kubectl get namespace nexus-api &> /dev/null; then
        print_error "API namespace finns inte!"
        return 1
    fi
    
    print_info "API pod beskrivning:"
    kubectl describe pod -n nexus-api -l app=nexus-api
    
    echo ""
    print_info "API deployment beskrivning:"
    kubectl describe deployment -n nexus-api nexus-api
}

# Visa events
events() {
    print_debug "=== KUBERNETES EVENTS ==="
    
    print_info "Alla events (sorterade efter tid):"
    kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
    
    echo ""
    print_info "Nexus events:"
    kubectl get events -n nexus --sort-by='.lastTimestamp' | tail -10
    
    echo ""
    print_info "API events:"
    kubectl get events -n nexus-api --sort-by='.lastTimestamp' | tail -10
}

# Visa resursanvändning
resources() {
    print_debug "=== RESURSANVÄNDNING ==="
    
    print_info "Nod resursanvändning:"
    kubectl top nodes 2>/dev/null || print_warning "Metrics server inte tillgänglig"
    
    echo ""
    print_info "Nexus resursanvändning:"
    kubectl top pods -n nexus 2>/dev/null || print_warning "Nexus metrics inte tillgängliga"
    
    echo ""
    print_info "API resursanvändning:"
    kubectl top pods -n nexus-api 2>/dev/null || print_warning "API metrics inte tillgängliga"
    
    echo ""
    print_info "Resursbegränsningar:"
    kubectl describe nodes | grep -A 5 "Allocated resources"
}

# Kontrollera port-användning
ports() {
    print_debug "=== PORT-ANVÄNDNING ==="
    
    print_info "Kontrollerar port 8081 (Nexus):"
    if lsof -i :8081 &> /dev/null; then
        lsof -i :8081
    else
        print_warning "Port 8081 är inte i användning"
    fi
    
    echo ""
    print_info "Kontrollerar port 3000 (API):"
    if lsof -i :3000 &> /dev/null; then
        lsof -i :3000
    else
        print_warning "Port 3000 är inte i användning"
    fi
    
    echo ""
    print_info "Kind port-mapping:"
    docker ps | grep kind
}

# Visa Docker images i Kind-klustret
images() {
    print_debug "=== DOCKER IMAGES I KIND-KLUSTRET ==="
    
    print_info "Images i Kind-klustret:"
    docker exec nexus-cluster-control-plane crictl images
    
    echo ""
    print_info "Lokala Docker images:"
    docker images | grep -E "(nexus|sonatype)"
}

# Kontrollera nätverksanslutningar
network() {
    print_debug "=== NÄTVERKSANSLUTNINGAR ==="
    
    print_info "Kontrollerar anslutning till Nexus:"
    if curl -s http://localhost:8081/health &> /dev/null; then
        print_success "Nexus svarar på http://localhost:8081"
    else
        print_warning "Nexus svarar inte på http://localhost:8081"
    fi
    
    echo ""
    print_info "Kontrollerar anslutning till API:"
    if curl -s http://localhost:3000/health &> /dev/null; then
        print_success "API svarar på http://localhost:3000"
    else
        print_warning "API svarar inte på http://localhost:3000"
    fi
    
    echo ""
    print_info "Kubernetes services:"
    kubectl get svc --all-namespaces
}

# Kontrollera health checks
health() {
    print_debug "=== HEALTH CHECKS ==="
    
    print_info "Nexus health check:"
    if kubectl get pods -n nexus -l app=nexus | grep -q Running; then
        print_success "Nexus pod körs"
    else
        print_error "Nexus pod körs inte"
    fi
    
    echo ""
    print_info "API health check:"
    if kubectl get pods -n nexus-api -l app=nexus-api | grep -q Running; then
        print_success "API pod körs"
    else
        print_error "API pod körs inte"
    fi
    
    echo ""
    print_info "Pod readiness:"
    kubectl get pods --all-namespaces -o wide | grep -E "(nexus|READY)"
}

# Kör alla debug-kommandon
full_debug() {
    print_info "🔍 Kör fullständig debug-analys..."
    echo ""
    
    cluster_status
    echo ""
    nexus_status
    echo ""
    api_status
    echo ""
    events
    echo ""
    resources
    echo ""
    ports
    echo ""
    images
    echo ""
    network
    echo ""
    health
    
    echo ""
    print_success "✅ Fullständig debug-analys klar!"
    print_info "Granska outputen ovan för att identifiera problem."
}

# Analysera och fixa ImagePullBackOff-problem
fix_image_pull_problem() {
    print_debug "=== IMAGE PULL BACKOFF ANALYS OCH FIX ==="
    
    # Steg 1: Analysera problemet
    print_info "Steg 1/6: Analyserar ImagePullBackOff-problem..."
    
    # Kontrollera API pod status
    API_POD_STATUS=$(kubectl get pods -n nexus-api -l app=nexus-api -o jsonpath='{.items[0].status.containerStatuses[0].state.waiting.reason}' 2>/dev/null || echo "Unknown")
    
    if [[ "$API_POD_STATUS" == "ImagePullBackOff" ]]; then
        print_error "✅ Problem identifierat: ImagePullBackOff"
        print_info "Detta betyder att Kubernetes inte kan hämta Docker-imagen"
    else
        print_warning "Pod-status: $API_POD_STATUS (inte ImagePullBackOff)"
    fi
    
    echo ""
    
    # Steg 2: Kontrollera om image finns lokalt
    print_info "Steg 2/6: Kontrollerar om image finns lokalt..."
    
    if docker images | grep -q "nexus-api.*latest"; then
        print_success "✅ Image 'nexus-api:latest' finns lokalt"
        LOCAL_IMAGE_SIZE=$(docker images --format "table {{.Size}}" nexus-api:latest | tail -1)
        print_info "Image-storlek: $LOCAL_IMAGE_SIZE"
    else
        print_error "❌ Image 'nexus-api:latest' finns INTE lokalt"
        print_info "Lösning: Bygg image först med './scripts/run.sh build-api'"
        return 1
    fi
    
    echo ""
    
    # Steg 3: Kontrollera om image finns i Kind-klustret
    print_info "Steg 3/6: Kontrollerar om image finns i Kind-klustret..."
    
    if docker exec nexus-cluster-control-plane crictl images | grep -q "nexus-api.*latest"; then
        print_success "✅ Image finns i Kind-klustret"
    else
        print_warning "⚠️  Image finns INTE i Kind-klustret"
        print_info "Lösning: Ladda image till Kind-klustret"
    fi
    
    echo ""
    
    # Steg 4: Kontrollera pod-detaljer
    print_info "Steg 4/6: Analyserar pod-detaljer..."
    
    print_info "Pod-beskrivning:"
    kubectl describe pod -n nexus-api -l app=nexus-api | grep -A 10 -B 5 "Events:"
    
    echo ""
    
    # Steg 5: Försök att fixa problemet
    print_info "Steg 5/6: Försöker fixa problemet..."
    
    # Ladda om image till Kind
    print_info "Laddar om image till Kind-klustret..."
    if kind load docker-image nexus-api:latest --name nexus-cluster; then
        print_success "✅ Image laddad till Kind-klustret"
    else
        print_error "❌ Kunde inte ladda image till Kind-klustret"
        return 1
    fi
    
    # Starta om deployment
    print_info "Startar om API deployment..."
    if kubectl rollout restart deployment/nexus-api -n nexus-api; then
        print_success "✅ Deployment omstartad"
    else
        print_error "❌ Kunde inte starta om deployment"
        return 1
    fi
    
    echo ""
    
    # Steg 6: Verifiera fix
    print_info "Steg 6/6: Verifierar att problemet är löst..."
    
    print_info "Väntar 30 sekunder för att pod ska starta..."
    sleep 30
    
    # Kontrollera ny status
    NEW_POD_STATUS=$(kubectl get pods -n nexus-api -l app=nexus-api -o jsonpath='{.items[0].status.containerStatuses[0].state.waiting.reason}' 2>/dev/null || echo "Unknown")
    
    if [[ "$NEW_POD_STATUS" == "ImagePullBackOff" ]]; then
        print_error "❌ Problem kvarstår: ImagePullBackOff"
        print_info "Försök manuellt:"
        print_info "1. kubectl delete pod -n nexus-api -l app=nexus-api"
        print_info "2. kubectl get pods -n nexus-api -w"
    elif [[ "$NEW_POD_STATUS" == "Running" ]]; then
        print_success "✅ Problem löst! Pod körs nu"
    else
        print_warning "⚠️  Pod-status: $NEW_POD_STATUS"
        print_info "Kontrollera pod-status: kubectl get pods -n nexus-api"
    fi
    
    echo ""
    print_info "📋 Sammanfattning av analys:"
    print_info "  • Ursprunglig status: $API_POD_STATUS"
    print_info "  • Ny status: $NEW_POD_STATUS"
    print_info "  • Image laddad: $(docker exec nexus-cluster-control-plane crictl images | grep -q "nexus-api.*latest" && echo "Ja" || echo "Nej")"
    print_info "  • Deployment omstartad: Ja"
    
    echo ""
    print_success "🔧 ImagePullBackOff-analys och fix klar!"
}

# Huvudlogik
case "${1:-help}" in
    cluster-status)
        cluster_status
        ;;
    nexus-status)
        nexus_status
        ;;
    api-status)
        api_status
        ;;
    nexus-logs)
        nexus_logs
        ;;
    api-logs)
        api_logs
        ;;
    nexus-describe)
        nexus_describe
        ;;
    api-describe)
        api_describe
        ;;
    events)
        events
        ;;
    resources)
        resources
        ;;
    ports)
        ports
        ;;
    images)
        images
        ;;
    network)
        network
        ;;
    health)
        health
        ;;
    full-debug)
        full_debug
        ;;
    fix-image-pull)
        fix_image_pull_problem
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
