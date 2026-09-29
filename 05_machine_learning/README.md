English | [日本語](README.ja.md)

# Chapter 5: Your first machine learning

In [Chapter 4](../04_analysis/README.md) **you** chose one number and one threshold.
Now the computer will **look at examples and find the rules by itself**. You will
also learn the most important habit in machine learning: testing fairly, and
reporting honestly when something does not work.

## Goal

- Go from **rules you write** to **rules the computer learns**
- Understand why you must **never test on your training data**
- Train a **decision tree** and read the rules it found
- Read a **confusion matrix**, and learn what **overfitting** is
- Try the hard test: **a room the model has never seen**

**Who:** junior high school students and up, after Chapter 4.
**Time:** about 90 minutes in total (you can split it over two days).
**What you need:** a computer with this lab installed. `uv sync` (or the start script)
installs everything, including scikit-learn. No ESP32 boards needed.

## Pages

| # | Page | What you learn | Time |
|---|---|---|---|
| 5-1 | [`01_features_and_labels.md`](01_features_and_labels.md) | Turn a recording into a table: features (questions) and labels (answers) | 15 min |
| 5-2 | [`02_train_and_test.md`](02_train_and_test.md) | Why we test on new data; what overfitting is | 20 min |
| 5-3 | [`03_decision_tree.md`](03_decision_tree.md) | A decision tree you can read; the confusion matrix | 25 min |
| 5-4 | [`04_new_room.md`](04_new_room.md) | The "new room" test, other models, and honest reporting | 30 min |

## Notebook

| Read (md) | Run (ipynb) | What you can do |
|---|---|---|
| 5-1 to 5-4 | [`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb) | Every step of this chapter, ready to run with Shift+Enter |

> 💡 **Run the code in this chapter**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open the notebook above.
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

> ⚠️ All numbers in this chapter come from the **simulator** (the seeds are written next
> to them). Real rooms are messier, so your own recordings will usually score lower.

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [4-4. Finding breathing](../04_analysis/04_breathing.md) | [Chapter 5](README.md) | [Home](../README.md) | [5-1. Features and labels](01_features_and_labels.md) |
