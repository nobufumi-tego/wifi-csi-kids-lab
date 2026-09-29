English | [日本語](README.ja.md)

# Chapter 3: Build — your own sender and receiver

Program two ESP32 boards, one as a **sender (S)** and one as a **receiver (R)**, and
record real CSI in your own room.

> 👪 **Do this chapter with a parent, guardian, or teacher.** Read
> [0-4. Safety](../start_here/04_safety.md) together before you start.

> ✅ **This chapter is optional.** Chapters 4 and 5 work with pretend recordings from the
> simulator, so you can skip ahead and come back when you have the boards.

## What you will be able to do

- Explain how the two boards and the computer talk to each other
- Upload a program (firmware) to an ESP32 board with Arduino IDE
- Record CSI with `uv run csi-lab capture` and draw it with `uv run csi-lab show`
- Keep a lab notebook so your experiments are fair and repeatable

**Who:** with a grown-up · **Time:** about 2 hours (installing the software the first
time takes the longest)

## Pages

| # | Page | What you learn |
|---|---|---|
| 3-1 | [`01_parts.md`](01_parts.md) | What to buy, the 技適 (Giteki) mark, how the boards talk |
| 3-2 | [`02_flash_firmware.md`](02_flash_firmware.md) | Install Arduino IDE 2 and upload `csi_tx` to S and `csi_rx` to R |
| 3-3 | [`03_record.md`](03_record.md) | Set up the room and make your first real recordings |
| 3-4 | [`04_troubleshooting.md`](04_troubleshooting.md) | What to check when something does not work |

## Notebooks

This chapter uses the Arduino IDE and the terminal, not notebooks. Once you have your
own recordings, you can open them in the notebook of [Chapter 4](../04_analysis/README.md)
with `load_csv`.

## Firmware

The two programs are in [`firmware/`](../firmware/README.md):
[`csi_tx.ino`](../firmware/csi_tx/csi_tx.ino) (sender) and
[`csi_rx.ino`](../firmware/csi_rx/csi_rx.ino) (receiver).

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [2-4. Automatic gain](../02_csi_basics/04_automatic_gain.md) | [Chapter 3](README.md) | [Home](../README.md) | [3-1. Parts](01_parts.md) |
