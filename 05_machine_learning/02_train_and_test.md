English | [日本語](02_train_and_test.ja.md)

# 5-2. Training and testing — why we never test on the practice questions

A model that gets 100 % is not always a good model. On this page you learn how to
test **fairly**, and what **overfitting** means.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## The practice-test story

Imagine a test where the questions are exactly the practice questions you memorized.
You would get 100 %, but that says nothing about whether you *understand* the subject.
Machines are the same. So we always keep **separate data for testing**.

## Three sets of data

| set | how we make it | what it tells us |
|---|---|---|
| **train** | `seed=1`, room 7 | the examples the model learns from |
| **test** | `seed=2`, room 7 | a new recording in the **same room** |
| **new room** | `seed=2`, `room_seed=99` | a new recording with **different furniture** |

`seed` changes the recording (who moves when, the noise). `room_seed` moves the
furniture, so the room itself is different. Room 7 is the simulator's default room.

```python
from csi_lab import simulate_sequence
from csi_lab.features import window_features

steps = [("empty", 60), ("still", 60), ("walk", 60), ("wave", 60)]

def make(seed, room_seed=7):
    w = window_features(simulate_sequence(steps, seed=seed, room_seed=room_seed))
    return w.features, w.labels

X_train, y_train = make(seed=1)
X_test, y_test = make(seed=2)
X_room, y_room = make(seed=2, room_seed=99)
```

We split **by recording**, not by mixing random windows from one recording. Windows
next to each other are very similar, so putting one in "train" and its neighbor in
"test" would be like peeking at the answers.

## Accuracy

The simplest score is **accuracy**: the share of windows the model got right.

$$\text{accuracy} = \frac{\text{number of correct answers}}{\text{number of windows}}$$

An accuracy of 0.9 means 9 out of 10 windows were right.

## Overfitting

Let's train a decision tree with no limit on how many questions it may ask (you will
meet decision trees properly on the next page):

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(random_state=0)   # no limit
tree.fit(X_train, y_train)
print("train:", accuracy_score(y_train, tree.predict(X_train)))
print("test :", accuracy_score(y_test, tree.predict(X_test)))
```

In our run (seeds as above) it scored **1.000 on train** and **0.954 on test**.

The perfect train score is a **warning sign**, not a victory. The model may have
learned tiny details that only exist in *these* recordings, like memorizing the
practice test. This is called **overfitting**. The test score is the fair one, and
it is always the one you report.

> 🤖 **Ask your AI**
> - "Explain overfitting with an example from school tests. Then quiz me with two questions."
> - "Why is it bad to randomly mix windows from one recording into train and test? Give me a hint first."

## Check yourself

1. Why do we test on a different recording instead of the training data?
2. A model gets 100 % on training data. Should you be happy?
3. What is the difference between `seed` and `room_seed`?

<details><summary>Answers</summary>

1. Testing on training data only shows whether the model memorized. A new recording shows whether it can handle something it has not seen.
2. Not yet. It may be overfitting. Look at the test score (and later the new-room score).
3. `seed` makes a different recording in the same room. `room_seed` changes the room itself (the furniture).

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Loss functions and overfitting: [損失関数と過学習](https://github.com/nobufumi-tego/learning-math/blob/main/06_ml_math_bridge/01_loss_functions.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [5-1. Features and labels](01_features_and_labels.md) | [Chapter 5](README.md) | [Home](../README.md) | [5-3. Decision tree](03_decision_tree.md) |
