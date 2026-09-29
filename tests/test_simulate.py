from __future__ import annotations

import numpy as np
import pytest

from csi_lab import SCENARIOS, simulate, simulate_sequence
from csi_lab.features import motion_score


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_every_scenario_makes_a_valid_recording(name: str) -> None:
    rec = simulate(name, duration_s=5.0, seed=1)
    assert rec.amplitude.shape == (rec.n_packets, 56)
    assert np.all(np.isfinite(rec.amplitude)) and np.all(rec.amplitude >= 0)
    assert set(rec.labels) == {name}
    # about 100 packets per second, a few are missed on purpose
    assert 95 < rec.rate_hz < 105
    assert 450 < rec.n_packets <= 500


def test_same_seed_same_result_different_seed_different_result() -> None:
    a = simulate("walk", 3.0, seed=5)
    b = simulate("walk", 3.0, seed=5)
    c = simulate("walk", 3.0, seed=6)
    np.testing.assert_array_equal(a.amplitude, b.amplitude)
    assert not np.array_equal(a.amplitude[:100], c.amplitude[:100])


def test_walking_moves_the_signal_more_than_sitting_still() -> None:
    _, walk = motion_score(simulate("walk", 20.0, seed=2))
    _, still = motion_score(simulate("still", 20.0, seed=2))
    _, empty = motion_score(simulate("empty", 20.0, seed=2))
    assert np.median(walk) > 2 * np.median(still)
    assert np.median(still) < 1.2 * np.median(empty)


def test_sequence_labels_follow_the_steps() -> None:
    rec = simulate_sequence([("empty", 2.0), ("walk", 3.0)], seed=0)
    assert rec.labels[0] == "empty" and rec.labels[-1] == "walk"
    change = int(np.argmax(rec.labels == "walk"))
    assert rec.time_s[change] == pytest.approx(2.0, abs=0.05)
    assert np.all(np.diff(rec.time_s) >= 0)


def test_room_seed_changes_the_room() -> None:
    a = simulate("empty", 1.0, seed=0, room_seed=1).amplitude.mean(axis=0)
    b = simulate("empty", 1.0, seed=0, room_seed=2).amplitude.mean(axis=0)
    assert not np.allclose(a, b, rtol=0.05)


@pytest.mark.parametrize(
    ("steps", "match"),
    [([("dance", 1.0)], "unknown scenario"), ([("walk", 0.0)], "positive"), ([], "empty")],
)
def test_bad_arguments(steps: list[tuple[str, float]], match: str) -> None:
    with pytest.raises(ValueError, match=match):
        simulate_sequence(steps)
