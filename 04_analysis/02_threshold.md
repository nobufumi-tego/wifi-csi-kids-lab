English | [日本語](02_threshold.ja.md)

# 4-2. Deciding with a threshold — and counting right answers

A **threshold** is the line between "still" and "moving". Don't guess it: measure it.
Then test your detector on a recording where the situation changes.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb).
> New to the terminal? → [0-2. Terminal and uv](../start_here/02_terminal_and_uv.md)

## 1. Choose the threshold from data

Record (or simulate) a time when **nobody moves**, find its biggest motion number, and
add a safety margin.

```python
from csi_lab import simulate
from csi_lab.features import motion_score

_, still_motion = motion_score(simulate("still", duration_s=30, seed=1))
threshold = still_motion.max() * 1.2      # 20 % safety margin
print("threshold =", round(threshold, 3))
```

With `seed=1` the biggest "still" value was about 0.043, so the threshold becomes about
0.051.

## 2. Test it on a story

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

## 3. Accuracy

$$
\text{accuracy} = \frac{\text{number of right answers}}{\text{number of windows}}
$$

We compute it by hand with NumPy, so you can see there is no magic.

With these seeds we got an accuracy of **0.87** (87 of 100 windows right). Look at each
label:

| label | windows | said "moving" |
|---|---|---|
| empty | 30 | 0 % |
| walk  | 30 | 100 % |
| still | 20 | 5 % |
| wave  | 20 | 40 % |

(Simulator, `seed=100`, threshold 0.051.)

One number (87 %) hides a lot. "walk" is always found, but "wave" is found only 40 % of
the time. **Always look at each label**, not only the total.

> 🤖 **Ask your AI**
> - "My detector is right 87 % of the time. Ask me questions to find out whether that is
>   good or not."
> - "Why is it better to choose a threshold from data than to guess it?"

## Check yourself

1. Why should the threshold come from a "nobody moves" recording, not from a guess?
2. What is accuracy?
3. Your detector gets 87 % right. Is that good? What else do you want to know?

<details><summary>Answers</summary>

1. The data tells us how big "still" really is in *this* room with *this* hardware. A
   guess might be far off.
2. The number of right answers divided by the number of windows.
3. It depends! Look at each label: which situations are missed? 87 % can hide a class
   that is often wrong (like "wave" here). Also, it was tested in the simulator, not in
   a real room.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- How noise spreads: [正規分布（雑音の広がり方）](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/02_distributions.md)
- Is a difference real or chance?: [その差は本物か偶然か（仮説検定）](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/07_hypothesis_testing.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [4-1. A number for motion](01_motion_number.md) | [Chapter 4](README.md) | [Home](../README.md) | [4-3. What goes wrong](03_what_goes_wrong.md) |
