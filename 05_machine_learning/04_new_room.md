English | [日本語](04_new_room.ja.md)

# 5-4. A new room — the hard, honest test

A model that works in the room where it learned is a good start. But what happens
in **a room it has never seen**? On this page you try it, compare other models, and
learn to report results honestly, including the parts that do not work.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## More models

Besides the decision tree, we try two popular models:

- **Random forest** = many decision trees that each give an answer, and then vote.
- **k-nearest neighbors (KNN)** = "find the 5 training windows most similar to this
  one, and copy their most common answer". Remember that each window is a point
  (5-1); "similar" means "close".

This uses `X_train`, `X_test`, `X_room`, ... from [5-2](02_train_and_test.md).

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

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

What we got (train `seed=1` room 7, test `seed=2` room 7, new room `seed=2` `room_seed=99`):

| model | train | test (same room) | new room |
|---|---|---|---|
| tree (depth 3) | 0.892 | 0.912 | 0.562 |
| tree (no limit) | 1.000 | 0.954 | 0.458 |
| random forest | 1.000 | 0.950 | 0.496 |
| KNN (k=5) | 0.967 | 0.896 | 0.308 |

In the same room, every model scores about 0.9 or more. In the new room, every model
**drops a lot**. With four labels, guessing at random would be right about a quarter
of the time (0.25), so KNN in the new room is not much better than guessing.

## Why did it fail? The confusion matrix knows

```python
from sklearn.metrics import confusion_matrix

tree = models["tree (depth 3)"]
labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_room, tree.predict(X_room), labels=labels))
```

For the depth-3 tree in the new room:

| truth ↓ / said → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 43 | 0 | 0 | 17 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 45 | 15 |

The tree **never says `still`** in the new room: it calls it `empty` or `wave`. Why?
In [5-3](03_decision_tree.md) it used `spread` to tell `empty` from `still`, and
`spread` is a kind of **fingerprint of the room**. New furniture = new fingerprint,
so the learned rule no longer fits. Also, most `wave` windows now look like `walk`.

## We tried two fixes. Neither worked.

1. **Drop `spread`**, the room fingerprint, and train again → new room accuracy **0.487**.
2. **Train on three rooms** (`room_seed` 7, 11 and 23) so the model sees more variety
   → new room accuracy **0.388**.

(Both with the depth-3 tree, `seed=1` for training, new room `seed=2` `room_seed=99`.)

This is not a failure of *you*. Making Wi-Fi sensing work in **a room it has never
seen** is a hard problem that researchers still work on. Maybe your free research
can try a new idea, such as a new feature that does not depend on the room.

## Report honestly

When you write about a model, always say:

- **How you tested**: same recording? same room? a different day?
- **What the data was**: simulator or real boards? The simulator is **cleaner than
  reality**, so real recordings will usually score lower.
- **What did not work**, not only what worked. Results like "0.912 in the same room,
  0.562 in a new room" are much more useful than just "91 %".

> 🤖 **Ask your AI**
> - "My decision tree scores 91 % in the same room but 56 % in a new room. Don't give me the answer. Ask me questions that help me figure out why."
> - "Suggest three ideas for a feature that might not change when the furniture moves. Only give one-sentence hints."

## Check yourself

1. Why did the tree never answer `still` in the new room?
2. With four labels, about what accuracy would random guessing get?
3. Someone writes "my model is 95 % accurate". What questions should you ask them?

<details><summary>Answers</summary>

1. It used `spread` to separate `empty` and `still`. `spread` describes the room itself, so when the furniture changed (`room_seed=99`), the rule broke.
2. About 0.25 (one in four).
3. For example: Was it tested on data it had not seen? The same room or a new room? Simulator or real? Which labels does it mix up?

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Estimation and overfitting: [推定と過学習](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/06_estimation.md)
- How machines learn (gradient descent): [機械が学ぶしくみ（勾配降下法）](https://github.com/nobufumi-tego/learning-math/blob/main/05_optimization/02_gradient_descent.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [5-3. Decision tree](03_decision_tree.md) | [Chapter 5](README.md) | [Home](../README.md) | [Chapter 6: Free research](../06_free_research/README.md) |
