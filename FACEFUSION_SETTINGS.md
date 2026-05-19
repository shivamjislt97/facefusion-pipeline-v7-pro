# FACEFUSION SETTINGS — Non-Default Configuration

FaceFusion 3.6.1 | Commit `5b7d145`

---

## Execution

| Setting | Value | Notes |
|---------|-------|-------|
| `EXECUTION_PROVIDER` | `cuda` | Force GPU; default is auto-detect |
| `EXECUTION_THREAD_COUNT` | `4` | Parallel frame threads |
| `OUTPUT_VIDEO_ENCODER` | `h264_nvenc` | GPU-accelerated encoding |

---

## Face Swap

| Setting | Value | Notes |
|---------|-------|-------|
| `FACE_SWAPPER_MODEL` | `hyperswap_1a_256` | High-res swap model |
| `FACE_SWAPPER_PIXEL_BOOST` | `512x512` | Upscale before swap |
| `FACE_SWAPPER_WEIGHT` | `0.85` | Blend strength |

---

## Face Enhancement

| Setting | Value | Notes |
|---------|-------|-------|
| `ENABLE_FACE_ENHANCER` | `1` | Post-swap enhancement on |
| `FACE_ENHANCER_MODEL` | `gfpgan_1.4` | GFPGAN v1.4 |
| `FACE_ENHANCER_BLEND` | `80` | 80% enhancement blend |
| `FACE_ENHANCER_WEIGHT` | `0.70` | Model weight |
| `ENABLE_EXPRESSION_RESTORER` | `0` | Off — adds latency |

---

## Face Detection

| Setting | Value | Notes |
|---------|-------|-------|
| `FACE_DETECTOR_SCORE` | `0.60` | Detection confidence threshold |
| `FACE_LANDMARKER_SCORE` | `0.35` | Landmark confidence threshold |

---

## Face Masking

| Setting | Value |
|---------|-------|
| `FACE_MASK_BLUR` | `0.3` |
| `FACE_MASK_PADDING_TOP/RIGHT/BOTTOM/LEFT` | `0` |

---

## Content Filtering

| Setting | Value | Notes |
|---------|-------|-------|
| `BYPASS_CONTENT_ANALYSER` | `1` | Disable NSFW gate |

---

## Default Face Source

`DEFAULT_FACE_MEGA_LINK` — stored in `.env`, not committed to repo.
