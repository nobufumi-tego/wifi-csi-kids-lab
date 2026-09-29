English | [日本語](02_project_ideas.ja.md)

# 6-2. Project ideas — ten questions to start from

Pick one of these, change it, or use it as a spark for your own question. Your own
question is always the best one.

★ = easy, ★★ = medium, ★★★ = challenging.
🔌 = needs the ESP32 boards ([Chapter 3](../03_build/README.md)). 💻 = computer only.

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

Where to start for each idea:

- Ideas 1–7 and 10: record with the boards ([Chapter 3](../03_build/README.md)) and compare
  motion numbers ([4-1](../04_analysis/01_motion_number.md)).
- Idea 8: breathing rate ([4-4](../04_analysis/04_breathing.md)).
- Ideas 9 and 10: machine learning, especially the new-room test ([5-4](../05_machine_learning/04_new_room.md)).

Before you start, read [6-1. How to do research](01_how_to_do_research.md) and make
sure everyone you record has agreed.

> 🤖 **Ask your AI**
> - "I like idea 2 (things that block Wi-Fi). What could I change and what should I keep the same? Ask me questions first."
> - "I want to change idea 3 into my own question about [something at home]. Help me make it testable without writing it for me."

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [6-1. How to do research](01_how_to_do_research.md) | [Chapter 6](README.md) | [Home](../README.md) | [6-3. Research sheet](research_sheet.md) |
