# PATCHES — FaceFusion 3.6.1 Modifications

Base: FaceFusion 3.6.1 commit `5b7d145` (Patch 3.6.1 #1078)

---

## Patch 1 — Content Analyser Bypass

**File:** `facefusion/facefusion/content_analyser.py`  
**Nature:** Bypass NSFW content analysis gate  
**Reason:** Pipeline processes user-submitted videos; content gate caused false rejections  
**Env control:** `BYPASS_CONTENT_ANALYSER=1` — applied at runtime via `apply_content_analyser_bypass()` in `bot.py`  
**Forward-compatible:** Yes — env-var controlled, no source edit required

---

## Patch 2 — Execution Provider Override

**File:** `facefusion/facefusion/execution.py` (runtime override)  
**Nature:** Force CUDA execution provider  
**Reason:** Default provider detection unreliable in containerised environments  
**Env control:** `EXECUTION_PROVIDER=cuda`, `FACEFUSION_PROVIDER_OVERRIDE=cuda`  
**Forward-compatible:** Yes

---

## Patch 3 — Progress Callback Integration

**File:** `bot.py` (external integration, not FaceFusion source)  
**Nature:** Intercepts FaceFusion stdout/stderr progress lines via subprocess pipe  
**Reason:** FaceFusion has no native callback API; progress is parsed from tqdm output  
**Pattern:** `[ff] processing: X%|...` regex in `bot.py`  
**Forward-compatible:** Depends on tqdm output format remaining stable

---

## Patch 4 — tenacity Upgrade

**Package:** `tenacity` upgraded from `5.1.5` → `9.1.4`  
**Reason:** `tenacity 5.x` uses `asyncio.coroutine` removed in Python 3.12; `mega.py` depends on tenacity  
**Effect:** `mega.py` now imports correctly on Python 3.12 despite version constraint warning  
**Forward-compatible:** Yes — `mega.py` 1.0.8 works with tenacity 9.x at runtime

---

## Model Stack (non-default selections)

| Setting | Value | Default |
|---------|-------|---------|
| Face swapper | `inswapper_128_fp16` | `inswapper_128` |
| Face enhancer | `gfpgan_1.4` | none |
| Face detector | `retinaface_10g` + `yoloface_8n` | `retinaface_10g` |
| Face embedder | `arcface_w600k_r50` | `arcface_w600k_r50` |
| Pixel boost | enabled | disabled |
