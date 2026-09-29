English | [日本語](04_troubleshooting.ja.md)

# 3-4. Troubleshooting — when something does not work

Things go wrong in every real experiment. Read the message, check one thing at a time,
and write down what you tried.

## Common problems

| Problem | What to check |
|---|---|
| The computer does not see the board (no port) | Use a data cable, not a charge-only cable. Some boards need a USB driver: **CP210x** or **CH340**, depending on the chip next to the USB connector. |
| Upload fails ("Failed to connect") | Hold the **BOOT** button on the board while the upload starts, and let go when you see "Writing…". |
| `No USB serial port found` | Is R plugged in with a data cable? Try another USB port on the computer. |
| `Several ports found` | More than one board is plugged in. Add `--port <name>` (find names with `uv run csi-lab ports`). |
| `Cannot open <port>` | Close the Arduino Serial Monitor or any other program using the port. |
| `No CSI data for 5 s` | Is S powered on, with its LED blinking once per second? Were both boards programmed with this lab's firmware (S = `csi_tx`, R = `csi_rx`)? |
| R's Serial Monitor shows `# still waiting for csi_tx` | S is not reaching R. Check S's power and LED, move the boards closer, and check that both programs use the same channel (`WIFI_CHANNEL`, 11). |
| An LED blinks very fast all the time | Setup failed. Open the Serial Monitor (921600 for R, 115200 for S) and read the line starting with `# ERROR`. |
| Fewer than about 90 packets per second | Move the boards closer, and keep them away from busy Wi-Fi devices and microwave ovens. |

At the end of a recording, `capture` prints how many packets it got per second and how
many broken lines it skipped. A few broken lines are normal.

## Reading error messages

An error message is a letter from the computer telling you what went wrong. Copy the
**whole** message (not just "it doesn't work") before asking for help.

> 🤖 **Ask your AI**
> - "Here is the full error message and the command I ran: … What does it mean, and what
>   should I check first? Don't fix everything at once, one step at a time."
> - "My recording has only 60 packets per second. List possible reasons, from most to
>   least likely."

## Check yourself

1. The computer does not see the board at all. What is the first thing to try?
2. `capture` says `Cannot open port`. What is probably using the port?
3. Why should you copy the whole error message when asking for help?

<details><summary>Answers</summary>

1. Another USB cable (it may be charge-only). Then the USB driver (CP210x or CH340).
2. Another program, often the Arduino Serial Monitor.
3. The details (which command, which port, which line) tell a helper, or an AI, what
   really happened.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [3-3. Record](03_record.md) | [Chapter 3](README.md) | [Home](../README.md) | [Chapter 4. Find motion](../04_analysis/README.md) |
