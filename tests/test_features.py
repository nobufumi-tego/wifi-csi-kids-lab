from __future__ import annotations

import numpy as np
import pytest

from csi_lab import simulate, simulate_sequence
from csi_lab.features import (
    FEATURE_NAMES,
    breathing_rate_bpm,
    detect_motion,
    motion_score,
    normalize_per_packet,
    window_features,
)


def test_normalize_removes_packet_volume() -> None:
    amp = np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]])
    norm = normalize_per_packet(amp)
    np.testing.assert_allclose(norm[0], norm[1])
    np.testing.assert_allclose(norm.mean(axis=1), 1.0)
    with pytest.raises(ValueError):
        normalize_per_packet(np.ones(3))


def test_window_features_shape_and_labels() -> None:
    rec = simulate_sequence([("empty", 3.0), ("walk", 3.0)], seed=1)
    w = window_features(rec, window_s=1.0)
    assert w.features.shape == (6, len(FEATURE_NAMES))
    assert list(w.labels) == ["empty"] * 3 + ["walk"] * 3
    assert np.all(np.diff(w.start_s) > 0)


def test_window_features_rejects_bad_window() -> None:
    with pytest.raises(ValueError):
        window_features(simulate("empty", 1.0), window_s=0)


def test_threshold_detector_finds_walking() -> None:
    rec = simulate_sequence([("empty", 10.0), ("walk", 10.0), ("empty", 10.0)], seed=4)
    _, motion = motion_score(rec)
    _, calm = motion_score(simulate("empty", 10.0, seed=9))
    moving = detect_motion(motion, threshold=float(calm.max()) * 1.5)
    truth = window_features(rec).labels == "walk"
    assert (moving == truth).mean() >= 0.9
    with pytest.raises(ValueError):
        detect_motion(motion, -1.0)


def test_breathing_rate_found_in_simulator() -> None:
    bpm = breathing_rate_bpm(simulate("breathe", 60.0, seed=3))
    assert bpm == pytest.approx(15.0, abs=1.5)


def test_breathing_needs_long_recording() -> None:
    with pytest.raises(ValueError, match="too short"):
        breathing_rate_bpm(simulate("breathe", 5.0))
