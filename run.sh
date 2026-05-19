#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT_DIR/pipeline/logs"
mkdir -p "$LOG_DIR"

usage() {
	cat <<'EOF'
Usage:
	./run.sh up      # start lifecycle services (boot launcher)
	./run.sh status  # print guard/monitor/bot process status
	./run.sh stop    # stop guard and monitor (and bot via guard)
EOF
}

show_status() {
	local guard_pid=""
	local monitor_pid=""
	local bot_pid=""
	[[ -f "$LOG_DIR/process_guard.pid" ]] && guard_pid="$(cat "$LOG_DIR/process_guard.pid" 2>/dev/null || true)"
	[[ -f "$LOG_DIR/health_monitor.pid" ]] && monitor_pid="$(cat "$LOG_DIR/health_monitor.pid" 2>/dev/null || true)"
	[[ -f "$LOG_DIR/bot.pid" ]] && bot_pid="$(cat "$LOG_DIR/bot.pid" 2>/dev/null || true)"

	echo "guard_pid=${guard_pid:-0}"
	echo "monitor_pid=${monitor_pid:-0}"
	echo "bot_pid=${bot_pid:-0}"
	ps -eo pid=,ppid=,stat=,etime=,args= | grep -E "(process_guard.py|health_monitor.py|bot.py|job_worker.py)" | grep -v grep || true
}

stop_services() {
	for pf in "$LOG_DIR/health_monitor.pid" "$LOG_DIR/process_guard.pid"; do
		if [[ -f "$pf" ]]; then
			pid="$(cat "$pf" 2>/dev/null || echo "0")"
			if [[ "${pid:-0}" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null; then
				kill "$pid" 2>/dev/null || true
			fi
		fi
	done
}

cmd="${1:-up}"
case "$cmd" in
	up)
		cd "$ROOT_DIR"
		exec python3 ops/boot_launcher.py --interval-sec "${HEALTH_MONITOR_INTERVAL_SEC:-120}" --max-backoff "${PROCESS_GUARD_MAX_BACKOFF_SEC:-120}"
		;;
	status)
		show_status
		;;
	stop)
		stop_services
		;;
	*)
		usage
		exit 1
		;;
esac
