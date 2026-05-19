#!/usr/bin/env python3
import asyncio
import json
import os
import sys
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

TARGET_LINK = os.environ.get(
    "SATISFACTION_TARGET_LINK",
    "https://mega.nz/file/m8JWEC4L#fNAx9nJTxoaT01Em6IMKCWQQzC38AnArPMd6xOxa0ok",
).strip()
ROOT = Path("/teamspace/studios/this_studio")
LOG_PATH = ROOT / "TELEGRAM_E2E_LOG.txt"
JSON_PATH = ROOT / "SATISFACTION_TEST_REPORT.json"
MD_PATH = ROOT / "SATISFACTION_TEST_REPORT.md"

RUNTIME_ROOT = Path(__file__).resolve().parents[1]
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))

import bot as b
from telegram import Bot


class Ctx(SimpleNamespace):
    pass


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Recorder:
    def __init__(self):
        self.lines = []

    def log(self, msg):
        line = f"[{now_iso()}] {msg}"
        self.lines.append(line)
        print(line, flush=True)

    def dump(self):
        LOG_PATH.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def snapshot(chat_id):
    st = (b.job_status.get(str(chat_id), {}) or {}).copy()
    active = b._get_active_job_state(str(chat_id), allow_fallback=True) or {}
    q = b.job_queues.get(str(chat_id), []) or []
    worker = b.queue_workers.get(str(chat_id))
    return {
        "phase": str(st.get("phase") or active.get("phase") or active.get("status") or "").lower(),
        "stage": str(st.get("stage") or active.get("stage") or ""),
        "job_id": int(st.get("job_id") or active.get("job_id") or 0),
        "queue_len": len(q),
        "queue_worker_alive": bool(worker and not worker.done()),
        "worker_pid": int(active.get("worker_pid") or st.get("worker_pid") or 0),
        "processing_pid": int(active.get("processing_pid") or st.get("processing_pid") or 0),
        "details": str(st.get("details") or active.get("details") or ""),
        "upload_link": str(st.get("upload_link") or active.get("upload_link") or ""),
        "output_path": str(st.get("output_path") or active.get("output_path") or ""),
    }


def latest_worker_result(chat_id):
    log_dir = Path(b.PIPELINE) / "logs"
    files = sorted(log_dir.glob(f"worker_result_{chat_id}_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in files:
        try:
            return str(p), json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return "", {}


def latest_output_since(ts):
    for p in b.list_swap_outputs():
        with contextlib_suppress():
            if float(p.stat().st_mtime) >= ts:
                return str(p), int(p.stat().st_size)
    return "", 0


class contextlib_suppress:
    def __init__(self, *exc):
        self.exc = exc or (Exception,)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex, tb):
        return bool(ex_type and issubclass(ex_type, self.exc))


async def remediate(chat_id, reason, rec):
    rec.log(f"REMEDIATE reason={reason[:220]}")
    with contextlib_suppress():
        await asyncio.to_thread(b._kill_orphan_job_processes, str(chat_id))
    with contextlib_suppress():
        b._stop_active_job(str(chat_id))
    b.job_queues[str(chat_id)] = []
    await asyncio.sleep(2)


async def run_attempt(ctx, chat_id, rec, timeout_sec=2400):
    start_ts = time.time()
    rec.log(f"ATTEMPT send_link chat={chat_id}")
    await b.safe_send_message(ctx.bot, str(chat_id), "Satisfaction E2E test: injecting provided MEGA link now.")
    await b._auto_simulate_text(ctx, str(chat_id), TARGET_LINK)

    last_key = None
    phases_seen = []

    while time.time() - start_ts < timeout_sec:
        s = snapshot(chat_id)
        key = (s["phase"], s["stage"], s["queue_len"], s["queue_worker_alive"])
        if key != last_key:
            phases_seen.append({"t": now_iso(), **s})
            rec.log(
                f"MONITOR phase={s['phase'] or '-'} stage={s['stage'] or '-'} "
                f"queue={s['queue_len']} qworker={int(s['queue_worker_alive'])} "
                f"worker_pid={s['worker_pid']} proc_pid={s['processing_pid']}"
            )
            last_key = key

        wr_path, wr = latest_worker_result(str(chat_id))
        wr_phase = str((wr or {}).get("phase") or "").lower()
        out_path, out_size = latest_output_since(start_ts)

        if s["phase"] in {"failed", "stopped", "exception"}:
            reason = s["details"] or str((wr or {}).get("details") or "") or s["stage"] or s["phase"]
            return {
                "ok": False,
                "reason": reason,
                "phase": s["phase"],
                "stage": s["stage"],
                "snapshot": s,
                "phases_seen": phases_seen,
                "worker_result_path": wr_path,
                "worker_result": wr,
            }

        if (s["phase"] == "completed" or wr_phase == "completed") and out_path:
            return {
                "ok": True,
                "phase": s["phase"] or wr_phase,
                "stage": s["stage"] or str((wr or {}).get("stage") or ""),
                "snapshot": s,
                "phases_seen": phases_seen,
                "output_path": out_path,
                "output_size": out_size,
                "worker_result_path": wr_path,
                "worker_result": wr,
                "upload_ok": bool((wr or {}).get("upload_ok")),
                "upload_link": str((wr or {}).get("upload_link") or s.get("upload_link") or ""),
            }

        await asyncio.sleep(2)

    s = snapshot(chat_id)
    return {
        "ok": False,
        "reason": f"timeout phase={s['phase']} stage={s['stage']}",
        "phase": s["phase"],
        "stage": s["stage"],
        "snapshot": s,
        "phases_seen": phases_seen,
        "worker_result_path": latest_worker_result(str(chat_id))[0],
        "worker_result": latest_worker_result(str(chat_id))[1],
    }


async def main():
    rec = Recorder()
    result = {
        "started_at": now_iso(),
        "target_link": TARGET_LINK,
        "attempts": [],
        "final_status": "UNKNOWN",
    }

    try:
        b.reload_runtime_credentials()
        chat_id = str(b.ALLOWED_CHAT_ID)
        token = str(b.BOT_TOKEN or "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN missing")

        ctx = Ctx(bot=Bot(token=token), application=None, user_data={}, chat_data={}, bot_data={})

        rec.log(
            f"INIT chat={chat_id} authorized={b.is_authorized(b.ALLOWED_USER_ID, int(chat_id))} "
            f"mega={b.can_use_mega()} gdrive={b.can_use_gdrive()} provider={b.EXECUTION_PROVIDER}"
        )

        with contextlib_suppress():
            await asyncio.to_thread(b._kill_orphan_job_processes, chat_id)
        with contextlib_suppress():
            b._stop_active_job(chat_id)
        b.job_queues[chat_id] = []

        success = None
        for idx in range(1, 4):
            rec.log(f"ATTEMPT {idx} BEGIN")
            att = await run_attempt(ctx, chat_id, rec)
            att["attempt_no"] = idx
            result["attempts"].append(att)
            if att.get("ok"):
                success = att
                rec.log(f"ATTEMPT {idx} SUCCESS output={att.get('output_path')} bytes={att.get('output_size')}")
                break
            rec.log(f"ATTEMPT {idx} FAIL reason={str(att.get('reason') or '')[:240]}")
            if idx < 3:
                await remediate(chat_id, str(att.get("reason") or "unknown"), rec)

        if success:
            result["final_status"] = "PASS"
            result["final_output_path"] = success.get("output_path", "")
            result["final_output_size"] = int(success.get("output_size") or 0)
            result["final_upload_ok"] = bool(success.get("upload_ok"))
            result["final_upload_link"] = success.get("upload_link", "")
            await b.safe_send_message(ctx.bot, chat_id, "Satisfaction E2E test PASSED with provided MEGA link.")
        else:
            result["final_status"] = "FAIL"
            await b.safe_send_message(ctx.bot, chat_id, "Satisfaction E2E test FAILED after retries. Check report files.")

        result["ended_at"] = now_iso()

    except Exception as e:
        rec.log(f"FATAL {type(e).__name__}: {e}")
        rec.log(traceback.format_exc())
        result["final_status"] = "ERROR"
        result["error"] = f"{type(e).__name__}: {e}"
        result["ended_at"] = now_iso()

    rec.dump()
    JSON_PATH.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")

    lines = [
        "# SATISFACTION TEST REPORT",
        "",
        f"- Started: {result.get('started_at','')}",
        f"- Ended: {result.get('ended_at','')}",
        f"- Target link: {TARGET_LINK}",
        f"- Final status: {result.get('final_status','')}",
        f"- Attempts: {len(result.get('attempts', []))}",
        "",
        "## Attempt Details",
        "",
    ]

    for att in result.get("attempts", []):
        lines.append(f"### Attempt {att.get('attempt_no')} - {'PASS' if att.get('ok') else 'FAIL'}")
        lines.append(f"- Phase: {att.get('phase','')}")
        lines.append(f"- Stage: {att.get('stage','')}")
        if att.get("ok"):
            lines.append(f"- Output: {att.get('output_path','')}")
            lines.append(f"- Output bytes: {att.get('output_size',0)}")
            lines.append(f"- Upload ok: {att.get('upload_ok', False)}")
            lines.append(f"- Upload link present: {bool(att.get('upload_link',''))}")
        else:
            lines.append(f"- Failure reason: {att.get('reason','')}")
        lines.append("")

    lines.append("## Verdict")
    lines.append("")
    if result.get("final_status") == "PASS":
        lines.append("- Real output generated successfully from provided link.")
        lines.append("- Queue and worker progressed through terminal completion.")
        lines.append("- Delivery evidence recorded in log and worker result state.")
    else:
        lines.append("- Satisfaction loop did not reach successful output within retry budget.")
        lines.append("- See TELEGRAM_E2E_LOG.txt for root-cause trail.")

    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": result.get("final_status"), "json": str(JSON_PATH), "md": str(MD_PATH), "log": str(LOG_PATH)}))


if __name__ == "__main__":
    asyncio.run(main())
