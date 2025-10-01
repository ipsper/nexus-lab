#!/bin/bash

# Färgkoder för output
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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Sätt rätt working directory
cd "$(dirname "$0")/.." || exit 1
REPO_ROOT=$(pwd)
BUILD_DIR="$REPO_ROOT/build-npm"

print_info "🚀 Nexus Repository Frontend - NPM Package Builder"
print_info "=================================================="

# Kontrollera att Node.js är installerat
if ! command -v node &> /dev/null; then
    print_error "Node.js är inte installerat. Installera Node.js först."
    exit 1
fi

NODE_VERSION=$(node --version)
print_info "Använder Node.js $NODE_VERSION"

# Gå till build-mappen
cd "$BUILD_DIR" || exit 1

# Installera dependencies
print_info "Installerar dependencies..."
npm install
if [ $? -ne 0 ]; then
    print_error "Fel vid installation av dependencies"
    exit 1
fi
print_success "Dependencies installerade"

# Bygg frontend
print_info "Bygger frontend..."
npm run build
if [ $? -ne 0 ]; then
    print_error "Fel vid byggande av frontend"
    exit 1
fi
print_success "Frontend byggd"

# Kontrollera att dist-mappen finns
if [ ! -d "dist" ]; then
    print_error "dist-mappen skapades inte"
    exit 1
fi

print_info "Paketinformation:"
ls -lh dist/

print_success "Frontend-paket byggt framgångsrikt!"
print_info ""
print_info "📦 Nästa steg:"
print_info "  • Bygg Docker image: ./scripts/run.sh deploy-frontend"
print_info "  • Eller deploy allt: ./scripts/run.sh deploy-all"

