English | [日本語](02_what_is_csi.ja.md)

# 2-2. What is CSI? — 56 numbers instead of 1

Your phone shows Wi-Fi strength as a few bars. The receiver in this lab measures much
more. On this page you will find out what CSI is, and how it compares with the familiar
signal strength.

## CSI: how each lane arrived

**CSI** stands for **Channel State Information**. For every packet (a small chunk of
data sent by radio) the receiver measures how each lane arrived:

- **Amplitude**: how big the wave is when it arrives. **This is what we use.**
- **Phase**: where in its up-and-down the wave is when it arrives. It exists, but a
  low-cost receiver with one antenna (like the ESP32) mixes in its own timing errors, so
  phase is hard to use. We skip it here.

For each lane, the ESP32 actually reports **two whole numbers**, often written as a pair
$(a, b)$ or as one "complex number" $a + bi$. You can think of them as an arrow on a map:
the arrow's **length** is the amplitude, and its **direction** is the phase. The length
comes from Pythagoras again:

$$
\text{amplitude} = \sqrt{a^2 + b^2}
$$

Our receiver program does this calculation for you and sends only the amplitudes.

## RSSI vs CSI

**RSSI** (Received Signal Strength Indicator) is what your phone uses for the Wi-Fi
bars: one number for the whole packet.

| | RSSI | CSI (in this lab) |
|---|---|---|
| Numbers per packet | 1 (total strength) | 56 (one amplitude per lane) |
| What it is like | "How loud was the whole song?" | "How loud was each instrument?" |
| Good for | Is the signal strong? | *How* did the room change the signal? |

With 56 numbers instead of 1, CSI can notice small changes that RSSI misses.

## What does dBm mean?

RSSI is written in **dBm**, for example `-52`. Radio signals range from strong to
incredibly weak, so engineers use a scale that counts "how many times ten":

| dBm | Power | Compared with 0 dBm |
|---|---|---|
| 0 dBm | 1 mW (one thousandth of a watt) | same |
| −10 dBm | 0.1 mW | 10 times weaker |
| −20 dBm | 0.01 mW | 100 times weaker |
| −50 dBm | 0.00001 mW | 100,000 times weaker |

Every −10 means "ten times weaker". So **closer to 0 = stronger**. A Wi-Fi signal
around −50 dBm is a good, strong signal for these experiments.

## A recording is a table

Each packet becomes one row. A recording is a table with **one row per packet** and
**one column per lane** — in math, a table of numbers like this is called a
**matrix**. You will open one on the next page.

> 🤖 **Ask your AI**
> - "What is the difference between RSSI and CSI? Use a music or orchestra example."
> - "Explain dBm to me with sound volume. Why do engineers count 'times ten' instead of
>   just writing the power?"
> - "What is a complex number? Explain it as an arrow on a map, for a middle-school
>   student."

## Check yourself

1. RSSI gives one number per packet. How many does CSI give in this lab?
2. Which one is stronger: −45 dBm or −70 dBm?
3. Why do we skip the phase and use only the amplitude?

<details><summary>Answers</summary>

1. 56: one amplitude per lane.
2. −45 dBm (closer to 0 = stronger).
3. With one antenna, the ESP32's own timing errors mix into the phase, so it is hard to
   use. The amplitude is easier and still shows movement.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Logarithms and decibels (dB): [対数](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/04_logarithm.md)
- Basic symbols (including complex numbers ℂ): [基本記号](https://github.com/nobufumi-tego/learning-math/blob/main/00_notation/01_basic_symbols.md)
- Matrices: numbers in a table: [行列](https://github.com/nobufumi-tego/learning-math/blob/main/01_linear_algebra/02_matrices.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [2-1. Subcarriers](01_subcarriers.md) | [Chapter 2](README.md) | [Home](../README.md) | [2-3. Look at the data](03_look_at_data.md) |
