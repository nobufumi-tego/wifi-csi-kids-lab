English | [日本語](03_decision_tree.ja.md)

# 5-3. Decision tree — a model you can read

A **decision tree** is a list of yes/no questions, like a flowchart. The nice thing:
you can print it and check whether its rules make sense. On this page you train one
and look at its mistakes with a **confusion matrix**.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## Twenty questions

Do you know the game "twenty questions"? "Is it an animal?" "Yes." "Does it fly?"
"No." ... A decision tree plays that game with the numbers of a window:
"Is `change_rate` bigger than 0.04?" and so on, until it reaches an answer.

The computer picks the questions itself: at each step it chooses the question that
best separates the labels in the training data.

## Train a small tree

We allow at most 3 questions in a row (`max_depth=3`), so the tree stays small and
easy to read. This uses `X_train`, `y_train`, ... from [5-2](02_train_and_test.md).

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(max_depth=3, random_state=0)
tree.fit(X_train, y_train)

names = ["motion", "motion_max", "spread", "rssi_std_db", "change_rate"]
print(export_text(tree, feature_names=names))
print("train:", accuracy_score(y_train, tree.predict(X_train)))
print("test :", accuracy_score(y_test, tree.predict(X_test)))
```

In our run (train `seed=1`, test `seed=2`, room 7) the tree was:

```text
|--- change_rate <= 0.04
|   |--- motion <= 0.04
|   |   |--- spread <= 0.24
|   |   |   |--- class: still
|   |   |--- spread >  0.24
|   |   |   |--- class: empty
|   |--- motion >  0.04
|   |   |--- motion_max <= 0.05
|   |   |   |--- class: wave
|   |   |--- motion_max >  0.05
|   |   |   |--- class: wave
|--- change_rate >  0.04
|   |--- class: walk
```

and it scored **0.892 on train** and **0.912 on test**.

How to read it:

- Fast changes (`change_rate` above 0.04) → `walk`.
- Slow changes but some wobble (`motion` above 0.04) → `wave`. (Both branches under it
  say `wave`; the last question did not change the answer.)
- Almost no wobble → `empty` or `still`, decided by `spread`.

Remember `spread`, the "fingerprint of the room". It will matter on the next page.

Want a picture instead of text? `sklearn.tree.plot_tree(tree, feature_names=names, class_names=tree.classes_, filled=True)`
draws the same tree with matplotlib.

## The confusion matrix: where are the mistakes?

One accuracy number hides *which* answers are wrong. A **confusion matrix** shows it:
rows = the truth, columns = what the model said.

```python
from sklearn.metrics import confusion_matrix

labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_test, tree.predict(X_test), labels=labels))
```

For the test data (same room) we got:

| truth ↓ / said → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 20 | 39 | 0 | 1 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 0 | 60 |

The numbers on the diagonal (top-left to bottom-right) are correct answers. The
mistakes are almost all in one place: 20 `still` windows were called `empty`. A
person sitting very still hardly changes the signal, so this is a hard pair.

> 🤖 **Ask your AI**
> - "Here is my decision tree printout. Don't explain it yet. Ask me what the first question means."
> - "In my confusion matrix, 20 'still' windows were called 'empty'. Why could that happen? Give me hints."

## Check yourself

1. What does `max_depth=3` do?
2. In the confusion matrix, where are the correct answers?
3. What does the confusion matrix show that a single accuracy number does not?

<details><summary>Answers</summary>

1. The tree may ask at most 3 questions in a row. It keeps the tree small and easier to read (and less likely to overfit).
2. On the diagonal, where the truth and the answer are the same label.
3. Which labels get mixed up with which, for example `still` being called `empty`.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Decision trees and random forests (counting): [決定木とランダムフォレスト（組合せ）](https://github.com/nobufumi-tego/learning-math/blob/main/04_discrete_math/03_combinatorics.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [5-2. Training and testing](02_train_and_test.md) | [Chapter 5](README.md) | [Home](../README.md) | [5-4. A new room](04_new_room.md) |
