"""Turn raw CSI into numbers that describe motion.

CSI の生の数字から「どれくらい動いたか」を表す数（特徴量）を作る。

The main idea: when nothing moves, the amplitude on each subcarrier stays almost the
same. When something moves, it wobbles. So "how much it wobbles in one second"
(the standard deviation over time) is a good motion number.
何も動かなければ振幅はほぼ一定。動くとゆれる。1 秒の間のゆれ（標準偏差）が動きの目安になる。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from csi_lab.recording import Recording

DEFAULT_WINDOW_S: float = 1.0
MIN_PACKETS_PER_WINDOW: int = 5  # skip windows with too few packets (e.g. many missed)
TINY: float = 1e-12  # avoids dividing by zero


def normalize_per_packet(amplitude: NDArray[np.float64]) -> NDArray[np.float64]:
    """Divide each packet by its own average over subcarriers.

    The ESP32 changes its volume knob (automatic gain) for every packet, so the raw
    size jumps around even when nothing moves. Dividing by the packet's average
    removes most of that jump and keeps the *shape* across subcarriers.
    パケットごとの平均で割って、受信機の自動的な音量調整の影響を消す。

    Args:
        amplitude: Shape ``(packets, subcarriers)``.

    Returns:
        Same shape; each row averages to 1.

    Raises:
        ValueError: If the array is not 2-D.
    """
    if amplitude.ndim != 2:
        raise ValueError(f"amplitude must be 2-D (packets, subcarriers), got {amplitude.shape}")
    mean = amplitude.mean(axis=1, keepdims=True)
    return np.asarray(amplitude / np.maximum(mean, TINY), dtype=np.float64)


@dataclass(frozen=True)
class Windows:
    """Numbers computed for each time window.

    Attributes:
        start_s: Start time of each window in seconds, shape ``(windows,)``.
        features: One row per window, shape ``(windows, len(names))``.
        names: Name of each feature column.
        labels: Most common label in each window, shape ``(windows,)``.
    """

    start_s: NDArray[np.float64]
    features: NDArray[np.float64]
    names: tuple[str, ...]
    labels: NDArray[np.str_]


FEATURE_NAMES: tuple[str, ...] = (
    "motion",  # mean over subcarriers of the wobble (std over time)
    "motion_max",  # the subcarrier that wobbles the most
    "spread",  # how different the subcarriers are from each other (room "fingerprint")
    "rssi_std_db",  # wobble of the signal strength
    "change_rate",  # how fast the amplitude changes from packet to packet
)


def _majority(labels: NDArray[np.str_]) -> str:
    values, counts = np.unique(labels, return_counts=True)
    return str(values[int(np.argmax(counts))])


def window_features(rec: Recording, window_s: float = DEFAULT_WINDOW_S) -> Windows:
    """Cut the recording into windows and compute motion numbers for each.

    Args:
        rec: A recording (real or simulated).
        window_s: Length of one window in seconds.

    Returns:
        The features of every window that has enough packets.

    Raises:
        ValueError: If ``window_s`` is not positive or no window has enough packets.
    """
    if not window_s > 0:
        raise ValueError(f"window_s must be positive, got {window_s}")
    norm = normalize_per_packet(rec.amplitude)
    t0 = rec.time_s[0]
    index = np.floor((rec.time_s - t0) / window_s).astype(np.int64)
    starts, rows, labels = [], [], []
    for w in np.unique(index):
        sel = index == w
        if sel.sum() < MIN_PACKETS_PER_WINDOW:
            continue
        a = norm[sel]
        wobble = a.std(axis=0)
        rows.append(
            [
                float(wobble.mean()),
                float(wobble.max()),
                float(a.mean(axis=0).std()),
                float(rec.rssi_dbm[sel].std()),
                float(np.abs(np.diff(a, axis=0)).mean()),
            ]
        )
        starts.append(t0 + w * window_s)
        labels.append(_majority(rec.labels[sel]))
    if not rows:
        raise ValueError("no window had enough packets; is the recording very short?")
    return Windows(
        start_s=np.array(starts, dtype=np.float64),
        features=np.array(rows, dtype=np.float64),
        names=FEATURE_NAMES,
        labels=np.array(labels, dtype=np.str_),
    )


def motion_score(rec: Recording, window_s: float = DEFAULT_WINDOW_S) -> tuple[
    NDArray[np.float64], NDArray[np.float64]
]:
    """Return one motion number per window (bigger = more movement).

    Args:
        rec: A recording.
        window_s: Window length in seconds.

    Returns:
        ``(start_s, motion)``: window start times and their motion numbers.
    """
    w = window_features(rec, window_s)
    return w.start_s, w.features[:, FEATURE_NAMES.index("motion")]


def detect_motion(motion: NDArray[np.float64], threshold: float) -> NDArray[np.bool_]:
    """Say "moving" (True) when the motion number is above a threshold.

    Args:
        motion: Motion numbers from :func:`motion_score`.
        threshold: The line between "still" and "moving". Choose it by looking at
            a recording where nothing moves.

    Returns:
        True for windows judged as moving.
    """
    if threshold < 0:
        raise ValueError(f"threshold must not be negative, got {threshold}")
    return np.asarray(motion > threshold, dtype=np.bool_)


def breathing_rate_bpm(
    rec: Recording, min_bpm: float = 6.0, max_bpm: float = 40.0
) -> float:
    """Estimate breaths per minute from a recording of someone sitting still.

    It looks for the strongest slow, regular wobble (between ``min_bpm`` and
    ``max_bpm``) using a Fourier transform, which splits a signal into its rhythms.
    ゆっくりした一定のリズムを探して、1 分あたりの呼吸数を見積もる。

    Args:
        rec: A recording of 30 seconds or more, with the person not moving otherwise.
        min_bpm: Slowest breathing rate to consider (breaths per minute).
        max_bpm: Fastest breathing rate to consider.

    Returns:
        The estimated breaths per minute.

    Raises:
        ValueError: If the recording is too short to see at least two breaths.
    """
    if not 0 < min_bpm < max_bpm:
        raise ValueError("need 0 < min_bpm < max_bpm")
    min_hz, max_hz = min_bpm / 60.0, max_bpm / 60.0
    if rec.duration_s < 2.0 / min_hz:
        raise ValueError(f"recording too short: need at least {2 / min_hz:.0f} s")
    rate_hz = rec.rate_hz
    grid = np.arange(rec.time_s[0], rec.time_s[-1], 1.0 / rate_hz)
    norm = normalize_per_packet(rec.amplitude)
    norm = norm - norm.mean(axis=0)
    # Use the subcarriers that wobble the most; they carry the breathing
    strongest = np.argsort(norm.std(axis=0))[-8:]
    spectrum = np.zeros(grid.size // 2 + 1)
    for k in strongest:
        x = np.interp(grid, rec.time_s, norm[:, k])
        spectrum += np.abs(np.fft.rfft(x * np.hanning(x.size)))
    freqs = np.fft.rfftfreq(grid.size, 1.0 / rate_hz)
    band = (freqs >= min_hz) & (freqs <= max_hz)
    if not band.any():
        raise ValueError("recording too short for this breathing range")
    peak_hz = freqs[band][int(np.argmax(spectrum[band]))]
    return float(peak_hz * 60.0)
