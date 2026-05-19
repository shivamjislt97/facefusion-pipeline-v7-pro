# Troubleshooting

## GPU not detected
```
nvidia-smi: command not found
```
**Fix:** Install NVIDIA drivers. For Docker: `apt-get install -y nvidia-container-toolkit && systemctl restart docker`. Verify with `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`.

## ONNX CUDA provider unavailable
```
CUDAExecutionProvider not in available providers
```
**Fix:** `pip install onnxruntime-gpu==1.19.2`. Must match CUDA 12.1. Do not install `onnxruntime` (CPU) alongside `onnxruntime-gpu`.

## FFmpeg nvenc unavailable
```
h264_nvenc not found
```
**Fix:** GPU must support NVENC (Tesla T4 does). Verify: `ffmpeg -encoders | grep nvenc`. If missing, fall back: set `OUTPUT_VIDEO_ENCODER=libx264` in `.env`.

## Mega upload failing (EBLOCKED / 402)
Mega blocks cloud server IPs. **Fix:** Use a different Mega account created from a residential IP, or switch to GDrive: set `GDRIVE_ENABLED=1` and configure `DRIVE_TOKEN`.

## Bot not receiving messages
**Check 1:** `BOT_TOKEN` is correct — test with `curl https://api.telegram.org/bot<TOKEN>/getMe`  
**Check 2:** `ALLOWED_USER_ID` matches your Telegram user ID  
**Check 3:** Bot is in polling mode (not webhook) — no webhook should be set

## Job IDs not resetting on restart
`queue_job_seq.clear()` is called in `_restore_queue_state_from_disk()`. If IDs persist, the queue state file is being loaded before the clear. Check `pipeline/logs/startup.log` for `[QUEUE_RESTORED]`.

## Dashboard not loading
**Check:** `DASHBOARD_ENABLED=1` and `DASHBOARD_PORT=7860` in `.env`. Verify port is exposed in Lightning AI studio settings.

## Bot crashes on startup
Check `pipeline/logs/bot_startup.log`. Common causes: missing `BOT_TOKEN`, CUDA not available, missing model files.
