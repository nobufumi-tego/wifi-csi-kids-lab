English | [日本語](01_motion_number.ja.md)

# 4-1. A number for motion — normalize, then measure the wobble

When nothing moves, each subcarrier stays almost the same. When something moves, it
**wobbles**. On this page you turn that wobble into one number per second.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb).
> New to the terminal? → [0-2. Terminal and uv](../start_here/02_terminal_and_uv.md)

## 1. First, normalize

The ESP32 receiver has an automatic "volume knob" (automatic gain control). It turns the
volume up or down **for every packet**, even when nothing in the room moves (see
[2-4. Automatic gain](../02_csi_basics/04_automatic_gain.md)).

The trick: divide every packet by its own average. Then each packet averages to 1, and
only the **shape** across subcarriers is left. That shape is what people change.

```python
from csi_lab import simulate
from csi_lab.features import normalize_per_packet

rec = simulate("still", duration_s=30, seed=1)
raw_avg = rec.amplitude.mean(axis=1)                    # average of each packet
norm_avg = normalize_per_packet(rec.amplitude).mean(axis=1)

print("raw:  how much the packet average jumps =", raw_avg.std())
print("norm: how much the packet average jumps =", norm_avg.std())
```

With `seed=1`, the raw packet average jumps by about 0.89 (standard deviation), and after
normalizing it is practically 0 (about $10^{-16}$). The volume knob is gone.

## 2. Cut into windows, measure the wobble

We cut the recording into 1-second pieces called **windows**. In each window we measure
how much each subcarrier wobbles with the **standard deviation**: how far the values
spread from their average. For values $x_1, \dots, x_n$ with average $\bar{x}$:

$$
\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2}
$$

Big $\sigma$ = big wobble. The **motion number** of a window is the average of $\sigma$
over all 56 subcarriers.

```python
import numpy as np
from csi_lab import simulate
from csi_lab.features import motion_score

for name in ["empty", "still", "walk", "wave"]:
    rec = simulate(name, duration_s=30, seed=1)
    start_s, motion = motion_score(rec)          # one number per 1-second window
    print(f"{name:6s} median={np.median(motion):.4f}  max={motion.max():.4f}")
```

What we got (simulator, `seed=1`, 30 s each):

| scenario | median | max |
|---|---|---|
| empty | 0.0305 | 0.0311 |
| still | 0.0302 | 0.0427 |
| walk  | 0.0935 | 0.1385 |
| wave  | 0.0385 | 0.0647 |

Walking wobbles about 3 times as much as sitting still. Waving a hand is only a little
bigger than sitting still.

## 3. More numbers per window

`window_features` gives five numbers for every window. Chapter 5 uses them all.

| name | meaning |
|---|---|
| `motion` | average wobble over subcarriers (the motion number above) |
| `motion_max` | the wobble of the subcarrier that wobbles most |
| `spread` | how different the subcarriers are from each other (the room's "fingerprint") |
| `rssi_std_db` | wobble of the signal strength (RSSI) |
| `change_rate` | how fast the amplitude changes from one packet to the next |

```python
from csi_lab import simulate
from csi_lab.features import window_features

w = window_features(simulate("walk", duration_s=10, seed=1))
print(w.names)
print(w.features.shape)      # (windows, 5)
print(w.labels[:3])
```

> 🤖 **Ask your AI**
> - "My ESP32 has automatic gain control. Explain with a TV's volume why dividing each
>   packet by its average helps. Don't give me code — ask me questions."
> - "What is a standard deviation? Use the heights of my classmates as an example."

## Check yourself

1. Why do we divide each packet by its average?
2. What does a big standard deviation in a 1-second window mean?
3. In the table, which scenario is hardest to tell apart from "still"?

<details><summary>Answers</summary>

1. The receiver's automatic gain changes the volume for every packet. Dividing by the
   average removes that, so only changes caused by the room remain.
2. The amplitude wobbled a lot in that second, so something probably moved.
3. "wave": its motion number is only a little bigger than "still".

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Standard deviation: [標準偏差（記述統計）](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/05_descriptive_stats.md)
- Variance: [分散](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/03_expectation_variance.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Chapter 4](README.md) | [Chapter 4](README.md) | [Home](../README.md) | [4-2. Threshold](02_threshold.md) |
