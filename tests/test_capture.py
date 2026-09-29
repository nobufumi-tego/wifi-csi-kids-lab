from __future__ import annotations

import io
from pathlib import Path

import pytest

from csi_lab import load_csv
from csi_lab.capture import TIMER_WRAP_US, parse_line, record_lines


def _line(t_us: int, rssi: int = -50, amp: float = 12.5) -> str:
    return "CSI," + ",".join([str(t_us), str(rssi)] + [f"{amp}"] * 56) + "\n"


def test_parse_line() -> None:
    pkt = parse_line(_line(1234))
    assert pkt is not None
    assert pkt.time_us == 1234 and pkt.rssi_dbm == -50 and len(pkt.amplitude) == 56
    assert parse_line("# csi_rx ready\n") is None
    with pytest.raises(ValueError):
        parse_line("CSI,1,2,3\n")
    with pytest.raises(ValueError):
        parse_line(_line(1).replace("12.5", "x", 1))


def test_record_lines_writes_a_loadable_file(tmp_path: Path) -> None:
    lines = ["# csi_rx ready\n", _line(1_000_000), "CSI,broken\n", _line(1_010_000),
             _line(1_020_000)]
    messages: list[str] = []
    path = tmp_path / "rec.csv"
    with path.open("w") as out:
        stats = record_lines(lines, out, "empty", seconds=10.0, on_message=messages.append)
    assert stats.packets == 3 and stats.broken_lines == 1
    assert messages == ["# csi_rx ready"]
    rec = load_csv(path)
    assert rec.n_packets == 3
    assert rec.time_s[1] == pytest.approx(0.01)
    assert set(rec.labels) == {"empty"}
    assert rec.info["source"] == "esp32"


def test_record_lines_stops_after_seconds() -> None:
    lines = [_line(i * 10_000) for i in range(1000)]  # 10 s at 100 per second
    stats = record_lines(lines, io.StringIO(), "walk", seconds=2.0)
    assert stats.packets == 201


def test_record_lines_handles_clock_restart() -> None:
    out = io.StringIO()
    lines = [_line(TIMER_WRAP_US - 10_000), _line(0), _line(10_000)]
    stats = record_lines(lines, out, "x", seconds=10.0)
    assert stats.packets == 3
    assert stats.duration_s == pytest.approx(0.02)
