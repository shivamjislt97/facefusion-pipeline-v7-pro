# MASTER TEST REPORT

- Date: 2026-04-22
- TEST1 status: PASS
- TEST2 status: PASS
- Autosleep 2m evidence: FAIL

## TEST1 (Image)
- Media kind: image
- Stage updates: Downloading -> Processing -> Uploading -> Output Link
- Invalid stages: None
- Output: live_tests/retry_2026_04_22/TEST1_OUTPUT.jpg
- Image diff mean: 1.2266453674121405

## TEST2 (Video)
- Media kind: video
- Stage updates: Downloading -> Extracting Frames -> Face Swap Processing -> Merging Frames -> Uploading -> Output Link
- Invalid stages: None
- Output: live_tests/retry_2026_04_22/TEST2_OUTPUT.mp4
- Video frame diff mean: 1.7161534891010803

## Evidence Files
- live_tests/retry_2026_04_22/TEST1_INPUT.jpg
- live_tests/retry_2026_04_22/TEST1_OUTPUT.jpg
- live_tests/retry_2026_04_22/TEST1_STAGE_LOG.txt
- live_tests/retry_2026_04_22/TEST2_INPUT.mp4
- live_tests/retry_2026_04_22/TEST2_OUTPUT.mp4
- live_tests/retry_2026_04_22/TEST2_STAGE_LOG.txt
- live_tests/retry_2026_04_22/AUTO_SLEEP_LOG.txt
- live_tests/retry_2026_04_22/MASTER_TEST_REPORT.json