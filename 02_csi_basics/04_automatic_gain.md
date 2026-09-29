English | [日本語](04_automatic_gain.ja.md)

# 2-4. Automatic gain — why we divide by the average first

The ESP32 turns its own volume knob up and down for every packet. That makes the raw
numbers jump even when nothing in the room moves. On this page you will see the jumps,
and remove them with one line of Python.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_look_at_csi.ipynb`](notebooks/01_look_at_csi.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## The automatic volume knob

A strong signal and a weak signal would give numbers of very different sizes. To keep
them in a handy range, the ESP32 has an automatic volume knob, called **automatic gain
control** (AGC). For every packet it turns the volume up or down a little.

The problem: the raw amplitude can jump **even when nothing in the room moved** —
just because the knob moved.

## See the jumps

Take the empty-room sample from [2-3](03_look_at_data.md) and compute, for every
packet, the average amplitude over its 56 lanes:

```python
from csi_lab import load_csv

rec = load_csv("data/samples/empty.csv")
packet_average = rec.amplitude.mean(axis=1)    # one average per packet (row)
print(packet_average.min(), packet_average.max())
```

With `empty.csv` from `csi-lab samples` (seed 0) we got averages from **25.6 to 31.8**,
even though nobody was in the room.

## Remove them: divide by the packet's own average

The fix: divide every packet by its own average over the 56 lanes. Then every row
averages to exactly 1.

$$
\text{normalized amplitude} = \frac{\text{amplitude on one lane}}{\text{average of the 56 lanes in that packet}}
$$

```python
from csi_lab.features import normalize_per_packet

norm = normalize_per_packet(rec.amplitude)     # each row now averages to 1
print(norm.mean(axis=1).std())                 # almost 0: the jumps are gone
```

We got about $1 \times 10^{-16}$: that is zero, apart from tiny computer rounding.

## What is left: the shape

After dividing, the overall loudness is gone. What is left is the **shape** across the
lanes: which lanes are strong and which are weak. That shape is what the room and the
people in it change (remember [1-4](../01_waves/04_interference.md)). The heat map from
`csi-lab show` already does this for you.

> 🤖 **Ask your AI**
> - "Why would a receiver change its volume by itself? Explain with a microphone or a
>   camera's automatic brightness."
> - "If I divide every row of a table by its own average, what changes and what stays
>   the same? Give me a tiny example with 3 numbers."
> - "Why is 1e-16 basically zero for a computer?"

## Check yourself

1. What is automatic gain control?
2. Why can the raw amplitude jump when nothing moves?
3. After `normalize_per_packet`, what is the average of every row?

<details><summary>Answers</summary>

1. The receiver's automatic volume knob: it turns the volume up or down for each packet.
2. Because the knob itself changes from packet to packet.
3. 1. What remains is the shape across the lanes, which is what the room changes.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Mean and other summaries: [記述統計](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/05_descriptive_stats.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [2-3. Look at the data](03_look_at_data.md) | [Chapter 2](README.md) | [Home](../README.md) | [Chapter 3: Build](../03_build/README.md) |
