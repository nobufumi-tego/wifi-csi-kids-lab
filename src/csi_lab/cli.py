"""Command line tool: ``uv run csi-lab <command>``.

コマンドで使う入口。``uv run csi-lab --help`` で使い方が出る。

Commands:
    samples   make pretend recordings in data/samples/ (no hardware needed)
    show      draw a recording and save a PNG picture next to it
    ports     list USB serial ports (to find your receiver)
    capture   record from your ESP32 receiver
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from csi_lab.recording import load_csv, save_csv
from csi_lab.simulate import SCENARIOS, simulate, simulate_sequence

SAMPLES_DIR: Path = Path("data") / "samples"
SAMPLE_SECONDS: float = 30.0
#: The "story" sample: situations change, handy for machine learning.
STORY_STEPS: list[tuple[str, float]] = [
    ("empty", 20.0), ("walk", 20.0), ("still", 20.0), ("walk", 10.0),
    ("wave", 20.0), ("empty", 10.0),
]


def cmd_samples(args: argparse.Namespace) -> int:
    """Write one file per scenario plus a 'story' file with changing situations."""
    out = Path(args.out)
    for i, name in enumerate(SCENARIOS):
        path = save_csv(simulate(name, SAMPLE_SECONDS, seed=args.seed + i), out / f"{name}.csv")
        print(f"wrote {path}  ({SCENARIOS[name]})")
    story = simulate_sequence(STORY_STEPS, seed=args.seed + 100)
    print(f"wrote {save_csv(story, out / 'story.csv')}  (situations change over time)")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Draw a recording and save it as ``<file>.png``."""
    import matplotlib

    matplotlib.use("Agg")
    from csi_lab.plot import plot_overview

    path = Path(args.file)
    rec = load_csv(path)
    fig = plot_overview(rec, title=path.name)
    png = path.with_suffix(".png")
    fig.savefig(png, dpi=100)
    print(f"{rec.n_packets} packets, {rec.duration_s:.1f} s, {rec.rate_hz:.1f} per second")
    print(f"saved picture: {png}")
    return 0


def cmd_ports(args: argparse.Namespace) -> int:
    """Print the USB serial ports."""
    from serial.tools import list_ports

    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports found. / シリアルポートが見つかりません")
    for p in ports:
        print(f"{p.device}\t{p.description}")
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    """Record from the ESP32 receiver."""
    from csi_lab.capture import CaptureError, capture

    try:
        capture(args.port, args.seconds, args.label, Path(args.out) if args.out else None)
    except (CaptureError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser (separate so tests can use it)."""
    parser = argparse.ArgumentParser(prog="csi-lab", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("samples", help="make pretend recordings (no hardware needed)")
    p.add_argument("--out", default=str(SAMPLES_DIR), help="folder to write into")
    p.add_argument("--seed", type=int, default=0, help="change for different samples")
    p.set_defaults(func=cmd_samples)

    p = sub.add_parser("show", help="draw a recording and save a PNG")
    p.add_argument("file", help="a .csv recording")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("ports", help="list USB serial ports")
    p.set_defaults(func=cmd_ports)

    p = sub.add_parser("capture", help="record from your ESP32 receiver")
    p.add_argument("--label", required=True, help="what is happening, e.g. empty / walk")
    p.add_argument("--seconds", type=float, default=30.0, help="how long to record")
    p.add_argument("--port", default=None, help="serial port (found automatically if only one)")
    p.add_argument("--out", default=None, help="output .csv (default: data/my-recordings/...)")
    p.set_defaults(func=cmd_capture)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line tool.

    Args:
        argv: Arguments (defaults to the real command line).

    Returns:
        Exit code: 0 = success.
    """
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
