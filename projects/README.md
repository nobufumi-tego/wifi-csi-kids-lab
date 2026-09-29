English | [日本語](README.ja.md)

# Free research projects

Use what you learned to answer **your own question**. This page shows how to plan a
free research project (自由研究), gives ideas, and explains how to report it fairly.

Write-up sheet: [`research-sheet.md`](research-sheet.md)

---

## The seven steps

1. **Question** — What do you want to know? Make it specific.
   ✗ "Is Wi-Fi interesting?" ✓ "Does a person 3 m away change CSI less than a person 1 m away?"
2. **Hypothesis** — What do you think will happen, and **why**?
3. **Plan** — What will you change? What will you keep the same? How many times will you repeat?
4. **Measure** — Record data (with the boards) or simulate it. Write down the conditions every time.
5. **Analyze** — Make graphs and numbers (Levels 4 and 5).
6. **Conclude** — Was your hypothesis right, wrong, or "not sure yet"? All three are OK.
7. **Reflect** — What would you do differently? What new question did you find?

## Project ideas

★ = easy, ★★ = medium, ★★★ = challenging. 🔌 = needs the ESP32 boards (Level 3). 💻 = computer only.

| # | Question | Level | Needs |
|---|---|---|---|
| 1 | How far apart can the two boards be before motion is no longer detected? Is that the same as the distance where the signal is lost? | ★★ | 🔌 |
| 2 | Which blocks Wi-Fi more between the boards: cardboard, a water bottle, or a metal pot? (Water and metal are interesting!) | ★ | 🔌 |
| 3 | Can CSI tell if a door is open or closed? | ★ | 🔌 |
| 4 | Does the motion number get bigger when two people walk instead of one? | ★★ | 🔌 |
| 5 | Does the height or direction of the boards (on the floor, on a desk, standing up, lying flat) change how well motion is detected? | ★★ | 🔌 |
| 6 | Is the signal noisier in the evening, when many people at home use Wi-Fi? | ★★ | 🔌 |
| 7 | Which subcarriers react most when someone walks? Is it always the same ones? | ★★ | 🔌 or 💻 |
| 8 | In the simulator: how short can a breathing recording be and still give the right breathing rate? | ★★ | 💻 |
| 9 | In the simulator: does a detector trained in one room work in another (`room_seed`)? Can you invent a feature that helps? | ★★★ | 💻 |
| 10 | Can machine learning tell walking from waving with **your own** recordings? How does it compare with the simulator? | ★★★ | 🔌 |

> **Ask your AI**
> "I'm in grade 7. Here is my research question: [your question]. Help me make it more
> specific and testable. Ask me questions instead of rewriting it for me."

## Tips for a fair test

- **Change only one thing at a time.** If you change the distance *and* the room, you
  can't know which one made the difference.
- **Repeat at least 3 times** for each condition. One recording can be a lucky (or unlucky) one.
- **Record the conditions** every time: date and time, distance between boards, height,
  what was between them, how many people were in the room, the file name.
- **Keep a "nothing moves" recording** in every session — it is your baseline for the threshold.
- **Don't delete "bad" data** just because it doesn't match your hypothesis. If something
  went wrong (someone walked in), write it down instead.

## Being fair to people (ethics)

- **Ask first.** Only record people who agreed, and tell them what you are measuring.
  Wi-Fi sensing works through walls — never measure people who don't know about it.
- **No names in files or reports.** Use "Person A", "Person B".
- **Don't share recordings of your home** on the internet. Share graphs and numbers instead.
- Ask a parent or teacher to check your plan before you start.

## Reporting how you used AI

Using an AI study buddy is fine — hiding it is not. In your report, write:

- **What the AI helped with** (e.g. "explained standard deviation", "found a bug in my code").
- **What you checked yourself** (e.g. "I ran the code and compared with my own graph").
- **What you decided yourself** (your question, your hypothesis, your conclusion).
- If the AI said something wrong, write that too — finding it is a skill!

Also ask your school whether they have rules about using AI for free research.
