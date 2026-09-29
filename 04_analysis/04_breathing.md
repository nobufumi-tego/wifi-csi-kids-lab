English | [日本語](04_breathing.ja.md)

# 4-4. Finding breathing — can Wi-Fi see a slow rhythm?

Breathing moves the chest only a few millimeters, but slowly and **regularly**. On this
bonus page you look for that rhythm in the simulator, and learn why it is much harder in
real life.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb).
> New to the terminal? → [0-2. Terminal and uv](../start_here/02_terminal_and_uv.md)

## 1. Rhythms inside a signal

Music is many notes played together. Your ear can tell a low note from a high note even
when they sound at the same time. A **Fourier transform** does the same for a signal: it
splits it into slow and fast rhythms and tells how strong each one is.

Breathing 15 times per minute is a rhythm of

$$
f = \frac{15}{60\ \text{s}} = 0.25\ \text{Hz}
$$

(0.25 times per second). `breathing_rate_bpm` looks for the strongest slow rhythm
between 6 and 40 breaths per minute and turns it back into breaths per minute (bpm).

## 2. Try it

```python
from csi_lab import simulate
from csi_lab.features import breathing_rate_bpm

rec = simulate("breathe", duration_s=60, seed=3)
print("breaths per minute:", round(breathing_rate_bpm(rec), 1))
```

The simulated person breathes 15 times per minute, and the function finds 15.0
(`seed=3`). The recording must be long enough to contain a few breaths: at least 20 s
for the slowest rate it looks for.

## 3. Be careful

- This works nicely **in the simulator**. In a real room it is much harder: people move a
  little, other people and machines move, and the signal is noisier.
- Try `simulate("still", 60, seed=2)`. Nobody breathes in a regular way there, but the
  function still returns a number: 9.0. **A tool always gives an answer; that does not
  mean the answer is true.**
- This is **not a medical device**. Never use it to check someone's health.

> 🤖 **Ask your AI**
> - "Explain a Fourier transform with a music example. No formulas, and ask me one
>   question at the end."
> - "The function returned 9 breaths per minute for a recording with no breathing. How
>   could I check whether an answer is real?"

## Check yourself

1. 20 breaths per minute is how many breaths per second (Hz)?
2. Why did the function return a number for the "still" recording?
3. Why must you never use this to check someone's health?

<details><summary>Answers</summary>

1. $20 / 60 \approx 0.33$ Hz.
2. It always picks the strongest slow rhythm, even if that rhythm is just noise or small
   movements.
3. It was only tested in a simple simulator, it can be wrong without warning, and it is
   not a medical device.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Waves and rhythm: [波とリズム（三角関数）](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/03_trigonometry.md)
- Fourier transform demo: [フーリエ変換のデモ](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/notebooks/03_trigonometry_usecases.ipynb)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [4-3. What goes wrong](03_what_goes_wrong.md) | [Chapter 4](README.md) | [Home](../README.md) | [Chapter 5. Machine learning](../05_machine_learning/README.md) |
