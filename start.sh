#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
mkdir -p pipeline/logs
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) [start.sh] lifecycle startup" >> pipeline/logs/startup.log
exec ./run.sh up
