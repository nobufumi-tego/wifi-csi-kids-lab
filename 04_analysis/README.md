English | [日本語](README.ja.md)

# Chapter 4: Find motion — build a motion detector

Turn CSI into one **motion number** per second, choose a **threshold** from data, check
how often your detector is right, and find out **what goes wrong** and why.

## What you will be able to do

- Explain why we **normalize** each packet before looking at CSI
- Compute a motion number with a 1-second window and the standard deviation
- Choose a threshold from a "nobody moves" recording and measure accuracy
- Tell which situations a simple detector misses, and why
- Find a slow, regular rhythm (breathing) in the simulator, and know its limits

**Who:** junior-high students and up (中学生〜), or younger learners with help ·
**Time:** about 60–90 minutes

**What you need:** a computer with this lab set up. No hardware is needed: we use the
simulator. If you built the boards in [Chapter 3](../03_build/README.md), you can use
your own recordings too (`from csi_lab import load_csv`).

## Pages

| # | Page | What you learn |
|---|---|---|
| 4-1 | [`01_motion_number.md`](01_motion_number.md) | Normalize, cut into windows, measure the wobble |
| 4-2 | [`02_threshold.md`](02_threshold.md) | Choose a threshold from data and count right answers |
| 4-3 | [`03_what_goes_wrong.md`](03_what_goes_wrong.md) | Posture changes, small hand waves, real rooms |
| 4-4 | [`04_breathing.md`](04_breathing.md) | Bonus: can Wi-Fi find a breathing rhythm? |

## Notebooks

| Page | Notebook |
|---|---|
| 4-1 to 4-4 | [`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb) |

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [3-4. Troubleshooting](../03_build/04_troubleshooting.md) | [Chapter 4](README.md) | [Home](../README.md) | [4-1. A number for motion](01_motion_number.md) |
