English | [日本語](03_record.ja.md)

# 3-3. Record — your first real CSI

Set up the room, record "nobody moving" and "walking", and draw them.

> 💡 **Run the commands on this page** in a terminal opened in this lab's folder.
> New to the terminal? → [0-2. Terminal and uv](../start_here/02_terminal_and_uv.md)

## 1. Set up the room

- Place S and R about **3 m apart**, at the **same height** (for example, on two chairs
  or shelves), with nothing blocking the straight line between them.
- Keep the setup **the same** for all recordings you want to compare.
- Tell everyone in the room what you are doing and **ask them first**. Wi-Fi sensing can
  tell what people are doing, so it needs their "yes" (see [0-4. Safety](../start_here/04_safety.md)).

Plug R into the computer. S can be powered by the computer or a power bank.

## 2. Find the port

```bash
uv run csi-lab ports
```

If only one board is connected, `capture` finds it automatically. If there are several,
add `--port <name>` (for example `--port COM3` or `--port /dev/ttyUSB0`).

## 3. Record an empty room first

Leave the room (or sit still, far from the line between S and R), then run:

```bash
uv run csi-lab capture --label empty --seconds 30
```

The file is saved in `data/my-recordings/` with the date, time, and label in its name
(see [`data/README.md`](../data/README.md)). Press Ctrl+C to stop early; what was
recorded so far is kept.

Always record "empty" first. It is your **baseline**, the thing you compare everything
else with.

## 4. Record something moving

```bash
uv run csi-lab capture --label walk --seconds 30
```

While it records, walk slowly back and forth across the line between S and R.

## 5. Draw them

```bash
uv run csi-lab show data/my-recordings/<your-file>.csv
```

A picture `<your-file>.png` is saved next to the file. Compare it with the pretend
recordings from [Chapter 2](../02_csi_basics/README.md). What is similar? What is
different? Real data is usually noisier. That is normal.

## 6. Good habits for experiments

- **Change one thing at a time.** If you change the distance *and* the person at the same
  time, you cannot tell which one made the difference.
- **Repeat.** Record each condition at least 3 times.
- **Keep a lab notebook.** For each recording write:

| Write down | Example |
|---|---|
| date and time | 2026-08-01 14:05 |
| place (never your address) | living room |
| distance and height of S and R | 3 m, both 70 cm |
| who was in the room, and that they agreed | me (agreed), my brother (agreed) |
| what happened | walked across the line 5 times |
| anything unusual | the door opened at about 20 s |

> 🤖 **Ask your AI**
> - "I want to find out if a closed door changes CSI. Help me plan a fair experiment:
>   what should I keep the same, and what should I change?"
> - "Here is my lab notebook entry: … What important information is missing?"

## Check yourself

1. Why should you record "empty" first?
2. You moved the boards closer *and* opened a window, and the CSI changed. What is the
   problem with this experiment?
3. Why do you ask people in the room before recording?

<details><summary>Answers</summary>

1. It is the baseline. You need to know what "nothing moving" looks like in *this* room
   before you can say something changed.
2. Two things changed at once, so you cannot tell which one caused the change.
3. Wi-Fi sensing can reveal what people are doing. Recording people without asking is
   not fair to them.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [3-2. Upload the firmware](02_flash_firmware.md) | [Chapter 3](README.md) | [Home](../README.md) | [3-4. Troubleshooting](04_troubleshooting.md) |
