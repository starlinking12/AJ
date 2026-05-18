#!/bin/bash
set -e

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Backing up J.A.R.V.I.S. data..."
echo "================================"

if [ -d "data" ]; then
    cp -r data "$BACKUP_DIR/data"
    echo "Data directory backed up."
fi

if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env"
    echo "Environment file backed up."
fi

if [ -f "jarvis_core/config/user_config.yaml" ]; then
    cp jarvis_core/config/user_config.yaml "$BACKUP_DIR/user_config.yaml"
    echo "User config backed up."
fi

if [ -d "voice_pipeline/profiles" ]; then
    cp -r voice_pipeline/profiles "$BACKUP_DIR/profiles"
    echo "Voice profiles backed up."
fi

tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo ""
echo "Backup complete: $BACKUP_DIR.tar.gz"