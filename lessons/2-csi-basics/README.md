English | [日本語](README.ja.md)

# Level 2: CSI basics — look at the data

**Goal:** Know what CSI is, make pretend recordings on your computer, and draw them
with Python. At the end you will *see* the difference between an empty room and a
room where someone walks.

**Time:** about 60–90 minutes

**What you need:** A computer with this repository set up (see the main
[README](../../README.md)). No ESP32 yet.

---

## 1. Wi-Fi sends many waves side by side

In Level 1 we talked about "the" Wi-Fi wave. Actually, Wi-Fi splits its channel (a
20 MHz wide slice of radio frequencies) into many narrow **lanes**, like a highway with
many lanes. Each lane carries its own small wave. The lanes are called
**subcarriers**. This way of sending is called **OFDM**.

```
frequency ->
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
-28 ...            -1   (0)  1              ...          28
                         ^ the center lane is left empty
```

Neighboring lanes are 312.5 kHz apart. In this repository we use **56 lanes**, numbered
−28 to −1 and 1 to 28 (lane 0 in the middle is not used).

Each lane has a slightly different frequency, so a slightly different wavelength.
Remember interference from Level 1? The same room paths can **help** on one lane and
**cancel** on the next. So every lane arrives with its own size.

## 2. So what is CSI?

**CSI** stands for **Channel State Information**. For every packet the receiver gets,
it measures how each lane arrived:

- **Amplitude**: how big the wave is when it arrives. This is what we use.
- **Phase**: where in its up-and-down the wave is when it arrives. It exists, but a
  cheap receiver with one antenna (like the ESP32) mixes in its own timing errors, so
  phase is hard to use. We skip it here.

Compare it with **RSSI** (Received Signal Strength Indicator), which your phone uses for
the Wi-Fi bars:

| | RSSI | CSI |
|---|---|---|
| How many numbers per packet | 1 (total strength) | 56 (one per lane) |
| What it is like | "How loud was the whole song?" | "How loud was each instrument?" |
| Good for | Is the signal strong? | *How* did the room change the signal? |

With 56 numbers instead of 1, CSI can notice small changes that RSSI misses.

## 3. What a recording looks like

A recording is a table. **One row = one packet.** The transmitter sends 100 packets
per second, so 30 seconds is about 3,000 rows.

| time_s | rssi_dbm | label | sc-28 | sc-27 | … | sc28 |
|---|---|---|---|---|---|---|
| 0.000 | -52 | walk | 31.0 | 29.4 | … | 25.2 |
| 0.010 | -52 | walk | 30.5 | 29.7 | … | 25.8 |

- `time_s`: seconds since the start
- `rssi_dbm`: signal strength (closer to 0 = stronger)
- `label`: what was happening
- `sc-28` … `sc28`: amplitude on each lane

---

## Try it

### Step 1: make pretend recordings

We do not have hardware yet, so we use the **simulator**. It imitates a room with a
sender and a receiver 3 m apart.

```bash
uv sync
uv run csi-lab samples
```

This writes files into `data/samples/`:

| File | What happens |
|---|---|
| `empty.csv` | nobody in the room |
| `still.csv` | a person sits still, away from the line |
| `walk.csv` | a person walks back and forth across the line |
| `breathe.csv` | a person sits near the line and breathes |
| `wave.csv` | a person sits and waves a hand |
| `story.csv` | the situation changes over time |

These are **pretend** data made by a simple model. Real rooms are messier. You will
compare with real data in Level 3.

### Step 2: draw them

```bash
uv run csi-lab show data/samples/empty.csv
uv run csi-lab show data/samples/walk.csv
```

Each command saves a picture next to the file (`empty.png`, `walk.png`). Open both.

- **Top (heat map):** time goes to the right, lanes go up. Color = amplitude.
- **Middle:** a "motion number" for each second (you will build this in Level 4).
- **Bottom:** RSSI.

What is different between the two pictures? Look for **vertical stripes** in the heat
map.

### Step 3: open a file in a spreadsheet

Open `data/samples/walk.csv` in Excel, Google Sheets, or LibreOffice. The first line
starts with `#`; it is a note about the file. Make a line chart of the `sc10` column.

### Step 4: load it in Python

```python
from csi_lab import load_csv

rec = load_csv("data/samples/walk.csv")
print(rec.n_packets, "packets")
print(round(rec.duration_s, 1), "seconds")
print(round(rec.rate_hz, 1), "packets per second")

df = rec.to_dataframe()   # a pandas table, same columns as the CSV
print(df.head())
print(df["sc10"].describe())
```

### Step 5: draw a few lanes

```python
from csi_lab import load_csv
from csi_lab.plot import plot_subcarriers

for name in ["empty", "walk"]:
    rec = load_csv(f"data/samples/{name}.csv")
    fig = plot_subcarriers(rec, [-20, -5, 10, 25])
    fig.savefig(f"data/samples/{name}-lanes.png")
```

Compare the two pictures. Which one wiggles more?

There is also a notebook version of this lesson: `notebooks/01-look-at-csi.ipynb`.
Open it with `uv run --extra notebook jupyter lab`.

## 4. Why we "normalize" first

The ESP32 has an automatic volume knob (called **automatic gain control**). For every
packet it turns the volume up or down so the numbers stay in a handy range. That means
the raw amplitude can jump even when nothing in the room moved.

To remove this, we divide each packet by its own average over the 56 lanes:

```python
from csi_lab.features import normalize_per_packet

norm = normalize_per_packet(rec.amplitude)   # each row now averages to 1
```

The heat map from `csi-lab show` already does this. What is left is the **shape**
across the lanes (which lanes are strong, which are weak), and that shape is what the
room and the people in it change.

---

> **Ask your AI**
>
> - "I have a table where each row is a Wi-Fi packet and there are 56 columns of
>   amplitude. Explain how to read a heat map of it. Don't write code for me; give me
>   hints."
> - "What is the difference between RSSI and CSI? Use a music or orchestra example."
> - "In my walk.png there are vertical stripes in the heat map. What could make them?
>   Ask me questions so I figure it out myself."

## Check yourself

1. How many lanes (subcarriers) does one packet have in this repository?
2. RSSI gives one number per packet. How many does CSI give here?
3. Why do we divide each packet by its own average before drawing?

<details>
<summary>Answers</summary>

1. 56 (−28 to −1 and 1 to 28).
2. 56: one amplitude per lane.
3. The ESP32 changes its volume (automatic gain) every packet. Dividing by the average
   removes that jump and keeps the shape across lanes, which is what the room changes.

</details>

---

**Previous:** [Level 1](../1-waves/README.md) · **Next:** [Level 3: Build your own sender and receiver](../3-build/README.md)
