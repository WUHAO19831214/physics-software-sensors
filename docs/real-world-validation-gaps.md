# Real-world validation gaps

Phase 3D makes missing evidence visible; it does not fill it with synthetic claims.

| Sensor | Highest-priority missing validation | Minimum future evidence |
| --- | --- | --- |
| Camera | permission, device negotiation, exposure, drop/reconnect, long run | named camera/OS/backend; resolution/FPS matrix; latency/CPU/memory and reconnect log |
| Screen | actual chooser, tab/window/screen surfaces, scaling and permission cancellation | named browser/OS; user-driven smoke; pixel dimensions/timing and cancellation behavior |
| Number OCR | real instrument software fonts, DPI scaling, antialiasing, negative/decimal formats | de-identified recorded frames with expected values; exact/parse/error/latency report |
| Color marker | illumination, white balance, background, occlusion and calibration | recorded camera set with labelled centers/lost frames and pixel-to-physical calibration kept separate |
| Spot centroid | exposure/saturation, real spot shape, ROI and optics | real laser/LED frames across settings; centroid error and missing rate |
| Template | blur, scale, rotation, occlusion and backend/platform differences | labelled real sequence; success/lost/reacquire, center error, latency and memory |
| YOLO | approved weight/runtime, actual inference, class accuracy and ID stability | artifact hash/license approval; labelled frames; latency/FPS/memory/precision-recall and track-ID metrics |

Repository-wide gaps are Windows/Linux runtime coverage, real hardware evidence, long-duration stability, dependency security review, source-license resolution and an E5 downstream integration with a documented rollback. Until those exist, every sensor remains experimental and no result should be described as metrologically validated.
