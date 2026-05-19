#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
mkdir -p pipeline/logs
nohup bash ./run.sh up > pipeline/logs/lifecycle_boot.out 2>&1 &
echo $! > pipeline/logs/lifecycle_boot.pid
