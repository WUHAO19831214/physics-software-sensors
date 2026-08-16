# Dataset Card — YOLO Tracker Source-recorded Replay

- ID: `yolo-tracker-source-recorded-replay-v1`
- File: `tests/fixtures/yolo_tracker/source-golden.json`
- SHA-256: `641e0311c66f5c4508e6bc5990f071ec36627236e63efad18858e1a1bdbf0abd`
- Source repository: `WUHAO19831214/audio-visual-soundfield-tracker-stable`
- Source commit: `85740d686c67452a057540edb564d713e01ccc51`
- Generator: `tools/generate_yolo_source_golden.py`
- Privacy: no camera recording, person image, biometric data or third-party media; synthetic numeric boxes only
- Model artifact: none; no real weight and no neural inference

## Cases

The generator imports the fixed source `Detector` and `CentroidTracker`, injects scripted Ultralytics-shaped results, and records zero target, single target, movement, two targets, lost, reappear, missing native ID, centroid lifecycle/reset, and declared HOG fallback metadata. It also records source calls for confidence, classes, `persist=True` and `bytetrack.yaml`.

## Intended use

Source compatibility, deterministic adapter replay, class-filter behavior, multi-target JSON serialization and lifecycle/fallback regression. It may be regenerated only from the exact source SHA.

## Prohibited interpretation

This is not a labelled image dataset and does not measure YOLO detection quality, real ByteTrack identity quality, HOG person-detection quality, physical position accuracy, camera compatibility or real-time throughput.
