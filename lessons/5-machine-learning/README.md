English | [日本語](README.ja.md)

# Level 5: Your first machine learning

## Goal

- Go from **rules you write** (Level 4) to **rules the computer learns**
- Understand why you must **never test on your training data**
- Train a **decision tree** and read the rules it found
- Compare it with a **random forest** and **k-nearest neighbors**
- Read a **confusion matrix**, and learn what **overfitting** is
- Report results **honestly** — including the "new room" test

**Time:** about 90 minutes (you can split it into two days)
**What you need:** Level 4 finished. Install the machine learning extra once:

```bash
uv sync --extra ml
```

Notebook version: [`notebooks/03-first-machine-learning.ipynb`](../../notebooks/03-first-machine-learning.ipynb)

---

## 1. From rules to learning

In Level 4 **you** chose one number (`motion`) and one threshold. That worked for
"moving or not", but we now want four answers: `empty`, `still`, `walk`, `wave`.
With five numbers per window, writing the rules by hand gets hard. Machine learning
lets the computer **look at examples and find the rules**.

Each 1-second window becomes one row of a table:

```python
from csi_lab import simulate_sequence
from csi_lab.features import window_features

steps = [("empty", 60), ("still", 60), ("walk", 60), ("wave", 60)]
w = window_features(simulate_sequence(steps, seed=1))

print(w.names)          # the column names (features)
print(w.features[:3])   # the first three rows
print(w.labels[:3])     # the right answers for those rows
```

- **Features** (`w.features`) = the question sheet: numbers that describe each window
- **Labels** (`w.labels`) = the answer key: what was really happening

## 2. Never test on your training data

Imagine a test where the questions are exactly the practice questions you memorized.
You would get 100 % — but that says nothing about whether you *understand*.
Machines are the same. So we always keep separate data for testing.

We use three sets:

| set | how we make it | what it tells us |
|---|---|---|
| **train** | `seed=1`, room 7 | the examples the model learns from |
| **test** | `seed=2`, room 7 | new recording, **same room** |
| **new room** | `seed=2`, `room_seed=99` | new recording, **different furniture** |

```python
def make(seed, room_seed=7):
    w = window_features(simulate_sequence(steps, seed=seed, room_seed=room_seed))
    return w.features, w.labels

X_train, y_train = make(seed=1)
X_test, y_test = make(seed=2)
X_room, y_room = make(seed=2, room_seed=99)
```

Splitting **by recording** (not by mixing random windows from one recording) is important:
windows next to each other are very similar, so mixing them would be like peeking.

## 3. A decision tree you can read

A **decision tree** is a list of yes/no questions like "Is `motion` bigger than 0.04?".
The nice thing: you can print it and check whether the rules make sense.

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(max_depth=3, random_state=0)
tree.fit(X_train, y_train)

print(export_text(tree, feature_names=list(w.names)))
print("train   :", accuracy_score(y_train, tree.predict(X_train)))
print("test    :", accuracy_score(y_test, tree.predict(X_test)))
print("new room:", accuracy_score(y_room, tree.predict(X_room)))
```

In our run the tree first asks about `change_rate` (fast changes → `walk`), then `motion`,
and uses `spread` to tell `empty` from `still`. Remember `spread` — it matters soon.

## 4. More models: random forest and k-nearest neighbors

- **Random forest** = many trees that vote.
- **k-nearest neighbors (KNN)** = "find the 5 most similar training windows and copy their answer".

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

models = {
    "tree (depth 3)": DecisionTreeClassifier(max_depth=3, random_state=0),
    "tree (no limit)": DecisionTreeClassifier(random_state=0),
    "random forest": RandomForestClassifier(random_state=0),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:16s} train={accuracy_score(y_train, model.predict(X_train)):.3f} "
          f"test={accuracy_score(y_test, model.predict(X_test)):.3f} "
          f"new room={accuracy_score(y_room, model.predict(X_room)):.3f}")
```

What we got (simulator, seeds as above):

| model | train | test (same room) | new room |
|---|---|---|---|
| tree (depth 3) | 0.892 | 0.912 | 0.562 |
| tree (no limit) | 1.000 | 0.954 | 0.458 |
| random forest | 1.000 | 0.950 | 0.496 |
| KNN (k=5) | 0.967 | 0.896 | 0.308 |

## 5. Overfitting

The unlimited tree and the forest score **100 %** on training data. That is a warning sign,
not a victory: they may have memorized details of *these* recordings. This is called
**overfitting** — like memorizing the practice test instead of learning the subject.
The test column is the fair score. The "new room" column is the hard, honest one.

## 6. The confusion matrix: where are the mistakes?

One accuracy number hides *which* answers are wrong. A **confusion matrix** shows it:
rows = the truth, columns = what the model said.

```python
from sklearn.metrics import confusion_matrix

labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_test, tree.predict(X_test), labels=labels))
print(confusion_matrix(y_room, tree.predict(X_room), labels=labels))
```

For the depth-3 tree we got:

Same room (test):

| truth ↓ / said → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 20 | 39 | 0 | 1 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 0 | 60 |

New room:

| truth ↓ / said → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 43 | 0 | 0 | 17 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 45 | 15 |

In the new room, the tree never says `still` — it calls it `empty` or `wave`. Why? It
used `spread`, a kind of **fingerprint of the room**. New furniture = new fingerprint,
so the learned rule no longer fits. And in the new room, most `wave` windows look like `walk`.

## 7. Report honestly

- The simulator is **cleaner than reality**. Real recordings will usually score lower.
- Always say **how you tested**: same recording? same room? different day?
- Say what did **not** work. We tried two quick fixes — dropping `spread`, and training on
  three rooms (7, 11, 23) — and neither helped in the new room (0.487 and 0.388).
  Making Wi-Fi sensing work in **a room it has never seen** is still a hard problem that
  researchers work on. Maybe your free research can try an idea!

> **Ask your AI**
> "My decision tree scores 91 % in the same room but 56 % in a new room. Don't give me the
> answer — ask me questions that help me figure out why."

> **Ask your AI**
> "Explain overfitting with an example from school tests. Then quiz me with two questions."

## Check yourself

1. Why do we test on a different recording instead of the training data?
2. A model gets 100 % on training data. Should you be happy?
3. What does a confusion matrix show that a single accuracy number does not?
4. Why did the tree fail in the new room?

<details>
<summary>Answers</summary>

1. Testing on training data only shows whether the model memorized. A new recording shows whether it can handle something it has not seen.
2. Not yet. It may be overfitting. Check the test score (and the new-room score).
3. Which labels get mixed up with which — for example `still` being called `empty`.
4. It relied on `spread`, which describes the room itself. When the furniture moved (`room_seed=99`), that number changed, so the rule broke.

</details>

## Next

➡ [Free research projects](../../projects/README.md) — use what you learned to answer your own question.
