English | [日本語](03_look_at_data.ja.md)

# 2-3. Look at the data — make pretend recordings and draw them

Time to see CSI with your own eyes. We have no hardware yet, so we use the lab's
**simulator**: it imitates a room with a sender and a receiver 3 m apart. On this page
you will make recordings, draw them, and open them in a spreadsheet and in Python.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_look_at_csi.ipynb`](notebooks/01_look_at_csi.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## What a recording looks like

A recording is a table. **One row = one packet.** The transmitter sends 100 packets per
second, so 30 seconds is about 3,000 rows.

| time_s | rssi_dbm | label | sc-28 | sc-27 | … | sc28 |
|---|---|---|---|---|---|---|
| 0.000 | -54 | walk | 47.539 | 46.615 | … | … |
| 0.009 | -56 | walk | 48.332 | 49.396 | … | … |

- `time_s`: seconds since the start
- `rssi_dbm`: signal strength (closer to 0 = stronger, see [2-2](02_what_is_csi.md))
- `label`: what was happening
- `sc-28` … `sc28`: amplitude on each lane

(These two rows are the start of `walk.csv` made by the command below.)

## Step 1: make pretend recordings

In a terminal in the lab folder:

```bash
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
compare with real data in [Chapter 3](../03_build/README.md).

## Step 2: draw them

```bash
uv run csi-lab show data/samples/empty.csv
uv run csi-lab show data/samples/walk.csv
```

Each command saves a picture next to the file (`empty.png`, `walk.png`). Open both.

- **Top (heat map):** time goes to the right, lanes go up. Color = amplitude.
- **Middle:** a "motion number" for each second (you will build this in
  [Chapter 4](../04_analysis/README.md)).
- **Bottom:** RSSI.

What is different between the two pictures? Look for **vertical stripes** in the heat
map.

## Step 3: open a file in a spreadsheet

Open `data/samples/walk.csv` in Excel, Google Sheets, or LibreOffice. The first line
starts with `#`: it is a note about the file (`source=simulated scenario=walk ...`).
Make a line chart of the `sc10` column.

## Step 4: load it in Python

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

With the sample made by `csi-lab samples` (the walk file uses seed 2) we got
**2963 packets, 30.0 seconds, 98.8 packets per second**. Not exactly 3,000 or 100: the
simulator drops about 1% of packets on purpose, like a real receiver.

## Step 5: draw a few lanes

```python
from csi_lab import load_csv
from csi_lab.plot import plot_subcarriers

for name in ["empty", "walk"]:
    rec = load_csv(f"data/samples/{name}.csv")
    fig = plot_subcarriers(rec, [-20, -5, 10, 25])
    fig.savefig(f"data/samples/{name}-lanes.png")
```

Compare the two pictures. Which one wiggles more?

> 🤖 **Ask your AI**
> - "I have a table where each row is a Wi-Fi packet and there are 56 columns of
>   amplitude. Explain how to read a heat map of it. Don't write code for me; give me
>   hints."
> - "In my walk.png there are vertical stripes in the heat map. What could make them?
>   Ask me questions so I figure it out myself."
> - "What does `df.describe()` tell me? Explain count, mean, std, min and max simply."

## Check yourself

1. In a recording, what does one row stand for?
2. Which command draws a recording and saves a picture?
3. Why does the walk recording have a little fewer than 3,000 rows?

<details><summary>Answers</summary>

1. One packet.
2. `uv run csi-lab show <file>`.
3. Some packets are missed (the simulator drops about 1% on purpose, like a real
   receiver), and the timing is not perfectly even.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [2-2. What is CSI?](02_what_is_csi.md) | [Chapter 2](README.md) | [Home](../README.md) | [2-4. Automatic gain](04_automatic_gain.md) |
