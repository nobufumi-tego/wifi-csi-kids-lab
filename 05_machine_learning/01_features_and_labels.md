English | [日本語](01_features_and_labels.ja.md)

# 5-1. Features and labels — turning a recording into a table

Machine learning needs examples in a neat table: **questions** and their **answers**.
On this page you turn a CSI recording into exactly that.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## From rules to learning

In Chapter 4 you wrote one rule: "if `motion` is bigger than the threshold, someone
is moving". That worked for two answers (moving / not moving). Now we want **four**
answers:

| label | what was happening |
|---|---|
| `empty` | nobody in the room |
| `still` | a person sits still |
| `walk` | a person walks across the line between the boards |
| `wave` | a person sits and waves a hand |

With five numbers per window, writing the rules by hand gets hard. Machine learning
lets the computer **look at many examples and find the rules**.

## One window = one row

We cut the recording into 1-second windows, just like in Chapter 4. Each window
becomes **one row** of a table:

```python
from csi_lab import simulate_sequence
from csi_lab.features import window_features

steps = [("empty", 60), ("still", 60), ("walk", 60), ("wave", 60)]
w = window_features(simulate_sequence(steps, seed=1))

print(w.names)          # the column names (features)
print(w.features[:3])   # the first three rows
print(w.labels[:3])     # the right answers for those rows
print(w.features.shape) # (rows, columns)
```

With `seed=1` this gives 240 rows (60 of each label) and 5 columns. The first three
rows look like this (rounded):

| motion | motion_max | spread | rssi_std_db | change_rate | label |
|---|---|---|---|---|---|
| 0.0303 | 0.0345 | 0.2764 | 1.0563 | 0.0345 | empty |
| 0.0303 | 0.0358 | 0.2756 | 1.0017 | 0.0338 | empty |
| 0.0307 | 0.0347 | 0.2758 | 0.9563 | 0.0348 | empty |

- **Features** (`w.features`) = the question sheet: numbers that describe each window
- **Labels** (`w.labels`) = the answer key: what was really happening

## What the five features mean

| feature | meaning |
|---|---|
| `motion` | how much the amplitude wobbles, averaged over all subcarriers (your number from Chapter 4) |
| `motion_max` | the wobble of the subcarrier that wobbles the most |
| `spread` | how different the subcarriers are from each other (a kind of fingerprint of the room) |
| `rssi_std_db` | how much the signal strength wobbles, in dB |
| `change_rate` | how fast the amplitude changes from one packet to the next |

For example, if $\sigma_k$ is the wobble (standard deviation over time) of
subcarrier $k$, then `motion` is the average over the 56 subcarriers:

$$\text{motion} = \frac{1}{56} \sum_{k} \sigma_k$$

## Each row is a list of numbers

One row, like `[0.0303, 0.0345, 0.2764, 1.0563, 0.0345]`, is **a list of five
numbers**. In math this is called a **vector**. You can think of it as a point in a
space with five directions. Windows that are alike are points close to each other,
and that is what machine learning uses to tell them apart.

> 🤖 **Ask your AI**
> - "Explain what a 'feature' is in machine learning using a school report card as an example."
> - "Here is one row of my table: [0.03, 0.035, 0.28, 1.06, 0.035]. Ask me what each number might mean before telling me."

## Check yourself

1. In our table, what does one row stand for?
2. What is the difference between a feature and a label?
3. Why is it hard to write the rules for four labels by hand?

<details><summary>Answers</summary>

1. One 1-second window of the recording.
2. Features are the numbers that describe the window (the question). The label is what was really happening (the answer).
3. There are five numbers per window and four possible answers, so there are many combinations to think about. It is easier to let the computer find the rules from examples.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Vectors: a list of numbers: [ベクトル（数の並び）](https://github.com/nobufumi-tego/learning-math/blob/main/01_linear_algebra/01_vectors.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Chapter 5](README.md) | [Chapter 5](README.md) | [Home](../README.md) | [5-2. Training and testing](02_train_and_test.md) |
