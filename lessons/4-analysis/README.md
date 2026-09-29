English | [日本語](README.ja.md)

# Level 4: Did something move? — Build a motion detector

## Goal

- Understand why we **normalize** each packet before looking at CSI
- Turn CSI into one **motion number** per second
- Choose a **threshold** from data, then check how often your detector is right
- Find out **what goes wrong** and why

**Time:** about 60–90 minutes
**What you need:** a computer with this repository set up (Level 2). No hardware is needed — we use the simulator. If you built the boards in Level 3, you can use your own recordings too.

Notebook version: [`notebooks/02-motion-detector.ipynb`](../../notebooks/02-motion-detector.ipynb)

---

## 1. Why normalize?

The ESP32 receiver has an automatic "volume knob" (automatic gain control).
It turns the volume up or down **for every packet**, even when nothing in the room moves.
So the raw amplitude jumps around for a reason that has nothing to do with people.

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

With `seed=1`, the raw packet average jumps by about 0.9 (standard deviation), and after
normalizing it is practically 0. The volume knob is gone.

> **Ask your AI**
> "My ESP32 has automatic gain control. Explain with an example about a TV's volume why
> dividing each packet by its average helps. Don't give me code — ask me questions."

## 2. One motion number per second

When nothing moves, each subcarrier stays almost the same. When something moves, it
**wobbles**. We cut the recording into 1-second **windows** and measure the wobble
with the **standard deviation** ("how far values spread from their average").

```python
from csi_lab import simulate
from csi_lab.features import motion_score

for name in ["empty", "still", "walk", "wave"]:
    rec = simulate(name, duration_s=30, seed=1)
    start_s, motion = motion_score(rec)          # one number per 1-second window
    print(f"{name:6s} median={sorted(motion)[len(motion)//2]:.4f}  max={motion.max():.4f}")
```

`window_features` gives you more numbers per window (`motion`, `motion_max`, `spread`,
`rssi_std_db`, `change_rate`). We will use them all in Level 5.

## 3. Choose a threshold from data

A **threshold** is the line between "still" and "moving". Don't guess it — measure it.
Record (or simulate) a time when **nobody moves**, find its biggest motion number, and add
a safety margin.

```python
from csi_lab import simulate
from csi_lab.features import motion_score

_, still_motion = motion_score(simulate("still", duration_s=30, seed=1))
threshold = still_motion.max() * 1.2      # 20 % safety margin
print("threshold =", round(threshold, 3))
```

With `seed=1` the biggest "still" value was about 0.043, so the threshold becomes about 0.051.

## 4. Test it on a story

Now try the detector on a recording where the situation **changes**:
nobody → walking → sitting still → walking → waving → nobody.
This is the same story as `data/samples/story.csv` (made by `uv run csi-lab samples`).

```python
import numpy as np
from csi_lab import simulate_sequence
from csi_lab.features import window_features, detect_motion

story = simulate_sequence(
    [("empty", 20), ("walk", 20), ("still", 20), ("walk", 10), ("wave", 20), ("empty", 10)],
    seed=100,
)
w = window_features(story)
motion = w.features[:, w.names.index("motion")]
predicted = detect_motion(motion, threshold=0.051)       # True = "moving"
truth = np.isin(w.labels, ["walk", "wave"])              # what really happened

print("accuracy:", (predicted == truth).mean())
for label in ["empty", "still", "walk", "wave"]:
    sel = w.labels == label
    print(f"{label:6s} windows={sel.sum():3d}  said 'moving' in {predicted[sel].mean():.0%}")
```

**Accuracy** = (number of right answers) ÷ (number of windows). We compute it by hand with
NumPy so you can see there is no magic.

With these seeds we got an accuracy of **0.87** (87 of 100 windows right). Look at each label:

| label | windows | said "moving" |
|---|---|---|
| empty | 30 | 0 % |
| walk  | 30 | 100 % |
| still | 20 | 5 % |
| wave  | 20 | 40 % |

(Simulator, `seed=100`, threshold 0.051.)

## 5. What goes wrong — and why

- **"still" sometimes looks like moving.** People sitting "still" shift their posture now
  and then. The simulator includes these small posture changes on purpose, because real
  people do it too. Is that a mistake of the detector — or did something really move?
- **"wave" is often missed.** A hand is small, so its echo is small. The motion number
  for waving is only a little bigger than for sitting still.
- **One threshold can't fit everything.** If you lower the threshold, you catch more
  waving but also more posture changes. Try it! This trade-off appears in almost every
  detector in the world (smoke alarms, spam filters, ...).

> **Ask your AI**
> "My motion detector says 'moving' when someone only shifts in their chair. Give me three
> ideas to fix this, and for each one tell me what new mistake it might cause."

## 6. Bonus: can Wi-Fi see breathing?

Breathing moves the chest only a few millimeters, slowly and regularly. A **Fourier
transform** splits a signal into its rhythms, and `breathing_rate_bpm` looks for the
strongest slow rhythm.

```python
from csi_lab import simulate
from csi_lab.features import breathing_rate_bpm

rec = simulate("breathe", duration_s=60, seed=3)
print("breaths per minute:", round(breathing_rate_bpm(rec), 1))
```

The simulated person breathes 15 times per minute, and the function finds 15.0 (`seed=3`).

**Be careful:**
- This works nicely **in the simulator**. In a real room it is much harder: people move a
  little, other people and machines move, and the signal is noisier.
- Try it on `simulate("still", 60, seed=2)` — nobody is breathing in a regular way there,
  but the function still returns a number. A tool always gives an answer; that does not
  mean the answer is true.
- This is **not a medical device**. Never use it to check someone's health.

## Check yourself

1. Why do we divide each packet by its average?
2. What does a big standard deviation in a 1-second window mean?
3. Why should the threshold come from a "nobody moves" recording, not from a guess?
4. Your detector gets 87 % right. Is that good? What else do you want to know?

<details>
<summary>Answers</summary>

1. The receiver's automatic gain changes the volume for every packet. Dividing by the average removes that, so only changes caused by the room remain.
2. The amplitude wobbled a lot in that second — something probably moved.
3. The data tells us how big "still" really is in *this* room with *this* hardware. A guess might be far off.
4. It depends! Look at each label: which situations are missed? 87 % could hide a class that is almost always wrong (like "wave" here). Also: it was tested in the simulator, not a real room.

</details>

## Next

➡ [Level 5: Your first machine learning](../5-machine-learning/README.md) — let the computer find the rules.
