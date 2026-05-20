# Recent Changes Report — 2026-05-20

---

## 1. Upload Provider — GDrive Primary (Mega Secondary)

**Problem:** Lightning AI server ka IP Mega ke infrastructure se blocked hai (EBLOCKED error).

**Changes (`bot.py`):**
- `smart_upload()` — GDrive pehle try karta hai, Mega sirf fallback
- Re-upload keyboard updated:
  - `📁 GDrive ✅ Recommended` — pehle
  - `☁️ Mega ⚠️ May fail on this server` — neeche
- Mega EBLOCKED error pe informative message:
  > "⚠️ Mega Upload Blocked — This server's IP is blocked by Mega. Please use GDrive instead..."

---

## 2. GDrive Backup — Final Run ✅

**Archive:** `facefusion_pipeline_backup_20260520_165641.tar.gz` (2.0 GB)  
**GDrive File ID:** `1xieUWmguWmADnRuNLaA7z9GudgUcIYkM`  
**Link:** https://drive.google.com/open?id=1xieUWmguWmADnRuNLaA7z9GudgUcIYkM

**Verification:**
- ✅ Critical files present: `bot.py`, `job_worker.py`, `Dockerfile`, `PATCHES.md`, `dashboard.html`
- ✅ Excluded files absent: `.env`, media files, workspace
- ✅ Healthcheck: 12/15 passed (3 expected failures — rclone binary + `.env` excluded by design)

---

## 3. BACKUP_LOG.md — Created ✅

File `BACKUP_LOG.md` project root mein create ki — backup history track karne ke liye.

---

## 4. Bot Auto-Start — Systemd Service ✅

**Problem:** Bot manually start karna padta tha har reboot/crash ke baad.

**Solution:** Systemd service install ki — `/etc/systemd/system/faceswap-bot.service`

| Feature | Status |
|---|---|
| System boot pe auto-start | ✅ enabled |
| Crash pe auto-restart | ✅ Restart=always |
| Duplicate instance prevention | ✅ process_guard.py singleton |
| Lightning Studio resume hook | ✅ on_start.sh updated |
| Logs | `pipeline/logs/bot_service.log` |

**New file:** `ops/bot_service_start.sh` — clean startup wrapper

---

## 5. New Bot Token ✅

**Old:** `8779791358:AAGnQIpfWSXwsFYmiVuKlBB2ANXCnRCFArA`  
**New:** `8779791358:AAEoc3JW8G9EMZx_QBeNVZ2fFmoI8GyXq28`

Updated in `.env` — confirmed active in live API calls.

---

## 6. Dashboard Tracking URL Fix ✅

**Problem:** Har naye job pe Telegram pe tracking URL nahi aata tha.

**Root cause:** Bot public URL pe `/healthz` check karta tha → Lightning proxy 404 deta tha → URL block ho jaata tha.

**Fixes:**
- Health check ab `localhost:7860/healthz` pe hota hai
- `.env` mein correct URL set: `https://7860-01krxgywrxv27hb0jwkhahmbv1.cloudspaces.litng.ai`
- Bot ab `/live` append karke bhejta hai → final URL: `https://7860-01krxgywrxv27hb0jwkhahmbv1.cloudspaces.litng.ai/live`

---

## Current System Status

| Component | Status |
|---|---|
| Bot process | ✅ Running |
| Process Guard | ✅ Running |
| Systemd service | ✅ active |
| Auto-start on reboot | ✅ enabled |
| Active token | ✅ New token confirmed |
| GDrive upload | ✅ Primary provider |
| Dashboard URL | ✅ Correct URL sending |
| GitHub | ✅ Pushed (commit `ea79e18`) |

---

Sab changes live hain aur working hain. ✅
