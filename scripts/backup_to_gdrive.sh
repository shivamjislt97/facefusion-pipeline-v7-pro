#!/bin/bash
set -euo pipefail

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="facefusion_pipeline_backup_${TIMESTAMP}.tar.gz"
STAGING="/tmp/backup_staging_${TIMESTAMP}"

echo "Creating backup: ${BACKUP_NAME}"

rsync -a \
    --exclude='.env' \
    --exclude='workspace/' \
    --exclude='outputs/' \
    --exclude='pipeline/logs/' \
    --exclude='persistent/jobs/' \
    --exclude='*.mp4' --exclude='*.avi' --exclude='*.mkv' \
    --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.png' --exclude='*.gif' \
    --exclude='__pycache__/' --exclude='*.pyc' \
    --exclude='.git/' \
    --exclude='rclone.conf' \
    --exclude='.mega_creds' \
    "$PROJECT/" "$STAGING/"

tar -czf "/tmp/${BACKUP_NAME}" -C /tmp "backup_staging_${TIMESTAMP}/"
echo "Archive: /tmp/${BACKUP_NAME} ($(du -sh /tmp/${BACKUP_NAME} | cut -f1))"

echo "Uploading to GDrive..."
python3 "$PROJECT/scripts/gdrive_upload.py" "/tmp/${BACKUP_NAME}" "FacefusionBackups"

rm -rf "$STAGING" "/tmp/${BACKUP_NAME}"
echo "Done: ${BACKUP_NAME}"
