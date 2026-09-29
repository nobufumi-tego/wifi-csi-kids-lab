English | [日本語](README.ja.md)

# Wi-Fi CSI Kids Lab

[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey.svg)](LICENSE-DOCS)
[![CI](https://github.com/nobufumi-tego/wifi-csi-kids-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/nobufumi-tego/wifi-csi-kids-lab/actions/workflows/ci.yml)

**Can Wi-Fi notice that you moved?** Wi-Fi waves bounce around a room. When someone
walks, waves a hand, or even breathes, the waves change a tiny bit — and a Wi-Fi chip
can measure that as **CSI (Channel State Information)**.

In this lab you start from what radio waves are, look at CSI data with Python, try
your first machine learning, and finish with **your own free-research project
(自由研究)**. It is made for learners about **10–15 years old in Japan**, working with a
guardian and an **AI study buddy** (generative AI).

> ⚠️ **Please read first:** this material was written by an individual together with
> generative AI and has **not been reviewed by experts**. It may contain mistakes. The
> practice data comes from a simplified simulator. See [DISCLAIMER](DISCLAIMER.md).

## What you can do here

- Understand radio waves, reflection and interference with pictures and a little Python
- See CSI for yourself: 56 numbers per Wi-Fi packet, and how movement changes them
- Build a sender and receiver from two ESP32 boards (optional, with a guardian)
- Make a motion detector, then teach a computer to tell "empty / still / walking" apart
- Turn it into a fair, honest free-research project

---

## 🚀 Start in 3 minutes (no hardware needed)

### Step 1: get this folder

- **Easy:** on the GitHub page, click the green **`<> Code`** → **Download ZIP**, then
  **extract** it (right-click → "Extract All..." on Windows). Opening the ZIP without
  extracting will not work.
- **With git:** `git clone https://github.com/nobufumi-tego/wifi-csi-kids-lab.git`

### Step 2: start the lab

| Computer | How to start |
|---|---|
| **Windows** | double-click [`start.bat`](start.bat) |
| **Mac / Linux** | open a terminal in the folder and run `./start.sh` |

The script installs **uv** if needed, installs everything with `uv sync`, and opens
JupyterLab in your browser with this page. **The first time takes several minutes** —
please wait and do not press Ctrl+C. To stop the lab, press **Ctrl+C twice** in the
terminal window. (Ask a grown-up to help the first time.)

<details><summary>Prefer typing commands? / trouble?</summary>

```bash
uv sync                                    # install everything (once)
uv run csi-lab samples                     # make practice recordings in data/samples/
uv run csi-lab show data/samples/walk.csv  # draw one → data/samples/walk.png
uv run lab.py                              # start JupyterLab
```

More help: [0-2. Terminal and uv](start_here/02_terminal_and_uv.md).
</details>

---

## 🎯 Where to start

| You are... | Start here |
|---|---|
| New to all of this | [Chapter 0: Start here](start_here/README.md) |
| Curious about waves | [Chapter 1: Waves](01_waves/README.md) |
| Want to see data right away | [2-3. Look at the data](02_csi_basics/03_look_at_data.md) |
| Have two ESP32 boards and a grown-up | read [0-4. Safety](start_here/04_safety.md), then [Chapter 3: Build](03_build/README.md) |
| Planning a free-research project | [Chapter 6: Free research](06_free_research/README.md) |
| A parent or teacher | [For parents and teachers](docs/for_parents_and_teachers.md) |

Chapters 1, 2, 4 and 5 work **without hardware** (a simulator makes practice data).
The full list with target grades: [Learning path](docs/learning_path.md).

---

## 📚 All pages

### 🌱 [Chapter 0: Start here](start_here/README.md)

| Page |
|---|
| [0-1. What is Wi-Fi sensing? — Wi-Fi that notices you moved](start_here/01_what_is_wifi_sensing.md) |
| [0-2. Terminal and uv — opening the lab](start_here/02_terminal_and_uv.md) |
| [0-3. Learning with AI — a study buddy that is not always right](start_here/03_learning_with_ai.md) |
| [0-4. Safety — electricity, radio rules, and privacy](start_here/04_safety.md) |

📖 Columns (reading): [Column 1. Wi-Fi that notices people — why it needs care](start_here/columns/01_sensing_and_privacy.md)

### 🌊 [Chapter 1: Waves — how radio travels](01_waves/README.md)

| Page |
|---|
| [1-1. Radio waves — invisible waves all around you](01_waves/01_radio_waves.md) |
| [1-2. Wavelength and frequency — how long is one Wi-Fi wave?](01_waves/02_wavelength_and_frequency.md) |
| [1-3. Reflection and paths — Wi-Fi takes many roads at once](01_waves/03_reflection_and_paths.md) |
| [1-4. Adding waves (interference) — why a moving person changes Wi-Fi](01_waves/04_interference.md) |

🧪 Notebooks (run them): [`01_waves.ipynb`](01_waves/notebooks/01_waves.ipynb)
📖 Columns (reading): [Column 1: Why 2.4 GHz? — Wi-Fi's noisy neighborhood](01_waves/columns/01_why_2_4ghz.md)

### 📶 [Chapter 2: CSI basics — look at the data](02_csi_basics/README.md)

| Page |
|---|
| [2-1. Subcarriers — Wi-Fi is a highway with 56 lanes](02_csi_basics/01_subcarriers.md) |
| [2-2. What is CSI? — 56 numbers instead of 1](02_csi_basics/02_what_is_csi.md) |
| [2-3. Look at the data — make pretend recordings and draw them](02_csi_basics/03_look_at_data.md) |
| [2-4. Automatic gain — why we divide by the average first](02_csi_basics/04_automatic_gain.md) |

🧪 Notebooks (run them): [`01_look_at_csi.ipynb`](02_csi_basics/notebooks/01_look_at_csi.ipynb)

### 🔧 [Chapter 3: Build — your own sender and receiver](03_build/README.md)

| Page |
|---|
| [3-1. Parts — what you need and how the boards talk](03_build/01_parts.md) |
| [3-2. Upload the firmware — turn the boards into S and R](03_build/02_flash_firmware.md) |
| [3-3. Record — your first real CSI](03_build/03_record.md) |
| [3-4. Troubleshooting — when something does not work](03_build/04_troubleshooting.md) |


### 🔍 [Chapter 4: Find motion — build a motion detector](04_analysis/README.md)

| Page |
|---|
| [4-1. A number for motion — normalize, then measure the wobble](04_analysis/01_motion_number.md) |
| [4-2. Deciding with a threshold — and counting right answers](04_analysis/02_threshold.md) |
| [4-3. What goes wrong — and why](04_analysis/03_what_goes_wrong.md) |
| [4-4. Finding breathing — can Wi-Fi see a slow rhythm?](04_analysis/04_breathing.md) |

🧪 Notebooks (run them): [`01_motion_detector.ipynb`](04_analysis/notebooks/01_motion_detector.ipynb)

### 🤖 [Chapter 5: Your first machine learning](05_machine_learning/README.md)

| Page |
|---|
| [5-1. Features and labels — turning a recording into a table](05_machine_learning/01_features_and_labels.md) |
| [5-2. Training and testing — why we never test on the practice questions](05_machine_learning/02_train_and_test.md) |
| [5-3. Decision tree — a model you can read](05_machine_learning/03_decision_tree.md) |
| [5-4. A new room — the hard, honest test](05_machine_learning/04_new_room.md) |

🧪 Notebooks (run them): [`01_first_machine_learning.ipynb`](05_machine_learning/notebooks/01_first_machine_learning.ipynb)

### 🔬 [Chapter 6: Free research](06_free_research/README.md)

| Page |
|---|
| [6-1. How to do research — seven steps to a fair answer](06_free_research/01_how_to_do_research.md) |
| [6-2. Project ideas — ten questions to start from](06_free_research/02_project_ideas.md) |
| [6-3. Research sheet — write up your free research](06_free_research/research_sheet.md) |


### 📎 Appendix

- [Math map](appendix/math_map.md) — which learning-math page explains the math on each page
- [Appendix](appendix/README.md) — further reading
- [Glossary](glossary/README.md) — words used in the lessons

---

## 🤖 Learning with AI

Open this folder in an AI coding tool (for example **Claude Code**, **Codex**, or
**Gemini CLI**). They read [`AGENTS.md`](AGENTS.md), which asks the AI to act as a
tutor: it asks what you think first, gives hints before answers, and keeps you safe.
Try the commands `/explain-simply <topic>`, `/check-understanding <topic>` and
`/research-buddy <idea>`. Tips: [0-3. Learning with AI](start_here/03_learning_with_ai.md).

## 📐 The math behind it

You do not need math in advance. When you want to go deeper, the
[math map](appendix/math_map.md) links each page to the matching page of
**[learning-math](https://github.com/nobufumi-tego/learning-math)** — a separate course by the same author, written **in Japanese
for adults**. Read it with a grown-up, or come back to it when you are older.

## 🛡️ Safety

Before building anything, read [0-4. Safety](start_here/04_safety.md): USB power only,
boards with the Japanese **技適 mark**, and **only record people who agreed**.
Recordings stay in [`data/`](data/README.md) on your computer and are never committed.

## License

- Code (`src/`, `tests/`, `firmware/`, scripts, notebook code cells): **MIT** — [LICENSE-CODE](LICENSE-CODE)
- Lessons and other documents: **CC BY 4.0** — [LICENSE-DOCS](LICENSE-DOCS)
- Overview: [LICENSE](LICENSE) · Contributing: [CONTRIBUTING](CONTRIBUTING.md)
