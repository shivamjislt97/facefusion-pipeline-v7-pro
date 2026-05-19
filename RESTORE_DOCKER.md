# Docker Restore Guide

## Prerequisites

- Linux host with NVIDIA GPU (8GB+ VRAM)
- Docker installed
- NVIDIA Container Toolkit installed

## Steps

**1. Clone**
```bash
git clone https://github.com/shivamjislt97/facefusion-pipeline-v7-pro.git
cd facefusion-pipeline-v7-pro
```

**2. Configure**
```bash
cp .env.example .env
nano .env   # set BOT_TOKEN, ALLOWED_USER_ID, MEGA_EMAIL, MEGA_PASSWORD, DRIVE_TOKEN
```

**3. Verify NVIDIA Docker runtime**
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```
If this fails: `apt-get install -y nvidia-container-toolkit && systemctl restart docker`

**4. Build**
```bash
docker build -t facefusion-pipeline:latest .
```

**5. Health check**
```bash
docker run --rm --gpus all --env-file .env facefusion-pipeline:latest bash /healthcheck.sh
```
All checks must show PASS before proceeding.

**6. Run**
```bash
docker run -d --gpus all --env-file .env \
  --name pipeline \
  -p 7860:7860 \
  facefusion-pipeline:latest
```

**7. Verify**
- Check Telegram admin chat for startup notification (within 30s)
- Send a test Mega link — dashboard URL should return within 2s
- Monitor logs: `docker logs -f pipeline`
