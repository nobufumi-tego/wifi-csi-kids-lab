English | [日本語](03_learning_with_ai.ja.md)

# 0-3. Learning with AI — a study buddy that is not always right

An AI tool can be a great study buddy. It is patient, and you can ask it anything.
But it is **not always right**, and it learns nothing *for* you. You do the learning.

## Ask good questions

A good question tells the AI **what you tried**, **what happened**, and **what you
expected**. Paste the full error message.

| Not so good | Better |
|---|---|
| "It doesn't work." | "I ran `uv run csi-lab show data/samples/walk.csv` and got `FileNotFoundError`. I expected a picture. What should I check?" |
| "Explain CSI." | "I read Chapter 2. I understand amplitude, but why is it different on each subcarrier?" |
| "Do my free research." | "I want to test if a water bottle changes CSI. Can you help me plan an experiment? Don't tell me the answer yet." |

More prompts you can try:

- "Give me a hint, not the answer."
- "Explain this line of code like I'm 11."
- "Ask me three questions to check that I understand Chapter 1."
- "What could go wrong in this experiment, and how could I check it?"

## Shortcut commands for AI tools

If you use **Claude Code** or **Gemini CLI** inside this lab folder, you can type these
shortcuts (the same names work in both):

| Command | What it does |
|---|---|
| `/explain-simply <topic>` | Explains a topic with everyday examples and no hard math, e.g. `/explain-simply subcarrier` |
| `/check-understanding <topic>` | Asks you questions one at a time to check you really understand, e.g. `/check-understanding wavelength` |
| `/research-buddy` | Helps you plan your free research by asking questions. It does not write the report for you |

Other AI tools also read [`AGENTS.md`](../AGENTS.md), which asks them to act as a tutor.

## Check what the AI says

- **Run the code.** Does it really do what the AI said?
- **Compare with the lessons** and the [glossary](../glossary/README.md).
- **Ask "How do you know?"** A good answer points to something you can check.
- **Try a small test.** For example, change one number and see if the result changes
  the way the AI predicted.
- If the AI and the lesson disagree, tell the AI, and ask a guardian or teacher.

AI can make up numbers, facts, and even websites that don't exist. When a fact
matters (for your report!), check it somewhere else.

## Keep a learning log

Write a few lines each time you study. It helps you remember, and it shows your
teacher how you used AI in your free research.

```text
Date: 2026-08-01
I asked: why does the heat map get stripes when I walk?
I learned: moving changes the length of the bounced path, so the waves mix differently.
I checked myself: recorded "still" and "walk"; stripes only appeared in "walk".
AI mistake I found: none today / (write it if you found one)
```

## Rules to remember

- Don't let AI write your report. Use your own words.
- Don't share names, addresses, or recordings of people with AI tools.
- Some AI services have age rules. Use AI together with a guardian.

> 🤖 **Ask your AI**
> - "Ask me three questions to check that I understand this page."
> - "I think the answer is ... . Am I right? Don't just say yes; tell me how I could check."

## Check yourself

1. What three things make a good question to an AI?
2. The AI tells you a number for your report. What should you do?
3. Why keep a learning log?

<details><summary>Answers</summary>

1. What you tried, what happened, and what you expected (plus the full error message, if there is one).
2. Check it somewhere else: run the code, compare with the lessons, or look it up in a reliable source.
3. It helps you remember, and it shows your teacher how you used AI.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [0-2. Terminal and uv](02_terminal_and_uv.md) | [Chapter 0](README.md) | [Home](../README.md) | [0-4. Safety](04_safety.md) |
