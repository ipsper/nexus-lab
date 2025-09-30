#!/bin/bash

# Nexus Repository Frontend Start Script
# Startar React utvecklingsserver med korrekt konfiguration

set -e

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktioner för output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Kontrollera att vi är i rätt mapp
if [ ! -f "frontend/package.json" ]; then
    print_error "package.json hittades inte i frontend-mappen"
    print_info "Kör detta script från projektets root-mapp"
    exit 1
fi

# Gå till frontend-mappen
cd frontend

print_info "Startar Nexus Repository Frontend..."

# Kontrollera Node.js version
if ! command -v node &> /dev/null; then
    print_error "Node.js är inte installerat"
    print_info "Installera Node.js 18+ från https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_warning "Node.js version $NODE_VERSION hittades, men version 18+ rekommenderas"
fi

# Kontrollera om node_modules finns
if [ ! -d "node_modules" ]; then
    print_info "Installerar dependencies..."
    npm install
    print_success "Dependencies installerade"
fi

# Skapa .env.local om den inte finns
if [ ! -f ".env.local" ]; then
    print_info "Skapar .env.local konfigurationsfil..."
    cat > .env.local << EOF
VITE_API_URL=http://localhost:8000/api
EOF
    print_success ".env.local skapad"
fi

# Kontrollera att backend körs
print_info "Kontrollerar backend-anslutning..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    print_success "Backend API är tillgängligt"
else
    print_warning "Backend API svarar inte på http://localhost:8000/api/health"
    print_info "Starta backend först med: ./scripts/run.sh create"
fi

print_info "Startar React utvecklingsserver..."
print_info "Frontend kommer att vara tillgänglig på: http://localhost:3000"
print_info "Tryck Ctrl+C för att stoppa servern"

# Starta utvecklingsserver
npm run dev
