English | [日本語](README.ja.md)

# Firmware for the two ESP32 boards

| Folder | Board | What it does |
|---|---|---|
| [`csi_tx/`](csi_tx/csi_tx.ino) | **S** (sender) | Sends a small ESP-NOW broadcast 100 times per second on Wi-Fi channel 11 |
| [`csi_rx/`](csi_rx/csi_rx.ino) | **R** (receiver) | Measures the CSI of each packet from S and sends one text line to the PC |

Step-by-step instructions (with a guardian): [Lesson 3](../lessons/3-build/README.md).

## Quick facts

- Arduino IDE 2 → Boards Manager → "esp32 by Espressif Systems" → board **ESP32 Dev Module**
- No router, no password. Both boards must use the same channel (`WIFI_CHANNEL`, default 11).
- R talks to the PC at **921600** bits per second. Close the Serial Monitor before
  running `uv run csi-lab capture ...` (only one program can use the port).
- Output line of R (56 amplitudes, subcarriers -28..-1 then 1..28):

  ```text
  CSI,<time_us>,<rssi_dbm>,<amp sc-28>,...,<amp sc28>
  ```

  Lines starting with `#` are messages (ready, status, errors).
- R only keeps packets whose content starts with this project's marker, so other
  Wi-Fi devices nearby are ignored.
- Use boards whose module shows the Japanese **技適 (Giteki) mark**. Do not change the
  antenna or transmit power. See [safety](../guides/safety.md).

## Tested

- Compiles with Arduino-ESP32 core 2.0.17 (PlatformIO `espressif32@6.9.0`).
- Written to also compile with core 3.x (the ESP-NOW callback form is chosen by
  version), but this has **not been checked yet**. If it fails, please open an issue.
