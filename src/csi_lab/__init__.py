"""csi_lab: learn Wi-Fi sensing (CSI) step by step.

Wi-Fi の電波の「ゆれ」（CSI）を使って、人の動きを調べるための学習用パッケージ。

Main pieces:
    recording  -- read / write CSI recordings (CSV)
    simulate   -- make pretend (synthetic) recordings without any hardware
    features   -- turn raw CSI into numbers that describe motion
    plot       -- quick pictures of a recording
    capture    -- record CSI from your own ESP32 receiver
"""

from __future__ import annotations

from csi_lab.recording import SUBCARRIERS, Recording, load_csv, save_csv
from csi_lab.simulate import SCENARIOS, simulate, simulate_sequence

__all__ = [
    "SCENARIOS",
    "SUBCARRIERS",
    "Recording",
    "load_csv",
    "save_csv",
    "simulate",
    "simulate_sequence",
]

__version__ = "0.1.0"
