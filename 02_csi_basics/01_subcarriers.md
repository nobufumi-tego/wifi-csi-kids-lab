English | [日本語](01_subcarriers.ja.md)

# 2-1. Subcarriers — Wi-Fi is a highway with 56 lanes

In Chapter 1 we talked about "the" Wi-Fi wave. Actually, Wi-Fi sends many small waves
side by side. On this page you will meet these "lanes", and see why having many of them
is great for sensing.

## One channel, many lanes

Wi-Fi uses a **channel**: a slice of radio frequencies 20 MHz wide. It splits that slice
into many narrow **lanes**, like a highway with many lanes. Each lane carries its own
small wave. The lanes are called **subcarriers**, and this way of sending is called
**OFDM** (Orthogonal Frequency-Division Multiplexing — you do not need to remember the
long name).

```text
frequency ->
 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
-28 ...            -1   (0)  1              ...          28
                         ^ the center lane is left empty
```

- Neighboring lanes are **312.5 kHz** apart.
- In this lab we use **56 lanes**, numbered −28 to −1 and 1 to 28. Lane 0 in the middle
  is not used.
- On channel 11 (center 2.462 GHz), lane −28 is at about 2.4533 GHz and lane +28 at
  about 2.4708 GHz ($2.462\ \text{GHz} \pm 28 \times 312.5\ \text{kHz}$).

## Each lane sees the room a little differently

Each lane has a slightly different frequency, so a slightly different wavelength
($\lambda = c/f$ from [1-2](../01_waves/02_wavelength_and_frequency.md)). On
[1-4](../01_waves/04_interference.md) you saw that the same room paths can **help** on
one lane and **cancel** on another. So every lane arrives with its own size.

That is good news for sensing: instead of one number, we get **56 views** of the same
room at the same moment.

> 🤖 **Ask your AI**
> - "Why does Wi-Fi split its channel into many small lanes instead of using one big
>   wave? Explain like I'm 11."
> - "If lanes are 312.5 kHz apart, how wide are 56 lanes together? Let me calculate,
>   then check my answer."
> - "Why is the center lane (number 0) not used?"

## Check yourself

1. What are the small waves inside one Wi-Fi channel called?
2. How many lanes do we use in this lab, and which number is skipped?
3. Why do different lanes arrive with different sizes?

<details><summary>Answers</summary>

1. Subcarriers.
2. 56 lanes (−28 to −1 and 1 to 28). Lane 0 is skipped.
3. Each lane has a slightly different wavelength, so the room's paths help or cancel
   differently on each lane.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Chapter 2](README.md) | [Chapter 2](README.md) | [Home](../README.md) | [2-2. What is CSI?](02_what_is_csi.md) |
