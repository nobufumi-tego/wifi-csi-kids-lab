English | [日本語](README.ja.md)

# Wi-Fi CSI Kids Lab

**Can Wi-Fi "feel" you move?** Wi-Fi radio waves bounce around your room. When you
walk, wave your hand, or even breathe, the waves change a tiny bit. A Wi-Fi chip can
measure those changes as **CSI (Channel State Information)**. This lab shows you how
to see those changes and study them. You start with the basics of radio waves and end
with your own free-research project, using Python and your first machine learning.

It is made for learners aged about **10 to 15**, working with a guardian and an
**AI study buddy** (a generative AI tool).

## The learning path

| Level | Topic | What you need |
|---|---|---|
| [1 · Waves](lessons/1-waves/README.md) | What are radio waves? Why do they bounce and mix? | A computer |
| [2 · CSI basics](lessons/2-csi-basics/README.md) | Look at CSI data with Python (pretend data) | A computer |
| [3 · Build](lessons/3-build/README.md) | Set up two ESP32 boards and record your own CSI | Two ESP32 boards + USB cables |
| [4 · Analysis](lessons/4-analysis/README.md) | Turn CSI into a "motion number" and detect movement | A computer (+ your recordings) |
| [5 · Machine learning](lessons/5-machine-learning/README.md) | Teach a computer to tell "empty / still / walking" apart | A computer |

You can do Levels 1, 2, 4 and 5 **without any hardware**. The simulator makes
pretend recordings for you. When you want to measure real data, do Level 3.

## Start in 5 minutes (no hardware needed)

1. Install **uv**, a tool that sets up Python for you:
   <https://docs.astral.sh/uv/getting-started/installation/>
   (ask a guardian to help with installing software).
2. Open a terminal in this folder and run:

   ```bash
   uv sync                                   # install everything this lab needs
   uv run csi-lab samples                    # make pretend recordings in data/samples/
   uv run csi-lab show data/samples/walk.csv # draw one and save walk.png
   ```

3. Open `data/samples/walk.png`. The stripes in the top picture show a person walking.
4. Want notebooks (code and notes in your browser)?

   ```bash
   uv sync --extra notebook
   uv run jupyter lab notebooks/
   ```

> **Note:** The pretend (synthetic) data comes from a simple model of a room. Real
> rooms are messier, so your own recordings will look noisier. That is normal, and
> it is part of the fun.

## Learning with AI

Open this folder in an AI coding tool, for example **Claude Code**, **Codex**, or
**Gemini CLI**. These tools read [`AGENTS.md`](AGENTS.md), which tells the AI to act
as a **tutor**: it asks what you think, gives hints before answers, and keeps you
safe. Read [Learning with AI](guides/learning-with-ai.md) for tips on asking good
questions.

## More

- [Safety guide](guides/safety.md): electricity, radio law in Japan (技適), and privacy. **Read this before Level 3.**
- [For parents and teachers](guides/for-parents-and-teachers.md)
- [Free-research project ideas](projects/README.md)
- [Glossary](glossary.md): words used in the lessons
- [About the data folder](data/README.md)
- [Contributing](CONTRIBUTING.md)

## License

- Code (`src/`, `tests/`, `firmware/`, `notebooks/` code cells): **MIT**. See [LICENSE](LICENSE).
- Lessons, guides and other documents: **CC BY 4.0**. See [LICENSE-docs](LICENSE-docs).
