# Facefusion Pipeline V5 Pro

Production-grade Telegram bot that accepts Mega video links, processes them through an 11-stage AI face-swap pipeline using FaceFusion 3.6.1 with CUDA acceleration, and delivers output via Mega or Google Drive.

## Requirements

- CUDA 12.1 + cuDNN 8 (Tesla T4 or better, 8GB+ VRAM)
- Python 3.12
- FFmpeg with `h264_nvenc`
- Docker + NVIDIA Container Toolkit (for Docker restore)

## Quick Start

```bash
git clone https://github.com/shivamjislt97/facefusion-pipeline-v7-pro.git
cd facefusion-pipeline-v7-pro
cp .env.example .env
nano .env          # fill in BOT_TOKEN, ALLOWED_USER_ID, MEGA_EMAIL, MEGA_PASSWORD, DRIVE_TOKEN
bash start.sh
```

## Docker Restore

See [RESTORE_DOCKER.md](RESTORE_DOCKER.md) for full steps.

```bash
docker build -t facefusion-pipeline:latest .
docker run -d --gpus all --env-file .env --name pipeline facefusion-pipeline:latest
```

## GitHub Restore (no Docker)

See [RESTORE_GITHUB.md](RESTORE_GITHUB.md) for full steps.

## Telegram Bot Setup

1. Message [@BotFather](https://t.me/BotFather) → `/newbot`
2. Copy the token → set as `BOT_TOKEN` in `.env`
3. Get your user ID from [@userinfobot](https://t.me/userinfobot) → set as `ALLOWED_USER_ID`
4. Start the bot and send a Mega link

## Pipeline Stages

1. Link Receive → 2. Download → 3. Validation → 4. Frame Extraction → 5. Face Analysis → 6. Face Tracking → 7. Face Swap → 8. Enhancement → 9. Frame Validation → 10. Merge/Encode → 11. Upload & Deliver

## Live Dashboard

Available at `DASHBOARD_PUBLIC_URL/live` — shows real-time progress ring, frame counter, GPU stats.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
