#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file.tar.gz>"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring J.A.R.V.I.S. from backup..."
echo "======================================"

RESTORE_DIR="restore_temp"
mkdir -p "$RESTORE_DIR"
tar -xzf "$BACKUP_FILE" -C "$RESTORE_DIR"

BACKUP_CONTENT=$(ls "$RESTORE_DIR" | head -1)

if [ -d "$RESTORE_DIR/$BACKUP_CONTENT/data" ]; then
    cp -r "$RESTORE_DIR/$BACKUP_CONTENT/data" .
    echo "Data restored."
fi

if [ -f "$RESTORE_DIR/$BACKUP_CONTENT/.env" ]; then
    cp "$RESTORE_DIR/$BACKUP_CONTENT/.env" .
    echo "Environment restored."
fi

rm -rf "$RESTORE_DIR"

echo ""
echo "Restore complete."