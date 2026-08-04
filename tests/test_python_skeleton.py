from physics_software_sensors import LifecycleState, SensorDescriptor


def test_python_contract_skeleton_imports() -> None:
    descriptor = SensorDescriptor(
        sensor_id="tracker.spot-centroid",
        version="0.1.0",
        category="processor",
        input_kinds=("frame-packet.camera-frame",),
        output_kinds=("sensor-event.centroid",),
    )
    assert descriptor.sensor_id == "tracker.spot-centroid"
    assert LifecycleState.RUNNING.value == "running"
