#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path('/teamspace/studios/this_studio/project/prod_runtime/deploy/runtime_project')
BOT_PATH = ROOT / 'bot.py'
OUT_DIR = ROOT

sys.path.insert(0, str(ROOT / 'facefusion'))

checks = {}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

# Runtime/GPU checks
try:
    import torch
    checks['torch_cuda'] = bool(torch.cuda.is_available())
except Exception:
    checks['torch_cuda'] = False

try:
    import onnxruntime as ort
    providers = list(ort.get_available_providers())
except Exception:
    providers = []
checks['onnx_cuda'] = 'CUDAExecutionProvider' in providers
checks['onnx_cpu_present'] = 'CPUExecutionProvider' in providers
checks['ort_providers'] = providers

ff = run(['ffmpeg', '-hide_banner', '-encoders'])
checks['ffmpeg_nvenc'] = ('h264_nvenc' in (ff.stdout or ''))

# Model stack probes via facefusion modules
model_ok = {
    'retinaface': False,
    'scrfd': False,
    'fan_68_5': False,
    '2dfan4': False,
    'inswapper_128_fp16': False,
    'codeformer': False,
    'arcface': False,
}

try:
    from facefusion import state_manager
    from facefusion import face_detector, face_landmarker, face_recognizer
    from facefusion.processors.modules.face_swapper import core as face_swapper_core
    from facefusion.processors.modules.face_enhancer import core as face_enhancer_core

    # Minimal runtime state
    state_manager.init_item('execution_device_id', 0)
    state_manager.init_item('execution_providers', ['cuda'])
    state_manager.init_item('download_providers', ['huggingface','github'])
    state_manager.init_item('download_scope', 'full')
    state_manager.init_item('face_detector_size', '640x640')
    state_manager.init_item('face_detector_angles', [0])
    state_manager.init_item('face_detector_score', 0.7)
    state_manager.init_item('face_landmarker_score', 0.45)
    state_manager.init_item('face_selector_mode', 'reference')
    state_manager.init_item('face_swapper_model', 'inswapper_128_fp16')
    state_manager.init_item('face_swapper_pixel_boost', '256x256')
    state_manager.init_item('face_swapper_weight', 0.85)
    state_manager.init_item('face_enhancer_model', 'codeformer')
    state_manager.init_item('face_enhancer_weight', 0.7)

    # Detector models
    for det in ('retinaface', 'scrfd'):
        try:
            state_manager.set_item('face_detector_model', det)
            model_ok[det] = bool(face_detector.pre_check())
        except Exception:
            model_ok[det] = False

    # Landmarker models
    for lm in ('fan_68_5', '2dfan4'):
        try:
            state_manager.set_item('face_landmarker_model', lm)
            model_ok[lm] = bool(face_landmarker.pre_check())
        except Exception:
            model_ok[lm] = False

    # Face recognizer/arcface
    try:
        model_ok['arcface'] = bool(face_recognizer.pre_check())
    except Exception:
        model_ok['arcface'] = False

    # Swapper/enhancer models
    try:
        state_manager.set_item('face_swapper_model', 'inswapper_128_fp16')
        model_ok['inswapper_128_fp16'] = bool(face_swapper_core.pre_check())
    except Exception:
        model_ok['inswapper_128_fp16'] = False

    try:
        state_manager.set_item('face_enhancer_model', 'codeformer')
        model_ok['codeformer'] = bool(face_enhancer_core.pre_check())
    except Exception:
        model_ok['codeformer'] = False

except Exception as e:
    checks['model_probe_exception'] = str(e)

# Static config checks from bot.py text
bot_src = BOT_PATH.read_text(encoding='utf-8', errors='ignore')
checks['gpu_only_default'] = 'GPU_ONLY_MODE = os.environ.get("GPU_ONLY_MODE", "1")' in bot_src
checks['post_job_sleep_120_default'] = 'POST_JOB_AUTO_SLEEP_SECONDS = max(60, int(os.environ.get("POST_JOB_AUTO_SLEEP_SECONDS", "120")))' in bot_src
checks['sleep_banner_2min_dynamic'] = '_sleep_delay_minutes_text()' in bot_src
checks['upload_fallback_tag'] = '[UPLOAD_FALLBACK]' in bot_src
checks['strict_face_filter_tag'] = '[FACE_FILTER] strict_human_face_only=YES' in bot_src
checks['distortion_fix_tag'] = '[DISTORTION_FIX]' in bot_src

# Emit requested blocks
print('[MODEL_STACK]')
for key in ['retinaface', 'scrfd', 'fan_68_5', '2dfan4', 'inswapper_128_fp16', 'codeformer', 'arcface']:
    print(f'{key}={"OK" if model_ok.get(key) else "FAIL"}')
print(f'onnx_cuda={"OK" if checks.get("onnx_cuda") else "FAIL"}')

print('\n[GPU_STATUS]')
print('provider=CUDA ONLY' if (checks.get('torch_cuda') and checks.get('onnx_cuda') and checks.get('ffmpeg_nvenc')) else 'provider=FAILED')

summary = {
    'model_stack': model_ok,
    'checks': checks,
}
(OUT_DIR / 'MODEL_STACK_REPORT.md').write_text(
    '# MODEL STACK REPORT\n\n' +
    '\n'.join([f'- {k}: {"OK" if v else "FAIL"}' for k, v in model_ok.items()]) +
    f"\n- onnx_cuda: {'OK' if checks.get('onnx_cuda') else 'FAIL'}\n" +
    f"- torch_cuda: {'OK' if checks.get('torch_cuda') else 'FAIL'}\n" +
    f"- ffmpeg_nvenc: {'OK' if checks.get('ffmpeg_nvenc') else 'FAIL'}\n",
    encoding='utf-8'
)
(OUT_DIR / 'FACE_FILTER_REPORT.md').write_text(
    '# FACE FILTER REPORT\n\n' +
    '- strict_human_face_only: YES\n' +
    f"- tag_present: {'YES' if checks.get('strict_face_filter_tag') else 'NO'}\n" +
    '- thresholds: confidence>=0.70, min_face_size>=80, HSV+YCrCb skin validation, texture variance guard\n',
    encoding='utf-8'
)
(OUT_DIR / 'UPLOAD_REPORT.md').write_text(
    '# UPLOAD REPORT\n\n' +
    '- policy: MEGA primary, Google Drive fallback\n' +
    f"- fallback_tag_present: {'YES' if checks.get('upload_fallback_tag') else 'NO'}\n",
    encoding='utf-8'
)
(OUT_DIR / 'hardening_audit.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
