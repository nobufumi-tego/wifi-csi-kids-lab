English | [日本語](03_what_goes_wrong.ja.md)

# 4-3. What goes wrong — and why

Our detector from [4-2](02_threshold.md) was right 87 % of the time. On this page you
look at the other 13 % and think about why.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb).
> New to the terminal? → [0-2. Terminal and uv](../start_here/02_terminal_and_uv.md)

## 1. "still" sometimes looks like moving

People sitting "still" shift their posture now and then. The simulator includes these
small posture changes on purpose, because real people do it too. In the story from 4-2,
1 of the 20 "still" windows (5 %) was called "moving".

Is that a mistake of the detector, or did something really move? The label says "still",
but the body did move a little. **Labels are written by people, and they can be too
simple.**

## 2. "wave" is often missed

A hand is small, so its echo is small. The motion number for waving (median 0.0385 with
`seed=1`) is only a little bigger than for sitting still (0.0302). In the story, only
40 % of the "wave" windows were called "moving".

## 3. One threshold cannot fit everything

If you lower the threshold, you catch more waving but also more posture changes. If you
raise it, you miss more waving. Try it:

```python
import numpy as np
from csi_lab import simulate, simulate_sequence
from csi_lab.features import motion_score, window_features, detect_motion

_, still_motion = motion_score(simulate("still", duration_s=30, seed=1))
story = simulate_sequence(
    [("empty", 20), ("walk", 20), ("still", 20), ("walk", 10), ("wave", 20), ("empty", 10)],
    seed=100,
)
w = window_features(story)
motion = w.features[:, w.names.index("motion")]
truth = np.isin(w.labels, ["walk", "wave"])

for margin in [1.0, 1.2, 1.5]:
    predicted = detect_motion(motion, threshold=still_motion.max() * margin)
    wave = predicted[w.labels == "wave"].mean()
    print(f"margin {margin}: accuracy={(predicted == truth).mean():.2f}  wave found={wave:.0%}")
```

What we got (simulator, same seeds as 4-2):

| margin | accuracy | "wave" found |
|---|---|---|
| 1.0 | 0.88 | 45 % |
| 1.2 | 0.87 | 40 % |
| 1.5 | 0.86 | 35 % |

This trade-off appears in almost every detector in the world: smoke alarms, spam
filters, and many more.

## 4. Real rooms are harder

The simulator is a simple model of a room. In a real room:

- other people, pets, fans, and curtains move
- the automatic gain is less tidy, and the signal is noisier
- moving the boards even a little changes everything

So numbers from your own recordings will be different, and usually the gap between
"still" and "walk" is smaller. That is not a failure; it is what you find out by
measuring.

> 🤖 **Ask your AI**
> - "My motion detector says 'moving' when someone only shifts in their chair. Give me
>   three ideas to fix this, and for each one tell me what new mistake it might cause."
> - "Why can a smoke alarm never be perfect? Connect it to my motion detector."

## Check yourself

1. Why is "wave" harder to detect than "walk"?
2. What happens when you lower the threshold?
3. Why will your real recordings probably look different from the simulator?

<details><summary>Answers</summary>

1. A hand is small, so its echo is small and the wobble is only a little bigger than
   sitting still.
2. You find more small movements (like waving), but also more posture changes are called
   "moving".
3. Real rooms have more things that move, more noise, and are more complicated than the
   simple model.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [4-2. Threshold](02_threshold.md) | [Chapter 4](README.md) | [Home](../README.md) | [4-4. Breathing](04_breathing.md) |
