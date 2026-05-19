# CRITICAL COMPONENTS — Facefusion Pipeline V5 Pro

> Audit date: 2026-05-19  
> FaceFusion version: 3.6.1 (commit `5b7d145`)  
> Python: 3.12 | CUDA: 12.1 | ONNX Runtime GPU: 1.19.2

---

## Source Files

| File | Purpose | In Backup |
|------|---------|-----------|
| `bot.py` | Main Telegram bot + pipeline orchestrator | ✅ |
| `job_worker.py` | Subprocess worker shim | ✅ |
| `ops/dashboard_server.py` | FastAPI live dashboard | ✅ |
| `ops/job_worker.py` | Queue worker | ✅ |
| `ops/auto_sleep_manager.py` | Auto-sleep config | ✅ |
| `ops/state_manager.py` | Pipeline state persistence | ✅ |
| `ops/safe_cleanup.py` | Temp file cleanup | ✅ |
| `ops/health_monitor.py` | GPU/system health | ✅ |
| `ops/process_guard.py` | Process lifecycle | ✅ |
| `ops/boot_launcher.py` | Boot sequence | ✅ |
| `config/credentials.py` | Credential loading | ✅ |
| `config/__init__.py` | Config package | ✅ |
| `facefusion/` | FaceFusion 3.6.1 (patched) | ✅ |
| `scripts/live_monitor.html` | Live dashboard UI | ✅ |
| `scripts/dashboard.html` | Dashboard UI | ✅ |
| `run.sh` | Pipeline entry point | ✅ |
| `start.sh` | Bot start script | ✅ |
| `startup.py` | Startup shim | ✅ |
| `.lightning/startup.sh` | Lightning AI auto-start | ✅ |

---

## ONNX Models (`facefusion/.assets/models/`)

| Model File | Purpose | Bundled |
|-----------|---------|---------|
| `inswapper_128_fp16.onnx` | Face swap (primary) | ✅ |
| `hyperswap_1a_256.onnx` | Face swap (high-res) | ✅ |
| `gfpgan_1.4.onnx` | Face enhancement | ✅ |
| `retinaface_10g.onnx` | Face detection | ✅ |
| `yoloface_8n.onnx` | Face detection (fast) | ✅ |
| `arcface_w600k_r50.onnx` | Face embedding/tracking | ✅ |
| `fairface.onnx` | Gender/age analysis | ✅ |
| `bisenet_resnet_34.onnx` | Face parsing/masking | ✅ |
| `2dfan4.onnx` | Face landmark detection | ✅ |
| `fan_68_5.onnx` | Face landmark (68-point) | ✅ |
| `xseg_1.onnx` | Face segmentation | ✅ |
| `nsfw_1/2/3.onnx` | Content filtering | ✅ |
| `live_portrait_*.onnx` | Live portrait (3 files) | ✅ |
| `kim_vocal_2.onnx` | Audio processing | ✅ |

---

## Runtime Requirements

| Dependency | Version | Notes |
|-----------|---------|-------|
| Python | 3.12 | System Python on Lightning AI |
| CUDA | 12.1 | nvidia/cuda:12.1.0-cudnn8-devel |
| cuDNN | 8 | Bundled with CUDA image |
| onnxruntime-gpu | 1.19.2 | Must match CUDA version |
| torch | 2.8.0+cu128 | CUDA 12.8 build |
| python-telegram-bot | 20.7 | PTB v20 async API |
| fastapi | 0.135.1 | Dashboard server |
| uvicorn | 0.42.0 | ASGI server |
| mega.py | 1.0.8 | Mega upload SDK |
| tenacity | 9.1.4 | Retry logic (upgraded from 5.x) |
| opencv-python-headless | 4.10.0.84 | Frame processing |
| ffmpeg | system | h264_nvenc required |
| rclone | system | GDrive upload |

---

## Explicitly EXCLUDED from Backup

- `workspace/` — temporary frame extraction directories
- `outputs/` — processed video outputs
- `pipeline/logs/` — runtime logs
- `persistent/jobs/` — job state files
- `.env` — secrets (use `.env.example`)
- `*.mp4`, `*.avi`, `*.mkv` — video files
- `*.jpg`, `*.jpeg`, `*.png` — image/face files
- `__pycache__/`, `*.pyc` — compiled Python
- `rclone.conf` — contains GDrive tokens (regenerate from `DRIVE_TOKEN` env var)
