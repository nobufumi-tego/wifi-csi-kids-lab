"""Quick pictures of a recording.

記録をすぐに絵にするための関数。
"""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from csi_lab.features import motion_score, normalize_per_packet
from csi_lab.recording import SUBCARRIERS, Recording

DEFAULT_SUBCARRIERS: tuple[int, ...] = (-20, -5, 10, 25)


def plot_overview(rec: Recording, title: str | None = None) -> Figure:
    """Draw three panels: a heat map, the motion number, and the signal strength.

    - Top: every subcarrier over time (color = wave size, after removing the
      receiver's automatic volume changes). Stripes = something moved.
    - Middle: motion number for each 1-second window.
    - Bottom: signal strength (RSSI).

    Args:
        rec: The recording to draw.
        title: Text above the picture. Defaults to the file's scenario/source.

    Returns:
        The matplotlib figure (call ``fig.savefig("name.png")`` to save it).
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True,
                             gridspec_kw={"height_ratios": [3, 1.3, 1]})
    norm = normalize_per_packet(rec.amplitude)
    image = axes[0].imshow(
        norm.T,
        aspect="auto",
        origin="lower",
        extent=(rec.time_s[0], rec.time_s[-1], SUBCARRIERS[0], SUBCARRIERS[-1]),
        cmap="viridis",
    )
    axes[0].set_ylabel("subcarrier")
    fig.colorbar(image, ax=axes[0], label="relative amplitude")

    start_s, motion = motion_score(rec)
    axes[1].step(start_s, motion, where="post", color="tab:orange")
    axes[1].set_ylabel("motion")

    axes[2].plot(rec.time_s, rec.rssi_dbm, lw=0.8, color="tab:blue")
    axes[2].set_ylabel("RSSI [dBm]")
    axes[2].set_xlabel("time [s]")

    # Shade parts with different labels so you can compare them
    changes = np.flatnonzero(rec.labels[1:] != rec.labels[:-1]) + 1
    bounds = [0, *changes.tolist(), rec.n_packets]
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1] - 1
        axes[1].axvspan(rec.time_s[a], rec.time_s[b], alpha=0.08 * (i % 2 + 1), color="gray")
        axes[1].text(rec.time_s[a], axes[1].get_ylim()[1], f" {rec.labels[a]}",
                     va="top", fontsize=9)
    fig.suptitle(title or rec.info.get("scenario", rec.info.get("label", "recording")))
    fig.tight_layout()
    return fig


def plot_subcarriers(rec: Recording, subcarriers: Sequence[int] = DEFAULT_SUBCARRIERS) -> Figure:
    """Draw the raw amplitude of a few subcarriers over time.

    Args:
        rec: The recording.
        subcarriers: Subcarrier numbers to draw (-28..-1, 1..28).

    Returns:
        The matplotlib figure.

    Raises:
        ValueError: If a subcarrier number does not exist.
    """
    bad = [k for k in subcarriers if k not in SUBCARRIERS]
    if bad:
        raise ValueError(f"no such subcarrier: {bad}; use -28..-1 or 1..28")
    fig, ax = plt.subplots(figsize=(10, 4))
    for k in subcarriers:
        ax.plot(rec.time_s, rec.amplitude[:, SUBCARRIERS.index(k)], lw=0.7, label=f"sc {k}")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("amplitude")
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig
