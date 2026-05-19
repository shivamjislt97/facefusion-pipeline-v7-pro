#!/bin/bash
PASS=0; FAIL=0

check() {
    if eval "$2" &>/dev/null; then
        echo "PASS  $1"
        ((PASS++))
    else
        echo "FAIL  $1"
        ((FAIL++))
    fi
}

check "nvidia-smi"          "nvidia-smi"
check "ffmpeg"              "ffmpeg -version"
check "ffmpeg h264_nvenc"   "ffmpeg -encoders 2>/dev/null | grep -q h264_nvenc"
check "python3"             "python3 -c 'import sys; assert sys.version_info >= (3,10)'"
check "onnxruntime-gpu"     "python3 -c 'import onnxruntime; assert \"CUDAExecutionProvider\" in onnxruntime.get_available_providers()'"
check "telegram bot"        "python3 -c 'import telegram'"
check "opencv"              "python3 -c 'import cv2'"
check "BOT_TOKEN set"       "[ -n \"$BOT_TOKEN\" ]"
check "ALLOWED_USER_ID set" "[ -n \"$ALLOWED_USER_ID\" ]"
check "facefusion dir"      "[ -d /workspace/facefusion ]"
check "inswapper model"     "[ -f /workspace/facefusion/.assets/models/inswapper_128_fp16.onnx ]"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
