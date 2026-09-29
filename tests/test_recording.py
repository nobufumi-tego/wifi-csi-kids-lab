from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from csi_lab import SUBCARRIERS, Recording, load_csv, save_csv, simulate


def _tiny(n: int = 4) -> Recording:
    return Recording(
        time_s=np.arange(n, dtype=np.float64) / 100,
        rssi_dbm=np.full(n, -50.0),
        amplitude=np.ones((n, len(SUBCARRIERS))),
        labels=np.array(["empty"] * n),
    )


def test_subcarriers_skip_center() -> None:
    assert len(SUBCARRIERS) == 56
    assert 0 not in SUBCARRIERS
    assert SUBCARRIERS[0] == -28 and SUBCARRIERS[-1] == 28


def test_round_trip(tmp_path: Path) -> None:
    rec = simulate("walk", duration_s=2.0, seed=3)
    path = save_csv(rec, tmp_path / "sub" / "walk.csv")
    back = load_csv(path)
    assert back.n_packets == rec.n_packets
    np.testing.assert_allclose(back.amplitude, rec.amplitude, atol=1e-3)
    np.testing.assert_allclose(back.time_s, rec.time_s, atol=1e-3)
    assert list(back.labels) == list(rec.labels)
    assert back.info["source"] == "simulated"


def test_csv_opens_with_plain_pandas(tmp_path: Path) -> None:
    import pandas as pd

    path = save_csv(_tiny(), tmp_path / "t.csv")
    df = pd.read_csv(path, comment="#")
    assert list(df.columns[:3]) == ["time_s", "rssi_dbm", "label"]
    assert df.shape == (4, 3 + 56)


def test_bad_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="amplitude"):
        Recording(np.zeros(3), np.zeros(3), np.zeros((3, 10)), np.array(["a"] * 3))
    with pytest.raises(ValueError, match="backwards"):
        Recording(np.array([0.0, 1.0, 0.5]), np.zeros(3), np.zeros((3, 56)), np.array(["a"] * 3))
    with pytest.raises(ValueError, match="at least one"):
        Recording(np.zeros(0), np.zeros(0), np.zeros((0, 56)), np.array([], dtype=str))


def test_load_reports_missing_file_and_columns(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "nope.csv")
    bad = tmp_path / "bad.csv"
    bad.write_text("time_s,rssi_dbm\n0,-50\n")
    with pytest.raises(ValueError, match="missing columns"):
        load_csv(bad)


def test_rate_and_duration() -> None:
    rec = _tiny(101)
    assert rec.duration_s == pytest.approx(1.0)
    assert rec.rate_hz == pytest.approx(100.0)
