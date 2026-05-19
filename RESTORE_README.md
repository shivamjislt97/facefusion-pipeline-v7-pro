# Restore Guide — facefusion-pipeline-v5

> GPU REQUIRED: NVIDIA GPU mandatory. CPU not supported.

## Current Face Detection Settings (v3)
- Model: RetinaFace
- Detector score: 0.65
- Landmarker score: 0.6
- Detector angles: 0, 45, 315
- Selector mode: one | order: best-worst
- Mask: box only | blur: 0.4 | padding: 5/35/30/35
- Enhancer: gfpgan_1.4 | blend: 55
- Skip logic: frames without face → original frame kept

## Option A — Docker (Fastest)
  docker pull sivamjislt97/facefusion-pipeline-v5:v5
  docker run -d --gpus all --name faceswap-pipeline \
    --restart unless-stopped \
    -v $(pwd)/output:/workspace/output \
    sivamjislt97/facefusion-pipeline-v5:v5

## Option B — Google Drive
  rclone copy "gdrive:facefusion-pipeline-v5" ./project --progress --transfers 4
  cd project && pip3 install -r requirements.txt
  python3 bot.py

## Option C — GitHub (Code only, no models)
  git clone https://github.com/shivamjislt97/facefusion-pipeline-v5.git
  pip3 install -r requirements.txt
  # Restore models from GDrive separately:
  rclone copy "gdrive:facefusion-pipeline-v5/facefusion/models" ./facefusion/models

## Troubleshooting
  GPU not detected: ensure nvidia-container-toolkit installed + docker restart
  CUDA error: host CUDA must match image CUDA version
  Face swap missing frames: expected — frames without face are intentionally skipped