English | [日本語](safety.ja.md)

# Safety guide

Read this with a guardian **before Level 3** (building and recording).

## 1. Electricity

- Power the boards **only by USB**, from a computer or a USB power adapter.
- Do not connect the boards to wall sockets, loose batteries, or other power sources.
  Do not open power adapters.
- **Don't touch the metal pins** while the board is powered. Put the board on a dry,
  non-metal surface (not on coins, foil, or tools), so the pins cannot touch each other.
- Boards can get **warm**. If a board gets hot or smells strange, unplug it right away
  and tell an adult.
- **Unplug the boards** when you are done.

## 2. Radio law in Japan (技適 / 電波法)

In Japan, devices that send radio waves must be certified. Certified devices carry
the **技適 mark** (a symbol like 〒 inside a circle, with a number).

- Use only ESP32 boards whose **radio module shows the 技適 mark**. Check before
  buying, and check the board itself.
- Boards bought from overseas shops often **do not** have the mark. Don't use them
  for this lab.
- **Don't modify** the board: no extra antennas, no cutting or soldering the
  antenna, and no settings that raise the transmit power. Use the firmware in this
  repository as it is.
- If you are not sure, stop and ask a guardian.

## 3. Privacy and consent

Wi-Fi sensing can tell **whether someone is there and what they are doing**, even
without a camera. That is why it needs care.

- **Ask everyone in the room** before recording, and record only people who agree.
  Tell them what you are measuring.
- **Never** aim your setup at neighbors, other homes, or places where people do not
  know about it. Don't try to "see through walls" into someone else's space.
- **Keep recordings on your own computer.** They go in `data/`, which git ignores.
  Don't upload them or send them to others.
- Don't write real names, addresses, or school names in file names or notes.
  Use labels like `person-A` or `room-1`.

## 4. Sharing your results

- Share **graphs and numbers**, not raw recordings of people.
- No names, faces, addresses, or photos that show where you live.
- Say clearly whether your data is **simulated** (pretend) or **real**.

If something feels unsafe or wrong, stop and ask an adult. That is always the right choice.
