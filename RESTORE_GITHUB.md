# GitHub Restore Guide (No Docker)

## Steps

**1. Clone**
```bash
git clone https://github.com/shivamjislt97/facefusion-pipeline-v7-pro.git
cd facefusion-pipeline-v7-pro
```

**2. Python environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install onnxruntime-gpu==1.19.2
pip install python-telegram-bot==20.7 fastapi==0.135.1 uvicorn==0.42.0 \
    mega.py==1.0.8 tenacity==9.1.4 opencv-python-headless==4.10.0.84 \
    numpy pillow requests
```

**3. System dependencies**
```bash
apt-get install -y ffmpeg rclone
```

**4. Configure**
```bash
cp .env.example .env
nano .env   # set all required variables
```

**5. Health check**
```bash
python3 scripts/healthcheck.py
```
Fix any FAIL items before proceeding.

**6. Start**
```bash
bash start.sh
```

**7. Verify**
- Telegram admin chat receives startup notification
- Send a Mega link to the bot
