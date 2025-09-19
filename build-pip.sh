#!/bin/bash

# Wrapper script för att köra pip build från root-katalogen
# Detta skript dirigerar om till build-pip/build-pip.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_SCRIPT="$SCRIPT_DIR/build-pip/build-pip.sh"

if [ ! -f "$BUILD_SCRIPT" ]; then
    echo "❌ Fel: build-pip/build-pip.sh hittades inte"
    echo "Kontrollera att build-pip mappen finns"
    exit 1
fi

# Kör build-skriptet med alla argument
exec "$BUILD_SCRIPT" "$@"