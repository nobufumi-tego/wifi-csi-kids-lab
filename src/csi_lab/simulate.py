r"""Make pretend (synthetic) CSI recordings, no hardware needed.

ハードウェアがなくても試せるように、部屋の中の電波をまねして CSI の記録を作る。

The model (top view, in meters)::

        y
        ^        person (moves)
        |          o
        |         / \\
     S  +--------+---+--------> x
    (0,0)       1.5        R (3,0)

- The transmitter ``S`` and the receiver ``R`` are 3 m apart.
- The wave reaches ``R`` along several paths: straight (line of sight), bounced
  off walls and furniture (fixed), and bounced off the person (changes when the
  person moves). The paths add up, sometimes helping and sometimes canceling each
  other. That mix is different on every subcarrier, which is what CSI shows.
- When the person stands on the straight line, their body blocks part of it.
- The receiver behaves like an ESP32: it changes its volume knob (automatic gain)
  every packet, rounds numbers to integers, and sometimes misses packets.

It is a simplified model for learning. Real rooms are messier, so results from
real hardware will be noisier than these. / 学習用の単純なモデル。本物の部屋はもっと複雑。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from csi_lab.recording import SUBCARRIER_SPACING_HZ, SUBCARRIERS, Recording

# ---- physics / 物理 -----------------------------------------------------------
SPEED_OF_LIGHT_M_S: float = 299_792_458.0
CENTER_FREQ_HZ: float = 2.462e9  # Wi-Fi channel 11 / チャンネル 11 の中心周波数
TX_POS_M: tuple[float, float] = (0.0, 0.0)
RX_POS_M: tuple[float, float] = (3.0, 0.0)
MIDPOINT_X_M: float = 1.5

# ---- room / 部屋 ---------------------------------------------------------------
N_WALL_PATHS: int = 5
WALL_EXTRA_LEN_M: tuple[float, float] = (0.5, 8.0)  # extra length of bounced paths
WALL_GAIN: tuple[float, float] = (0.15, 0.5)  # size of bounced waves (straight = 1)

# ---- person / 人 --------------------------------------------------------------
BODY_GAIN: float = 0.2  # size of the wave bounced off a body (at 3 m total path)
HAND_GAIN: float = 0.1  # a hand is small, so its echo is small
BLOCK_DEPTH: float = 0.6  # how much a body on the line weakens the straight wave
BLOCK_WIDTH_M: float = 0.25  # how close to the line the body must be to block
WALK_SPEED_M_S: float = 1.0
WALK_HALF_RANGE_M: float = 2.0  # walks from y=-2 m to y=+2 m and back
STILL_Y_M: float = 1.2
SWAY_M: float = 0.004  # tiny unconscious movement while sitting still
SWAY_HZ: float = 0.15
FIDGET_EVERY_S: float = 20.0  # on average, one small posture change every 20 s
FIDGET_M: tuple[float, float] = (0.02, 0.06)  # how far the body shifts
FIDGET_S: float = 1.5  # how long a posture change takes
BREATHE_Y_M: float = 0.6
CHEST_M: float = 0.003  # chest moves about 3 mm when breathing
BREATHE_HZ: float = 0.25  # 15 breaths per minute
HAND_Y_M: float = 0.7
HAND_SWING_M: float = 0.15
WAVE_HZ: float = 1.2

# ---- receiver (ESP32-like) / 受信機 --------------------------------------------
TARGET_LEVEL: float = 30.0  # automatic gain keeps the average near this value
GAIN_WOBBLE: float = 0.03  # automatic gain is not perfect (+-3 %)
NOISE_LEVEL: float = 0.04  # electrical noise, relative to the signal
RSSI_AT_REFERENCE_DBM: float = -50.0
RSSI_NOISE_DB: float = 1.0
TIMING_JITTER_S: float = 0.001
LOSS_RATE: float = 0.01  # 1 % of packets are missed

DEFAULT_RATE_HZ: float = 100.0
DEFAULT_ROOM_SEED: int = 7


@dataclass(frozen=True)
class _Reflectors:
    """Moving echoes for every packet.

    Attributes:
        length_m: Path length of each moving echo, shape ``(packets, 2)`` (body, hand).
        gain: Size of each moving echo, shape ``(packets, 2)``; 0 = not there.
        los_factor: How much of the straight wave gets through, shape ``(packets,)``.
    """

    length_m: NDArray[np.float64]
    gain: NDArray[np.float64]
    los_factor: NDArray[np.float64]


def _path_via(y_m: NDArray[np.float64]) -> NDArray[np.float64]:
    """Length of the path S -> point (1.5, y) -> R in meters."""
    to_point = np.hypot(MIDPOINT_X_M - TX_POS_M[0], y_m - TX_POS_M[1])
    from_point = np.hypot(RX_POS_M[0] - MIDPOINT_X_M, RX_POS_M[1] - y_m)
    return np.asarray(to_point + from_point, dtype=np.float64)


def _body(y_m: NDArray[np.float64], gain: float) -> tuple[NDArray[np.float64], ...]:
    """Echo length, echo size and blocking for a body at (1.5, y)."""
    length = _path_via(y_m)
    los_length = RX_POS_M[0] - TX_POS_M[0]
    size = gain * los_length / length * np.ones_like(y_m)  # farther = weaker
    los = 1.0 - BLOCK_DEPTH * np.exp(-((y_m / BLOCK_WIDTH_M) ** 2))
    return length, size, los


def _scenario_empty(t: NDArray[np.float64], rng: np.random.Generator) -> _Reflectors:
    n = t.size
    return _Reflectors(np.ones((n, 2)), np.zeros((n, 2)), np.ones(n))


def _sway(t: NDArray[np.float64], rng: np.random.Generator) -> NDArray[np.float64]:
    """Small movements of someone "sitting still": slow sway plus a few posture changes."""
    phase = rng.uniform(0, 2 * np.pi)
    drift = np.cumsum(rng.normal(0.0, SWAY_M / 50, t.size))
    y = SWAY_M * np.sin(2 * np.pi * SWAY_HZ * t + phase) + drift
    duration = float(t[-1] - t[0]) if t.size > 1 else 0.0
    for _ in range(rng.poisson(duration / FIDGET_EVERY_S)):
        start = rng.uniform(t[0], t[-1])
        shift = rng.uniform(*FIDGET_M) * rng.choice([-1.0, 1.0])
        # a smooth step: the body moves to a new place and stays there
        y += shift / (1 + np.exp(-(t - start) / (FIDGET_S / 6)))
    return np.asarray(y, dtype=np.float64)


def _still_body(t: NDArray[np.float64], rng: np.random.Generator, y0: float) -> _Reflectors:
    length, size, los = _body(y0 + _sway(t, rng), BODY_GAIN)
    n = t.size
    return _Reflectors(
        np.stack([length, np.ones(n)], axis=1), np.stack([size, np.zeros(n)], axis=1), los
    )


def _scenario_still(t: NDArray[np.float64], rng: np.random.Generator) -> _Reflectors:
    return _still_body(t, rng, STILL_Y_M)


def _scenario_walk(t: NDArray[np.float64], rng: np.random.Generator) -> _Reflectors:
    period_s = 4 * WALK_HALF_RANGE_M / WALK_SPEED_M_S
    phase = rng.uniform(0, 1)
    frac = ((t - t[0]) / period_s + phase) % 1.0
    tri = 4 * np.abs(frac - 0.5) - 1  # triangle wave between -1 and +1
    y = WALK_HALF_RANGE_M * tri + rng.normal(0, 0.01, t.size)
    length, size, los = _body(y, BODY_GAIN)
    n = t.size
    return _Reflectors(
        np.stack([length, np.ones(n)], axis=1), np.stack([size, np.zeros(n)], axis=1), los
    )


def _scenario_breathe(t: NDArray[np.float64], rng: np.random.Generator) -> _Reflectors:
    phase = rng.uniform(0, 2 * np.pi)
    chest = CHEST_M * np.sin(2 * np.pi * BREATHE_HZ * t + phase)
    y = BREATHE_Y_M + chest + _sway(t, rng) / 4
    length, size, los = _body(y, BODY_GAIN)
    n = t.size
    return _Reflectors(
        np.stack([length, np.ones(n)], axis=1), np.stack([size, np.zeros(n)], axis=1), los
    )


def _scenario_wave(t: NDArray[np.float64], rng: np.random.Generator) -> _Reflectors:
    body = _still_body(t, rng, STILL_Y_M)
    phase = rng.uniform(0, 2 * np.pi)
    hand_y = HAND_Y_M + HAND_SWING_M * np.sin(2 * np.pi * WAVE_HZ * t + phase)
    hand_len, hand_size, _ = _body(hand_y, HAND_GAIN)
    length = body.length_m.copy()
    gain = body.gain.copy()
    length[:, 1] = hand_len
    gain[:, 1] = hand_size
    return _Reflectors(length, gain, body.los_factor)


_Scenario = Callable[[NDArray[np.float64], np.random.Generator], _Reflectors]

_SCENARIO_FUNCS: dict[str, _Scenario] = {
    "empty": _scenario_empty,
    "still": _scenario_still,
    "walk": _scenario_walk,
    "breathe": _scenario_breathe,
    "wave": _scenario_wave,
}

#: Scenario names and what they mean. / 場面の名前と意味
SCENARIOS: dict[str, str] = {
    "empty": "nobody in the room / 部屋にだれもいない",
    "still": "a person sits still, away from the line / 人が線から離れて静かに座っている",
    "walk": "a person walks back and forth across the line / 人が線を横切って往復する",
    "breathe": "a person sits near the line and breathes / 人が線の近くに座って呼吸する",
    "wave": "a person sits and waves a hand / 人が座って手をふる",
}


def _frequencies_hz() -> NDArray[np.float64]:
    """Frequency of each subcarrier in Hz."""
    return CENTER_FREQ_HZ + np.array(SUBCARRIERS, dtype=np.float64) * SUBCARRIER_SPACING_HZ


def _room(room_seed: int) -> tuple[NDArray[np.float64], NDArray[np.complex128]]:
    """Fixed paths of the room: straight path first, then wall/furniture bounces."""
    rng = np.random.default_rng(room_seed)
    los_m = RX_POS_M[0] - TX_POS_M[0]
    lengths = np.concatenate([[los_m], los_m + rng.uniform(*WALL_EXTRA_LEN_M, N_WALL_PATHS)])
    sizes = np.concatenate([[1.0], rng.uniform(*WALL_GAIN, N_WALL_PATHS)])
    phases = np.concatenate([[0.0], rng.uniform(0, 2 * np.pi, N_WALL_PATHS)])
    return lengths, (sizes * np.exp(1j * phases)).astype(np.complex128)


def _packet_times(
    duration_s: float, rate_hz: float, rng: np.random.Generator
) -> NDArray[np.float64]:
    """Packet arrival times with small timing jitter and a few missed packets."""
    nominal = np.arange(0.0, duration_s, 1.0 / rate_hz)
    jitter = rng.normal(0.0, TIMING_JITTER_S, nominal.size)
    t = np.clip(nominal + jitter, 0.0, None)
    keep = rng.random(nominal.size) >= LOSS_RATE
    keep[0] = True
    return np.sort(t[keep])


def _check_args(duration_s: float, rate_hz: float) -> None:
    if not duration_s > 0:
        raise ValueError(f"duration_s must be positive, got {duration_s}")
    if not rate_hz > 0:
        raise ValueError(f"rate_hz must be positive, got {rate_hz}")


def simulate_sequence(
    steps: list[tuple[str, float]],
    rate_hz: float = DEFAULT_RATE_HZ,
    seed: int = 0,
    room_seed: int = DEFAULT_ROOM_SEED,
) -> Recording:
    """Make one recording where the situation changes over time.

    Example: ``simulate_sequence([("empty", 10), ("walk", 10), ("still", 10)])``
    makes 30 seconds: nobody, then walking, then sitting still. Each packet gets
    the label of its step, which is handy for machine learning.

    Args:
        steps: List of ``(scenario, seconds)``. Scenario names are in :data:`SCENARIOS`.
        rate_hz: Packets per second (the ESP32 transmitter sends 100).
        seed: Change this to get a different but similar recording.
        room_seed: Change this to move the furniture (a different room).

    Returns:
        The pretend recording.

    Raises:
        ValueError: If a scenario name is unknown or a length is not positive.
    """
    if not steps:
        raise ValueError("steps must not be empty")
    for name, seconds in steps:
        if name not in _SCENARIO_FUNCS:
            raise ValueError(f"unknown scenario {name!r}; choose from {sorted(SCENARIOS)}")
        _check_args(seconds, rate_hz)

    rng = np.random.default_rng(seed)
    wall_len, wall_gain = _room(room_seed)
    freqs = _frequencies_hz()
    wave_number = 2 * np.pi * freqs / SPEED_OF_LIGHT_M_S  # radians per meter

    times, labels, echoes = [], [], []
    start = 0.0
    for name, seconds in steps:
        t = start + _packet_times(seconds, rate_hz, rng)
        times.append(t)
        labels.append(np.full(t.size, name))
        echoes.append(_SCENARIO_FUNCS[name](t, rng))
        start += seconds
    t_all = np.concatenate(times)
    length = np.concatenate([e.length_m for e in echoes])
    gain = np.concatenate([e.gain for e in echoes])
    los = np.concatenate([e.los_factor for e in echoes])

    # Add up every path on every subcarrier: shape (packets, subcarriers)
    fixed_gain = np.tile(wall_gain, (t_all.size, 1))
    fixed_gain[:, 0] *= los  # the body may block the straight path
    h = (fixed_gain[:, :, None] * np.exp(-1j * wall_len[None, :, None] * wave_number)).sum(axis=1)
    h += (gain[:, :, None] * np.exp(-1j * length[:, :, None] * wave_number)).sum(axis=1)

    level = np.sqrt(np.mean(np.abs(h) ** 2, axis=1))  # strength of each packet
    noise = rng.normal(size=h.shape) + 1j * rng.normal(size=h.shape)
    h += NOISE_LEVEL * level[:, None] * noise / np.sqrt(2)

    # Automatic gain: scale every packet to about the same size, like the ESP32
    agc = TARGET_LEVEL / level * (1 + GAIN_WOBBLE * rng.normal(size=level.size))
    scaled = h * agc[:, None]
    scaled = np.round(scaled.real) + 1j * np.round(scaled.imag)  # ESP32 reports integers
    amplitude = np.abs(scaled)

    rssi = RSSI_AT_REFERENCE_DBM + 20 * np.log10(level) + rng.normal(0, RSSI_NOISE_DB, level.size)
    info = {
        "source": "simulated",
        "scenario": "+".join(name for name, _ in steps),
        "seed": str(seed),
        "room_seed": str(room_seed),
    }
    return Recording(
        time_s=t_all,
        rssi_dbm=np.round(rssi),
        amplitude=amplitude,
        labels=np.concatenate(labels).astype(np.str_),
        info=info,
    )


def simulate(
    scenario: str,
    duration_s: float = 30.0,
    rate_hz: float = DEFAULT_RATE_HZ,
    seed: int = 0,
    room_seed: int = DEFAULT_ROOM_SEED,
) -> Recording:
    """Make a pretend recording of one situation.

    Args:
        scenario: One of :data:`SCENARIOS` (``"empty"``, ``"still"``, ``"walk"``,
            ``"breathe"``, ``"wave"``).
        duration_s: Length in seconds.
        rate_hz: Packets per second.
        seed: Change this to get a different but similar recording.
        room_seed: Change this to move the furniture (a different room).

    Returns:
        The pretend recording.
    """
    return simulate_sequence([(scenario, duration_s)], rate_hz, seed, room_seed)
