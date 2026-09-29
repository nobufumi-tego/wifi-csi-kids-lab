English | [日本語](README.ja.md)

# The `data/` folder

This folder holds recordings on **your computer only**. Everything here, except these
two README files, is ignored by git, so it is never uploaded.

| Folder | What goes in | How it gets there |
|---|---|---|
| `data/samples/` | Pretend (simulated) recordings: `empty`, `still`, `walk`, `breathe`, `wave`, and `story` | `uv run csi-lab samples` |
| `data/my-recordings/` | Your own recordings from the ESP32 receiver | `uv run csi-lab capture --label <name>` |

Each file is a CSV (open it in Python, or even a spreadsheet app). One row is one
packet: `time_s`, `rssi_dbm`, `label`, then the amplitude of 56 subcarriers (`sc-28` … `sc28`).

**Never share recordings of people.** Wi-Fi recordings can show when someone was
home and what they were doing. Share graphs and numbers instead, and only with the
agreement of the people you recorded. See the [safety page](../start_here/04_safety.md).

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Home](../README.md) | [Home](../README.md) | [Home](../README.md) | [Home](../README.md) |
