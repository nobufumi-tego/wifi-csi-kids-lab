"""Read and write CSI recordings as simple CSV files.

CSI の記録を CSV ファイルで読み書きする。Excel でも pandas でもそのまま開ける形。

File format (one row = one Wi-Fi packet)::

    # csi-lab v1 source=simulated scenario=walk
    time_s,rssi_dbm,label,sc-28,...,sc-1,sc1,...,sc28
    0.000,-52,walk,31.2,...

- ``time_s``   seconds since the recording started / 記録開始からの秒
- ``rssi_dbm`` received signal strength in dBm (bigger = stronger) / 受信の強さ
- ``label``    what was happening (e.g. ``empty``, ``walk``) / その時していたこと
- ``sc<k>``    amplitude (size of the wave) on subcarrier ``k`` / サブキャリア k の振幅

The same format is written by the simulator (:mod:`csi_lab.simulate`) and by the
capture tool (:mod:`csi_lab.capture`), so every lesson works on both.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray

#: Subcarrier numbers we keep (HT20: -28..-1 and 1..28; 0 is the empty center).
#: サブキャリアの番号。0 番（中央）は電波が乗らないので除く。
SUBCARRIERS: tuple[int, ...] = tuple(k for k in range(-28, 29) if k != 0)
N_SUBCARRIERS: int = len(SUBCARRIERS)  # 56

#: Distance between neighboring subcarriers [Hz] (802.11n, 20 MHz channel).
SUBCARRIER_SPACING_HZ: float = 312_500.0

#: Name of the amplitude column for each subcarrier.
AMP_COLUMNS: tuple[str, ...] = tuple(f"sc{k}" for k in SUBCARRIERS)
META_COLUMNS: tuple[str, ...] = ("time_s", "rssi_dbm", "label")

#: First line of every file. Lines starting with "#" are comments.
FORMAT_TAG: str = "csi-lab v1"

#: Label used when nobody wrote down what was happening.
UNKNOWN_LABEL: str = "unknown"


@dataclass
class Recording:
    """One CSI recording.

    Attributes:
        time_s: Time of each packet in seconds, shape ``(packets,)``.
        rssi_dbm: Signal strength of each packet in dBm, shape ``(packets,)``.
        amplitude: Wave size on each subcarrier, shape ``(packets, 56)``.
            Row = packet (time), column = subcarrier (frequency), in the order of
            :data:`SUBCARRIERS`.
        labels: What was happening at each packet, shape ``(packets,)``.
        info: Extra notes stored in the first line of the file (e.g. ``source``).
    """

    time_s: NDArray[np.float64]
    rssi_dbm: NDArray[np.float64]
    amplitude: NDArray[np.float64]
    labels: NDArray[np.str_]
    info: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Check that all arrays fit together."""
        n = self.time_s.shape[0]
        if self.time_s.ndim != 1:
            raise ValueError(f"time_s must be 1-D, got shape {self.time_s.shape}")
        if n == 0:
            raise ValueError("a recording needs at least one packet")
        if self.amplitude.shape != (n, N_SUBCARRIERS):
            raise ValueError(
                f"amplitude must have shape ({n}, {N_SUBCARRIERS}), got {self.amplitude.shape}"
            )
        if self.rssi_dbm.shape != (n,) or self.labels.shape != (n,):
            raise ValueError("time_s, rssi_dbm and labels must have the same length")
        if np.any(np.diff(self.time_s) < 0):
            raise ValueError("time_s must not go backwards")

    @property
    def n_packets(self) -> int:
        """Number of packets (rows)."""
        return int(self.time_s.shape[0])

    @property
    def duration_s(self) -> float:
        """Length of the recording in seconds."""
        return float(self.time_s[-1] - self.time_s[0])

    @property
    def rate_hz(self) -> float:
        """Average packets per second (0 if there is only one packet)."""
        if self.n_packets < 2 or self.duration_s == 0:
            return 0.0
        return (self.n_packets - 1) / self.duration_s

    def to_dataframe(self) -> pd.DataFrame:
        """Return the recording as a pandas table (same columns as the CSV)."""
        df = pd.DataFrame(self.amplitude, columns=list(AMP_COLUMNS))
        df.insert(0, "label", self.labels)
        df.insert(0, "rssi_dbm", self.rssi_dbm)
        df.insert(0, "time_s", self.time_s)
        return df


def _parse_info(line: str) -> dict[str, str]:
    """Read ``key=value`` pairs from the first comment line."""
    info: dict[str, str] = {}
    for token in line.lstrip("#").split():
        if "=" in token:
            key, value = token.split("=", 1)
            info[key] = value
    return info


def load_csv(path: str | Path) -> Recording:
    """Read a recording written by the simulator or the capture tool.

    Args:
        path: Path to a ``.csv`` file.

    Returns:
        The recording.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If columns are missing or values are not numbers.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    info: dict[str, str] = {}
    with path.open(encoding="utf-8") as f:
        first = f.readline()
    if first.startswith("#"):
        info = _parse_info(first)
    df = pd.read_csv(path, comment="#")
    missing = [c for c in (*META_COLUMNS, *AMP_COLUMNS) if c not in df.columns]
    if missing:
        more = "..." if len(missing) > 5 else ""
        raise ValueError(f"{path}: missing columns {missing[:5]}{more}")
    if df.empty:
        raise ValueError(f"{path}: no packets in file")
    try:
        amplitude = df[list(AMP_COLUMNS)].to_numpy(dtype=np.float64)
        time_s = df["time_s"].to_numpy(dtype=np.float64)
        rssi_dbm = df["rssi_dbm"].to_numpy(dtype=np.float64)
    except ValueError as e:
        raise ValueError(f"{path}: found something that is not a number: {e}") from e
    labels = df["label"].fillna(UNKNOWN_LABEL).astype(str).to_numpy(dtype=np.str_)
    return Recording(time_s, rssi_dbm, amplitude, labels, info)


def save_csv(rec: Recording, path: str | Path) -> Path:
    """Write a recording to a CSV file (folders are created if needed).

    Args:
        rec: The recording to save.
        path: Where to write. Should end with ``.csv``.

    Returns:
        The path that was written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = " ".join([f"# {FORMAT_TAG}", *(f"{k}={v}" for k, v in rec.info.items())])
    df = rec.to_dataframe()
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(header + "\n")
        df.to_csv(f, index=False, float_format="%.3f")
    return path
