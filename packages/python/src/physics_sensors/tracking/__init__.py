"""Tracking sensor implementations."""

from .color_marker import (
    ColorMarkerConfig,
    ColorMarkerResult,
    ColorMarkerSensor,
    ColorMarkerTracker,
    estimate_hsv_range_from_roi,
)
from .spot_centroid import SpotCentroidConfig, SpotCentroidResult, SpotCentroidSensor, SpotCentroidTracker
from .template import (
    TRACKER_FALLBACK_ORDER,
    TemplateTracker,
    TemplateTrackerResult,
    TemplateTrackerSensor,
    create_opencv_tracker,
    scale_bbox_to_frame,
    validate_bbox,
)
from .yolo import (
    CentroidAssociator,
    ClassFilter,
    DetectorBackend,
    DetectorFrameResult,
    OpenCVHogDetectorBackend,
    RecordedDetectorBackend,
    YoloDetection,
    YoloDetectorBackend,
    YoloTrackerSensor,
)

__all__ = [
    "ColorMarkerConfig",
    "ColorMarkerResult",
    "ColorMarkerSensor",
    "ColorMarkerTracker",
    "estimate_hsv_range_from_roi",
    "SpotCentroidConfig",
    "SpotCentroidResult",
    "SpotCentroidSensor",
    "SpotCentroidTracker",
    "TRACKER_FALLBACK_ORDER",
    "TemplateTracker",
    "TemplateTrackerResult",
    "TemplateTrackerSensor",
    "create_opencv_tracker",
    "scale_bbox_to_frame",
    "validate_bbox",
    "CentroidAssociator",
    "ClassFilter",
    "DetectorBackend",
    "DetectorFrameResult",
    "OpenCVHogDetectorBackend",
    "RecordedDetectorBackend",
    "YoloDetection",
    "YoloDetectorBackend",
    "YoloTrackerSensor",
]
