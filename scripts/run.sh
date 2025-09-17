#!/bin/bash

# Nexus Repository Manager - Kind Installation Script
# Detta skript automatiserar installationen och hanteringen av Nexus Repository Manager i Kind

set -e  # Avsluta vid fel

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
    echo "Nexus Repository Manager - Kind Installation Script"
    echo ""
    echo "Användning: $0 [KOMMANDO]"
    echo ""
    echo "Kommandon:"
    echo "  create           Skapa allt (kluster + applikationer) - KOMPLETT SETUP"
    echo "  delete           Ta bort allt och rensa systemet - REN START"
    echo "  delete-saveimages Ta bort allt men spara images (utom FastAPI) - SNABB START"
    echo "  install-kind     Installera Kind"
    echo "  create-cluster   Skapa Kind-kluster"
    echo "  deploy-nexus     Deploya Nexus till klustret"
    echo "  start-nexus      Starta Nexus (alias för deploy-nexus)"
    echo "  stop-nexus       Stoppa Nexus"
    echo "  restart-nexus    Starta om Nexus"
    echo "  build-api        Bygg API-applikation Docker image"
    echo "  deploy-api       Deploya API-applikation till klustret"
    echo "  start-api        Starta API-applikation (alias för deploy-api)"
    echo "  stop-api         Stoppa API-applikation"
    echo "  get-logs         Visa Nexus-loggar"
    echo "  get-password     Hämta admin-lösenord"
    echo "  check-status     Kontrollera status"
    echo "  kong-info        Visa Kong Gateway information"
    echo "  backup           Backup av Nexus-data"
    echo "  restore          Återställ från backup"
    echo "  update-nexus     Uppdatera Nexus-image"
    echo "  cleanup          Rensa gamla artefakter"
    echo "  delete-cluster   Ta bort Kind-kluster"
    echo "  delete-nexus     Ta bort bara Nexus (behåll kluster)"
    echo "  help             Visa denna hjälp"
    echo ""
    echo "Exempel:"
    echo "  $0 install-kind"
    echo "  $0 create-cluster"
    echo "  $0 deploy-nexus"
    echo "  $0 get-logs"
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
        print_error "Kind är inte installerat. Kör 'install-kind' först."
        exit 1
    fi
}

# Installera Kind
install_kind() {
    print_info "Installerar Kind..."
    
    # Kontrollera operativsystem
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            print_info "Använder Homebrew för installation..."
            brew install kind
        else
            print_info "Laddar ner Kind från GitHub..."
            curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-darwin-amd64
            chmod +x ./kind
            sudo mv ./kind /usr/local/bin/kind
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        print_info "Laddar ner Kind från GitHub..."
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
        chmod +x ./kind
        sudo mv ./kind /usr/local/bin/kind
    else
        print_error "Operativsystemet stöds inte. Installera Kind manuellt."
        exit 1
    fi
    
    print_success "Kind installerad!"
}

# Skapa Kind-kluster
create_cluster() {
    check_kind
    print_info "Skapar Kind-kluster..."
    
    # Kontrollera om klustret redan finns
    if kind get clusters | grep -q nexus-cluster; then
        print_warning "Klustret 'nexus-cluster' finns redan. Ta bort det först om du vill skapa ett nytt."
        return 0
    fi
    
    # Skapa klustret
    kind create cluster --name nexus-cluster --config k8s/kind-config.yaml
    
    print_success "Kind-kluster skapat!"
    print_info "Klustret är tillgängligt på localhost:8081"
}

# Deploya Nexus
deploy_nexus() {
    check_kubectl
    print_info "Deployar Nexus till Kind-klustret..."
    
    # Kontrollera om klustret finns
    if ! kind get clusters | grep -q nexus-cluster; then
        print_error "Kind-klustret 'nexus-cluster' finns inte. Skapa det först med 'create-cluster'."
        exit 1
    fi
    
    # Deploya grundläggande komponenter
    print_info "Deployar grundläggande komponenter..."
    kubectl apply -f k8s/storage-class.yaml
    kubectl apply -f k8s/metrics-server.yaml
    kubectl apply -f k8s/kong-gateway.yaml
    
    # Vänta på att Kong startar
    print_info "Väntar på att Kong API Gateway startar..."
    # Vänta lite för att podden ska skapas
    sleep 10
    
    # Kontrollera om podden finns innan vi väntar
    if kubectl get pods -n kong -l app=kong --no-headers 2>/dev/null | grep -q .; then
        kubectl wait --for=condition=ready pod -l app=kong -n kong --timeout=120s
    else
        print_warning "Kong pod hittades inte, kontrollerar status..."
        kubectl get pods -n kong
        print_info "Fortsätter utan att vänta på Kong..."
    fi
    
    # Deploya Nexus
    print_info "Deployar Nexus Repository Manager..."
    kubectl apply -f k8s/nexus-deployment.yaml
    kubectl apply -f k8s/nexus-config.yaml
    kubectl apply -f k8s/nexus-ingress.yaml
    
    print_info "Väntar på att Nexus startar..."
    # Vänta lite för att podden ska skapas
    sleep 10
    
    # Kontrollera om podden finns innan vi väntar
    if kubectl get pods -n nexus -l app=nexus --no-headers 2>/dev/null | grep -q .; then
        kubectl wait --for=condition=ready pod -l app=nexus -n nexus --timeout=300s
    else
        print_warning "Nexus pod hittades inte, kontrollerar status..."
        kubectl get pods -n nexus
        print_info "Fortsätter utan att vänta på pod-ready..."
    fi
    
    print_success "Nexus deployad!"
    print_info "Nexus är tillgänglig på http://localhost:8081"
}

# Stoppa Nexus
stop_nexus() {
    check_kubectl
    print_info "Stoppar Nexus..."
    
    kubectl scale deployment nexus --replicas=0 -n nexus
    
    print_success "Nexus stoppad!"
}

# Starta om Nexus
restart_nexus() {
    check_kubectl
    print_info "Startar om Nexus..."
    
    kubectl rollout restart deployment/nexus -n nexus
    
    # Vänta lite för att podden ska skapas
    sleep 10
    
    # Kontrollera om podden finns innan vi väntar
    if kubectl get pods -n nexus -l app=nexus --no-headers 2>/dev/null | grep -q .; then
        kubectl wait --for=condition=ready pod -l app=nexus -n nexus --timeout=300s
    else
        print_warning "Nexus pod hittades inte efter omstart, kontrollerar status..."
        kubectl get pods -n nexus
    fi
    
    print_success "Nexus omstartad!"
}

# Visa loggar
get_logs() {
    check_kubectl
    print_info "Visar Nexus-loggar (tryck Ctrl+C för att avsluta)..."
    
    kubectl logs -f deployment/nexus -n nexus
}

# Hämta admin-lösenord
get_password() {
    check_kubectl
    print_info "Hämtar admin-lösenord..."
    
    # Vänta på att podden är redo
    kubectl wait --for=condition=ready pod -l app=nexus -n nexus --timeout=60s
    
    # Hämta lösenordet
    PASSWORD=$(kubectl exec -n nexus deployment/nexus -- cat /nexus-data/admin.password 2>/dev/null || echo "Lösenordet kunde inte hämtas")
    
    if [[ "$PASSWORD" != "Lösenordet kunde inte hämtas" ]]; then
        print_success "Admin-lösenord: $PASSWORD"
        print_info "Användarnamn: admin"
        print_info "Logga in på http://localhost:8081"
    else
        print_error "Kunde inte hämta admin-lösenord. Kontrollera att Nexus är igång."
    fi
}

# Kontrollera status
check_status() {
    check_kubectl
    print_info "Kontrollerar status..."
    
    echo ""
    print_info "Kind-kluster:"
    kind get clusters
    
    echo ""
    print_info "Nexus pods:"
    kubectl get pods -n nexus
    
    echo ""
    print_info "Nexus services:"
    kubectl get svc -n nexus
    
    echo ""
    print_info "API pods:"
    kubectl get pods -n nexus-api 2>/dev/null || print_warning "API namespace finns inte"
    
    echo ""
    print_info "API services:"
    kubectl get svc -n nexus-api 2>/dev/null || print_warning "API namespace finns inte"
    
    echo ""
    print_info "Kong pods:"
    kubectl get pods -n kong 2>/dev/null || print_warning "Kong namespace finns inte"
    
    echo ""
    print_info "Kong services:"
    kubectl get svc -n kong 2>/dev/null || print_warning "Kong namespace finns inte"
    
    echo ""
    print_info "Resursanvändning:"
    kubectl top pods -n nexus 2>/dev/null || print_warning "Metrics server inte tillgänglig"
    kubectl top pods -n nexus-api 2>/dev/null || print_warning "API metrics inte tillgängliga"
    kubectl top pods -n kong 2>/dev/null || print_warning "Kong metrics inte tillgängliga"
}

# Visa Kong Gateway information
show_kong_info() {
    check_kubectl
    print_info "Kong Gateway Information:"
    echo ""
    print_info "🌐 Tjänster tillgängliga via Kong Gateway (utan port-forwarding):"
    print_info "  • Nexus Repository Manager: http://localhost:8000/nexus"
    print_info "  • FastAPI Applikation: http://localhost:8000/api"
    print_info "  • API Dokumentation: http://localhost:8000/api/docs"
    print_info "  • Kong Admin API: http://localhost:8001"
    print_info "  • Kong Admin GUI: http://localhost:8002"
    echo ""
    print_info "🔧 Kong Gateway fungerar via Kind NodePort-mappningar"
    print_info "✅ Ingen port-forwarding behövs - allt fungerar direkt!"
    print_info "Alla tjänster är tillgängliga via Kong på port 8000"
    echo ""
    print_info "📋 Testa anslutningarna:"
    print_info "  curl http://localhost:8000/api/health"
    print_info "  curl http://localhost:8000/api/docs"
    print_info "  curl http://localhost:8000/nexus"
    print_info "  curl http://localhost:8001/status"
    echo ""
    print_info "🎯 Kong Gateway Status:"
    kubectl get pods -n kong
    kubectl get svc -n kong
}

# Backup
backup() {
    check_kubectl
    print_info "Skapar backup av Nexus-data..."
    
    BACKUP_FILE="nexus-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    # Skapa backup
    kubectl exec -n nexus deployment/nexus -- tar czf /tmp/nexus-backup.tar.gz -C /nexus-data .
    kubectl cp nexus/$(kubectl get pods -n nexus -l app=nexus -o jsonpath='{.items[0].metadata.name}'):/tmp/nexus-backup.tar.gz ./$BACKUP_FILE
    
    print_success "Backup skapad: $BACKUP_FILE"
}

# Återställ
restore() {
    check_kubectl
    
    if [ -z "$1" ]; then
        print_error "Ange backup-fil som argument"
        print_info "Användning: $0 restore <backup-fil>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup-filen '$BACKUP_FILE' finns inte"
        exit 1
    fi
    
    print_info "Återställer från backup: $BACKUP_FILE"
    
    # Kopiera backup till podden
    kubectl cp "$BACKUP_FILE" nexus/$(kubectl get pods -n nexus -l app=nexus -o jsonpath='{.items[0].metadata.name}'):/tmp/nexus-backup.tar.gz
    
    # Återställ data
    kubectl exec -n nexus deployment/nexus -- tar xzf /tmp/nexus-backup.tar.gz -C /nexus-data
    
    print_success "Återställning klar!"
}

# Uppdatera Nexus
update_nexus() {
    check_kubectl
    print_info "Uppdaterar Nexus-image..."
    
    # Uppdatera image
    kubectl set image deployment/nexus nexus=sonatype/nexus3:latest -n nexus
    
    # Vänta på rollout
    kubectl rollout status deployment/nexus -n nexus
    
    print_success "Nexus uppdaterad!"
}

# Rensa gamla artefakter
cleanup() {
    check_kubectl
    print_info "Rensar gamla artefakter..."
    
    # Detta skulle normalt göras via Nexus UI, men vi kan visa instruktioner
    print_info "För att rensa gamla artefakter:"
    print_info "1. Gå till http://localhost:8081"
    print_info "2. Logga in som admin"
    print_info "3. Gå till Settings → Repositories"
    print_info "4. Välj repository → Cleanup policies"
    print_info "5. Konfigurera regler för borttagning av gamla artefakter"
}

# Ta bort Kind-kluster
delete_cluster() {
    check_kind
    print_info "Tar bort Kind-kluster..."
    kind delete cluster --name nexus-cluster
    
    print_success "Kind-kluster borttaget!"
}

# Ta bort bara Nexus
delete_nexus() {
    check_kubectl
    print_info "Tar bort Nexus..."
    kubectl delete namespace nexus
    
    print_success "Nexus borttaget!"
}

# Bygg API Docker image
build_api() {
    print_info "Bygger API Docker image..."
    
    if [ ! -d "app" ]; then
        print_error "App-mappen finns inte. Kör från projektets root-katalog."
        exit 1
    fi
    
    cd app
    docker build -t nexus-api:latest .
    cd ..
    
    print_success "API Docker image byggd!"
}

# Deploya API
deploy_api() {
    check_kubectl
    print_info "Deployar API-applikation till Kind-klustret..."
    
    # Kontrollera om klustret finns
    if ! kind get clusters | grep -q nexus-cluster; then
        print_error "Kind-klustret 'nexus-cluster' finns inte. Skapa det först med 'create-cluster'."
        exit 1
    fi
    
    # Kontrollera om API image finns
    if ! docker images | grep -q nexus-api; then
        print_warning "API Docker image finns inte. Bygger den först..."
        build_api
    fi
    
    # Ladda image till Kind-klustret
    kind load docker-image nexus-api:latest --name nexus-cluster
    
    # Deploya API
    print_info "Deployar FastAPI-applikation..."
    kubectl apply -f k8s/nexus-api-deployment.yaml
    
    print_info "Väntar på att API startar..."
    # Vänta lite för att podden ska skapas
    sleep 10
    
    # Kontrollera om podden finns innan vi väntar
    if kubectl get pods -n nexus-api -l app=nexus-api --no-headers 2>/dev/null | grep -q .; then
        kubectl wait --for=condition=ready pod -l app=nexus-api -n nexus-api --timeout=300s
    else
        print_warning "API pod hittades inte, kontrollerar status..."
        kubectl get pods -n nexus-api
        print_info "Fortsätter utan att vänta på pod-ready..."
    fi
    
    print_success "API deployad!"
    print_info "API är tillgänglig via Kong Gateway på http://localhost:8000/api"
    print_info "API-dokumentation: http://localhost:8000/api/docs"
}

# Stoppa API
stop_api() {
    check_kubectl
    print_info "Stoppar API-applikation..."
    
    kubectl scale deployment nexus-api --replicas=0 -n nexus-api
    
    print_success "API stoppad!"
}

# Starta om API
restart_api() {
    check_kubectl
    print_info "Startar om API-applikation..."
    
    kubectl rollout restart deployment/nexus-api -n nexus-api
    
    # Vänta lite för att podden ska skapas
    sleep 10
    
    # Kontrollera om podden finns innan vi väntar
    if kubectl get pods -n nexus-api -l app=nexus-api --no-headers 2>/dev/null | grep -q .; then
        kubectl wait --for=condition=ready pod -l app=nexus-api -n nexus-api --timeout=300s
    else
        print_warning "API pod hittades inte efter omstart, kontrollerar status..."
        kubectl get pods -n nexus-api
    fi
    
    print_success "API omstartad!"
}

# Komplett setup - skapa allt
create_all() {
    print_info "🚀 Startar komplett setup av Nexus Repository Manager + API..."
    print_info "Detta kommer att:"
    print_info "  1. Installera Kind (om inte redan installerat)"
    print_info "  2. Skapa Kind-kluster"
    print_info "  3. Deploya Nexus Repository Manager"
    print_info "  4. Bygga API Docker image"
    print_info "  5. Deploya API-applikation"
    print_info "  6. Visa admin-lösenord och status"
    echo ""
    
    # Steg 1: Installera Kind
    if ! command -v kind &> /dev/null; then
        print_info "Steg 1/6: Installerar Kind..."
        install_kind
    else
        print_success "Steg 1/6: Kind redan installerat ✓"
    fi
    
    # Steg 2: Skapa kluster
    print_info "Steg 2/6: Skapar Kind-kluster..."
    create_cluster
    
    # Steg 3: Deploya Nexus
    print_info "Steg 3/6: Deployar Nexus Repository Manager..."
    deploy_nexus
    
    # Steg 4: Bygga API
    print_info "Steg 4/6: Bygger API Docker image..."
    build_api
    
    # Steg 5: Deploya API
    print_info "Steg 5/6: Deployar API-applikation..."
    deploy_api
    
    # Steg 6: Visa status och lösenord
    print_info "Steg 6/6: Visar status och admin-lösenord..."
    echo ""
    print_success "🎉 Komplett setup klar!"
    echo ""
    print_info "📋 Tjänster tillgängliga via Kong Gateway:"
    print_info "  • Nexus Repository Manager: http://localhost:8000/nexus"
    print_info "  • FastAPI Applikation: http://localhost:8000/api"
    print_info "  • API Dokumentation: http://localhost:8000/api/docs"
    print_info "  • Kong Admin API: http://localhost:8001"
    print_info "  • Kong Admin GUI: http://localhost:8002"
    echo ""
    
    # Visa admin-lösenord
    get_password
    
    echo ""
    print_info "🔧 Användbara kommandon:"
    print_info "  • Kontrollera status: ./scripts/run.sh check-status"
    print_info "  • Visa loggar: ./scripts/run.sh get-logs"
    print_info "  • Ta bort allt: ./scripts/run.sh delete"
    echo ""
}

# Ta bort allt och rensa systemet
delete_all() {
    print_info "🗑️  Rensar systemet HELT:"
    print_info "  • Stoppar alla applikationer"
    print_info "  • Tar bort alla namespaces"
    print_info "  • Tar bort Kind-klustret"
    print_info "  • Rensar ALLA Docker images"
    print_info "  • Systemet blir helt rent för nästa start"
    echo ""
    
    print_info "🧹 Startar komplett rensning av systemet..."
    
    # Steg 1: Stoppa alla applikationer
    print_info "Steg 1/6: Stoppar alla applikationer..."
    if kubectl get namespace nexus-api &> /dev/null; then
        kubectl scale deployment nexus-api --replicas=0 -n nexus-api 2>/dev/null || true
    fi
    if kubectl get namespace nexus &> /dev/null; then
        kubectl scale deployment nexus --replicas=0 -n nexus 2>/dev/null || true
    fi
    if kubectl get namespace kong &> /dev/null; then
        kubectl scale deployment kong --replicas=0 -n kong 2>/dev/null || true
    fi
    
    # Steg 2: Ta bort alla namespaces
    print_info "Steg 2/6: Tar bort alla namespaces..."
    kubectl delete namespace nexus-api --ignore-not-found=true
    kubectl delete namespace nexus --ignore-not-found=true
    kubectl delete namespace kong --ignore-not-found=true
    kubectl delete namespace local-path-storage --ignore-not-found=true
    
    # Steg 3: Ta bort Kind-kluster
    print_info "Steg 3/6: Tar bort Kind-kluster..."
    if kind get clusters | grep -q nexus-cluster; then
        kind delete cluster --name nexus-cluster
    else
        print_info "Kind-kluster finns inte"
    fi
    
    # Steg 4: Rensa ALLA Docker images
    print_info "Steg 4/6: Rensar ALLA Docker images..."
    if docker images | grep -q nexus-api; then
        docker rmi nexus-api:latest 2>/dev/null || true
    fi
    if docker images | grep -q sonatype/nexus3; then
        docker rmi sonatype/nexus3:latest 2>/dev/null || true
    fi
    # Rensa alla oanvända images
    docker image prune -a -f 2>/dev/null || true
    
    # Steg 5: Rensa Docker system
    print_info "Steg 5/6: Rensar Docker system..."
    docker system prune -a -f 2>/dev/null || true
    
    # Steg 6: Rensa Docker volumes
    print_info "Steg 6/6: Rensar Docker volumes..."
    docker volume prune -f 2>/dev/null || true
    
    print_success "✨ Systemet är nu HELT rent!"
    print_info "Du kan nu köra './scripts/run.sh create' för en ren start"
    echo ""
}

# Ta bort allt men spara images (utom FastAPI)
delete_save_images() {
    print_info "🗑️  Rensar systemet men sparar images:"
    print_info "  • Stoppar alla applikationer"
    print_info "  • Tar bort alla namespaces"
    print_info "  • Tar bort Kind-klustret"
    print_info "  • Sparar Nexus och system images"
    print_info "  • Tar bort FastAPI image (alltid nybyggd)"
    print_info "  • Snabbare nästa start"
    echo ""
    
    print_info "🧹 Startar snabb rensning av systemet..."
    
    # Steg 1: Stoppa alla applikationer
    print_info "Steg 1/5: Stoppar alla applikationer..."
    if kubectl get namespace nexus-api &> /dev/null; then
        kubectl scale deployment nexus-api --replicas=0 -n nexus-api 2>/dev/null || true
    fi
    if kubectl get namespace nexus &> /dev/null; then
        kubectl scale deployment nexus --replicas=0 -n nexus 2>/dev/null || true
    fi
    if kubectl get namespace kong &> /dev/null; then
        kubectl scale deployment kong --replicas=0 -n kong 2>/dev/null || true
    fi
    
    # Steg 2: Ta bort alla namespaces
    print_info "Steg 2/5: Tar bort alla namespaces..."
    kubectl delete namespace nexus-api --ignore-not-found=true
    kubectl delete namespace nexus --ignore-not-found=true
    kubectl delete namespace kong --ignore-not-found=true
    kubectl delete namespace local-path-storage --ignore-not-found=true
    
    # Steg 3: Ta bort Kind-kluster
    print_info "Steg 3/5: Tar bort Kind-kluster..."
    if kind get clusters | grep -q nexus-cluster; then
        kind delete cluster --name nexus-cluster
    else
        print_info "Kind-kluster finns inte"
    fi
    
    # Steg 4: Rensa bara FastAPI image
    print_info "Steg 4/5: Rensar bara FastAPI image..."
    if docker images | grep -q nexus-api; then
        docker rmi nexus-api:latest 2>/dev/null || true
        print_success "✅ FastAPI image borttagen"
    else
        print_info "FastAPI image fanns inte"
    fi
    
    # Steg 5: Rensa Docker system (men spara images)
    print_info "Steg 5/5: Rensar Docker system (sparar images)..."
    docker system prune -f 2>/dev/null || true
    
    print_success "✨ Systemet rensat med sparade images!"
    print_info "Sparade images:"
    docker images | grep -E "(sonatype|nginx|metrics|local-path)" || print_info "  Inga system images hittades"
    echo ""
    print_info "Du kan nu köra './scripts/run.sh create' för en snabb start"
    echo ""
}

# Huvudlogik
case "${1:-help}" in
    create)
        create_all
        ;;
    delete)
        delete_all
        ;;
    delete-saveimages)
        delete_save_images
        ;;
    install-kind)
        install_kind
        ;;
    create-cluster)
        create_cluster
        ;;
    deploy-nexus|start-nexus)
        deploy_nexus
        ;;
    stop-nexus)
        stop_nexus
        ;;
    restart-nexus)
        restart_nexus
        ;;
    build-api)
        build_api
        ;;
    deploy-api|start-api)
        deploy_api
        ;;
    stop-api)
        stop_api
        ;;
    restart-api)
        restart_api
        ;;
    get-logs)
        get_logs
        ;;
    get-password)
        get_password
        ;;
    check-status)
        check_status
        ;;
    kong-info)
        show_kong_info
        ;;
    backup)
        backup
        ;;
    restore)
        restore "$2"
        ;;
    update-nexus)
        update_nexus
        ;;
    cleanup)
        cleanup
        ;;
    delete-cluster)
        delete_cluster
        ;;
    delete-nexus)
        delete_nexus
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
