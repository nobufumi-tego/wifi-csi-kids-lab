"""Record CSI from your own ESP32 receiver (firmware/csi_rx) into a CSV file.

自分の ESP32 受信機から CSI を受け取り、CSV ファイルに保存する。

The receiver prints one line per packet over USB::

    CSI,<time_us>,<rssi_dbm>,<amp sc-28>,...,<amp sc28>

Lines starting with ``#`` are messages from the receiver and are shown on screen.
Rows are written to the file as they arrive, so stopping early (Ctrl+C) keeps
everything recorded so far.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TextIO

from csi_lab.recording import AMP_COLUMNS, FORMAT_TAG, META_COLUMNS, N_SUBCARRIERS

BAUD_RATE: int = 921_600  # must match the receiver firmware (bits per second)
LINE_PREFIX: str = "CSI,"
N_FIELDS: int = 3 + N_SUBCARRIERS  # "CSI", time, rssi, 56 amplitudes
US_PER_S: float = 1_000_000.0
TIMER_WRAP_US: int = 2**32  # the receiver's clock counts up to 2^32 us, then restarts
FIRST_DATA_TIMEOUT_S: float = 5.0
READ_TIMEOUT_S: float = 0.5
DEFAULT_OUT_DIR: Path = Path("data") / "my-recordings"


class CaptureError(RuntimeError):
    """Something went wrong while recording (message explains what to check)."""


@dataclass(frozen=True)
class Packet:
    """One line from the receiver.

    Attributes:
        time_us: Receiver clock in microseconds (may restart from 0 after ~71 min).
        rssi_dbm: Signal strength in dBm.
        amplitude: 56 amplitude values, subcarriers -28..-1, 1..28.
    """

    time_us: int
    rssi_dbm: int
    amplitude: tuple[float, ...]


def parse_line(line: str) -> Packet | None:
    """Turn one receiver line into a :class:`Packet`.

    Args:
        line: Text of one line (with or without the newline).

    Returns:
        The packet, or ``None`` if the line is not CSI data (e.g. a ``#`` message).

    Raises:
        ValueError: If the line looks like CSI data but is broken (cut off, garbled).
    """
    line = line.strip()
    if not line.startswith(LINE_PREFIX):
        return None
    fields = line.split(",")
    if len(fields) != N_FIELDS:
        raise ValueError(f"expected {N_FIELDS} fields, got {len(fields)}")
    try:
        return Packet(int(fields[1]), int(fields[2]), tuple(float(x) for x in fields[3:]))
    except ValueError as e:
        raise ValueError(f"not a number in line: {e}") from e


@dataclass
class CaptureStats:
    """Counts shown at the end of a recording."""

    packets: int = 0
    broken_lines: int = 0
    duration_s: float = 0.0


def write_header(out: TextIO, label: str) -> None:
    """Write the comment line and the column names."""
    out.write(f"# {FORMAT_TAG} source=esp32 label={label}\n")
    out.write(",".join([*META_COLUMNS, *AMP_COLUMNS]) + "\n")


def record_lines(
    lines: Iterable[str],
    out: TextIO,
    label: str,
    seconds: float,
    on_message: Callable[[str], None] | None = None,
) -> CaptureStats:
    """Write receiver lines to ``out`` until ``seconds`` of data are recorded.

    Args:
        lines: Lines from the receiver (a serial port, or a list in tests).
        out: Open text file to write the CSV into.
        label: What is happening (e.g. ``walk``); stored in every row.
        seconds: How long to record, measured with the receiver's clock.
        on_message: Called with each ``#`` message from the receiver.

    Returns:
        Counts of good packets and broken lines.
    """
    stats = CaptureStats()
    write_header(out, label)
    first_us: int | None = None
    last_us = 0
    wraps = 0
    for raw in lines:
        if raw.startswith("#"):
            if on_message is not None:
                on_message(raw.rstrip())
            continue
        try:
            pkt = parse_line(raw)
        except ValueError:
            stats.broken_lines += 1
            continue
        if pkt is None:
            continue
        if first_us is None:
            first_us = pkt.time_us
        elif pkt.time_us < last_us:
            wraps += 1  # the receiver's clock restarted from 0
        last_us = pkt.time_us
        t_s = (pkt.time_us + wraps * TIMER_WRAP_US - first_us) / US_PER_S
        amps = ",".join(f"{a:.1f}" for a in pkt.amplitude)
        out.write(f"{t_s:.6f},{pkt.rssi_dbm},{label},{amps}\n")
        stats.packets += 1
        stats.duration_s = t_s
        if t_s >= seconds:
            break
    return stats


def find_port() -> str:
    """Find the USB serial port of the receiver when only one is connected.

    Returns:
        The port name (e.g. ``/dev/ttyUSB0`` or ``COM3``).

    Raises:
        CaptureError: If no port or more than one port is found.
    """
    from serial.tools import list_ports

    ports = [p.device for p in list_ports.comports() if p.vid is not None]
    if not ports:
        raise CaptureError(
            "No USB serial port found. Check: is the receiver plugged in? Is the cable a "
            "data cable (some cables only charge)? / USB ポートが見つかりません。"
            "ケーブルが充電専用でないか確かめてください。"
        )
    if len(ports) > 1:
        raise CaptureError(
            f"Several ports found: {ports}. Choose one with --port. / "
            "ポートが複数あります。--port で受信機のポートを選んでください。"
        )
    return str(ports[0])


def _serial_lines(port: str) -> Iterator[str]:
    """Yield text lines from a serial port; stop with a clear error if nothing arrives."""
    import serial

    try:
        conn = serial.Serial(port, BAUD_RATE, timeout=READ_TIMEOUT_S)
    except serial.SerialException as e:
        raise CaptureError(
            f"Cannot open {port}: {e}. Is another program (Arduino Serial Monitor) using it? / "
            "ほかのプログラム（シリアルモニタなど）が使っていないか確かめてください。"
        ) from e
    with conn:
        last_data = time.monotonic()
        while True:
            raw = conn.readline()
            if raw:
                text = raw.decode("ascii", errors="replace")
                if text.startswith(LINE_PREFIX):
                    last_data = time.monotonic()
                yield text
            elif time.monotonic() - last_data > FIRST_DATA_TIMEOUT_S:
                raise CaptureError(
                    f"No CSI data for {FIRST_DATA_TIMEOUT_S:.0f} s. Check: is the transmitter "
                    "powered on? Are both boards flashed with this repository's firmware? / "
                    "CSI が届きません。送信機の電源と、両方の書き込みを確かめてください。"
                )


def default_path(label: str, out_dir: Path = DEFAULT_OUT_DIR) -> Path:
    """Return ``data/my-recordings/<date>-<time>-<label>.csv``."""
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in label) or "recording"
    return out_dir / f"{datetime.now():%Y%m%d-%H%M%S}-{safe}.csv"


def capture(port: str | None, seconds: float, label: str, path: Path | None = None) -> Path:
    """Record from the receiver and save a CSV file.

    Args:
        port: Serial port, or ``None`` to find it automatically.
        seconds: How long to record.
        label: What is happening (e.g. ``empty``, ``walk``).
        path: Output file; defaults to :func:`default_path`.

    Returns:
        The path of the saved file.

    Raises:
        CaptureError: If the receiver cannot be reached or sends nothing.
        ValueError: If ``seconds`` is not positive.
    """
    if not seconds > 0:
        raise ValueError(f"seconds must be positive, got {seconds}")
    port = port or find_port()
    path = path or default_path(label)
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Recording {seconds:.0f} s from {port} -> {path}  (Ctrl+C to stop early)")
    with path.open("w", encoding="utf-8", newline="") as out:
        try:
            stats = record_lines(_serial_lines(port), out, label, seconds, on_message=print)
        except KeyboardInterrupt:
            print("Stopped. The data recorded so far is saved. / 途中まで保存しました")
            return path
    if stats.packets == 0:
        raise CaptureError("No CSI packets were recorded. / CSI が 1 件も記録されませんでした")
    rate = stats.packets / stats.duration_s if stats.duration_s > 0 else 0.0
    print(f"Done: {stats.packets} packets, {rate:.1f} per second, "
          f"{stats.broken_lines} broken lines skipped.")
    return path
