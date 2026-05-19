#!/bin/bash
set -euo pipefail

# Load .env if present
if [ -f /workspace/.env ]; then
    set -a; source /workspace/.env; set +a
fi

echo "Running health checks..."
if ! /healthcheck.sh; then
    echo "ERROR: Health checks failed. Aborting startup."
    exit 1
fi

echo "Starting Facefusion Pipeline Bot..."
exec python3 /workspace/bot.py
