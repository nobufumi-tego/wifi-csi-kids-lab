English | [日本語](02_terminal_and_uv.ja.md)

# 0-2. Terminal and uv — opening the lab

This page shows how to open the lab on your computer. You will meet three helpers:
the **terminal**, **uv**, and **JupyterLab**. Ask a grown-up to help the first time,
because it installs software.

## Step 1. Get the lab onto your computer

- **Easy way**: on the GitHub page, click the green **`<> Code`** button →
  **Download ZIP**. Then **extract** the ZIP (on Windows: right-click →
  "Extract All..."). Opening the ZIP by double-clicking is *not* the same as extracting.
- **If you know git**: `git clone https://github.com/nobufumi-tego/wifi-csi-kids-lab.git`

## Step 2. Start the lab with one click

| Computer | What to do |
|---|---|
| Windows | Double-click **`start.bat`** in the lab folder |
| Mac / Linux | Open a terminal in the lab folder and type `./start.sh` |
| Any (if uv is already installed) | `uv run lab.py` |

The start script installs **uv** if needed, then everything the lab uses (one
`uv sync` installs it all), then opens **JupyterLab** in your browser.
The first time takes a few minutes. Please wait and don't press Ctrl+C.

**To stop the lab:** click the terminal window and press **Ctrl+C twice**. Closing
the browser tab does not stop it.

## What is a terminal?

A terminal is a window where you **type commands** instead of clicking. You type one
line, press Enter, and the computer answers. For example:

```bash
uv run csi-lab samples
```

means "using uv, run the lab's tool `csi-lab` and make sample recordings".
Don't worry about remembering commands. The lessons tell you what to type, and you
can always ask your AI what a command does **before** you run it.

## What is uv?

**uv** is a helper that prepares Python for you. It installs the right version of
Python and all the packages (NumPy, pandas, matplotlib, scikit-learn, JupyterLab…)
into a folder called `.venv` inside the lab. It does not change the rest of your computer.

| Command | What it does |
|---|---|
| `uv sync` | Install or update everything the lab needs |
| `uv run <something>` | Run a program using the lab's Python |
| `uv run lab.py` | Open JupyterLab |

## JupyterLab basics

JupyterLab opens in your browser. It shows pages and runnable code side by side.

- **File browser** (left side): click folders to open them. Each chapter has a
  `notebooks/` folder.
- **`.md` pages** open as nicely formatted pages (you can read the whole lab here).
- **`.ipynb` notebooks** have cells. Click a cell and press **Shift+Enter** to run it
  and move to the next one. Run cells from top to bottom.
- If something gets strange, use **Kernel → Restart Kernel and Run All Cells**.

## When you see an error

Errors look scary, but they are **messages that help you**. Read them from the
**bottom**: the last line usually says what went wrong.

```text
FileNotFoundError: file not found: data/samples/walk.csv
```

This one means the file is not there yet. Maybe you forgot `uv run csi-lab samples`.
If you are stuck, copy the **whole** error and show it to your AI study buddy
([0-3](03_learning_with_ai.md) explains how to ask).

> 🤖 **Ask your AI**
> - "What does `uv sync` do? Explain it like I'm 11."
> - "Here is my error message: ... What does the last line mean? Give me a hint first."

## Check yourself

1. How do you stop JupyterLab?
2. How do you run one cell in a notebook?
3. Where should you start reading an error message?

<details><summary>Answers</summary>

1. Press Ctrl+C twice in the terminal window. Closing the browser tab is not enough.
2. Click the cell and press Shift+Enter.
3. At the bottom. The last line usually says what went wrong.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- [Terminal basics with Penta the penguin](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/README.md)
- [What uv does](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/08_uv_keeps_pet_healthy.md)
- [How to read error messages](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/columns/05_reading_errors.md)
- [JupyterLab beginner's guide](https://github.com/nobufumi-tego/learning-math/blob/main/docs/jupyter_lab_guide.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [0-1. What is Wi-Fi sensing?](01_what_is_wifi_sensing.md) | [Chapter 0](README.md) | [Home](../README.md) | [0-3. Learning with AI](03_learning_with_ai.md) |
