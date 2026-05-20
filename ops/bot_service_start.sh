#!/bin/bash
# Bot service entry point — ensures clean start, then runs process_guard
PROJECT="/teamspace/studios/this_studio/facefusion-pipeline-v5-pro"
PYTHON="/home/zeus/miniconda3/envs/cloudspace/bin/python"
LOG_DIR="$PROJECT/pipeline/logs"

mkdir -p "$LOG_DIR"

# Clear stale PID files
rm -f "$LOG_DIR/process_guard.pid" "$LOG_DIR/health_monitor.pid" "$LOG_DIR/bot.pid"

# Start health_monitor in background
"$PYTHON" "$PROJECT/ops/health_monitor.py" --interval-sec 120 \
    >> "$LOG_DIR/health_monitor.log" 2>&1 &
echo $! > "$LOG_DIR/health_monitor.pid"

# Run process_guard in foreground (systemd tracks this PID)
exec "$PYTHON" "$PROJECT/ops/process_guard.py" --max-backoff 120
