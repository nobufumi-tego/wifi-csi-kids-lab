English | [日本語](02_flash_firmware.ja.md)

# 3-2. Upload the firmware — turn the boards into S and R

A **firmware** is the program that runs inside a board. You will put the sender program
on board S and the receiver program on board R.

> 👪 Installing software: ask a grown-up to help.

## 1. Install the software

1. Install **Arduino IDE 2** from the official Arduino website.
2. Open **Boards Manager** (the board icon on the left), search for **esp32**, and install
   **"esp32 by Espressif Systems"**.
3. Put tape on each board. Write **S** on one and **R** on the other.

## 2. Program board S (the sender)

1. Plug in board **S** only.
2. In Arduino IDE, open [`firmware/csi_tx/csi_tx.ino`](../firmware/csi_tx/csi_tx.ino).
3. Choose the board: **Tools → Board → esp32 → ESP32 Dev Module**.
4. Choose the port: **Tools → Port** (the one that appears when you plug in the board).
5. Click **Upload** (the → arrow).
6. When it finishes, the blue LED (on pin GPIO2, if your board has one) blinks
   **once per second**. That means S is sending.

## 3. Program board R (the receiver)

1. Unplug S. Plug in board **R**.
2. Open [`firmware/csi_rx/csi_rx.ino`](../firmware/csi_rx/csi_rx.ino), choose the same
   board and the new port, and click **Upload**.
3. Power S again (from the computer or a power bank). R's LED blinks about once per
   second while it receives packets from S.

## 4. Optional check: the Serial Monitor

Open **Tools → Serial Monitor** and set the speed to **921600**. You should see:

- a message line like `# csi_rx ready: channel 11, waiting for csi_tx...`
- many lines starting with `CSI,` (one per packet)
- every 5 seconds a status line starting with `#`

If you only see `# still waiting for csi_tx`, S is not reaching R. See
[3-4. Troubleshooting](04_troubleshooting.md).

**Close the Serial Monitor before the next page.** Only one program can use the port at
a time.

## What the LED tells you

| Board | LED | Meaning |
|---|---|---|
| S | blinks once per second | sending |
| R | blinks about once per second | receiving packets from S |
| S or R | blinks very fast, all the time | setup failed; the Serial Monitor shows a line starting with `# ERROR` |

> ℹ️ The firmware is checked to compile with Arduino-ESP32 core **2.0.17**. It is written to
> also work with core **3.x** (the current Arduino IDE default), but that has **not been
> tested yet**. If it fails, tell a grown-up and report it as an issue on GitHub.

> 🤖 **Ask your AI**
> - "My ESP32 upload fails with 'Failed to connect'. Here is the full error: … Walk me
>   through what to check, one step at a time."
> - "What is firmware? How is it different from an app on a phone?"

## Check yourself

1. Which program goes on S, and which on R?
2. Why must you close the Serial Monitor before recording?
3. R's Serial Monitor only shows `# still waiting for csi_tx`. What is the first thing to check?

<details><summary>Answers</summary>

1. `csi_tx` on S (sender), `csi_rx` on R (receiver).
2. Only one program can use the port. The recording tool cannot open it while the Serial
   Monitor is using it.
3. Is S powered on, with its LED blinking once per second?

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [3-1. Parts](01_parts.md) | [Chapter 3](README.md) | [Home](../README.md) | [3-3. Record](03_record.md) |
