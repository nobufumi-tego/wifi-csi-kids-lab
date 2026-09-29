English | [日本語](02_wavelength_and_frequency.ja.md)

# 1-2. Wavelength and frequency — how long is one Wi-Fi wave?

Two numbers describe every wave. On this page you will find them, connect them with one
simple rule, and discover that one Wi-Fi wave is about as long as your hand.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_waves.ipynb`](notebooks/01_waves.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## Two numbers

- **Frequency** $f$: how many times the wave wiggles up and down **per second**. The unit
  is hertz (Hz). Wi-Fi often uses **2.4 GHz**: about 2,400,000,000 wiggles per second.
- **Wavelength** $\lambda$ (the Greek letter "lambda"): the distance from one top of
  the wave to the next top.

```text
   top        top        top
   /\         /\         /\
  /  \       /  \       /  \
 /    \     /    \     /    \
       \   /      \   /
        \_/        \_/
   |<-------->|
    wavelength λ
```

## The rule that connects them

A wave moves forward one wavelength each time it wiggles once. In one second it wiggles
$f$ times, so it moves $f \times \lambda$. That must equal its speed $c$ (the speed of
light, about 300,000,000 m per second):

$$
c = f \times \lambda \qquad\Longrightarrow\qquad \lambda = \frac{c}{f}
$$

For Wi-Fi at 2.4 GHz:

$$
\lambda = \frac{300{,}000{,}000\ \text{m/s}}{2{,}400{,}000{,}000\ \text{per s}} = 0.125\ \text{m} \approx 12.5\ \text{cm}
$$

That is about the length of your hand. **Remember 12.5 cm.** It comes back on every
page of this chapter.

## Try it: compute it with Python

```python
c = 299_792_458          # speed of light in m/s (the exact value)
f = 2.4e9                # 2.4 GHz = 2.4 x 10^9 Hz
print(c / f, "m")        # about 0.1249 m
```

| Frequency | Wavelength (computed) |
|---|---|
| 2.4 GHz | 0.1249 m ≈ 12.5 cm |
| 2.462 GHz (Wi-Fi channel 11, used in this lab) | 0.1218 m ≈ 12.2 cm |
| 5.0 GHz | 0.0600 m ≈ 6 cm |

Higher frequency → shorter wavelength. Doubling the frequency halves the wavelength.

📖 Why does Wi-Fi use 2.4 GHz at all? → Column: [Why 2.4 GHz?](columns/01_why_2_4ghz.md)

> 🤖 **Ask your AI**
> - "Why does a higher frequency mean a shorter wavelength? Explain with people walking
>   in step, and ask me to guess first."
> - "What is the wavelength of FM radio at 80 MHz? Don't tell me the answer; show me
>   how to set it up."
> - "What does 'giga' mean in GHz? Give me other words with giga, mega, kilo."

## Check yourself

1. What is the wavelength of a 2.4 GHz Wi-Fi wave, roughly?
2. 5 GHz Wi-Fi: is its wavelength longer or shorter than 2.4 GHz Wi-Fi?
3. Write the rule that connects speed, frequency and wavelength.

<details><summary>Answers</summary>

1. About 12.5 cm.
2. Shorter (about 6 cm).
3. $\lambda = c / f$ (wavelength = speed ÷ frequency).

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Sine waves and radians: [三角関数](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/03_trigonometry.md)
- Greek letters such as λ (lambda): [ギリシャ文字](https://github.com/nobufumi-tego/learning-math/blob/main/00_notation/06_greek_letters.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [1-1. Radio waves](01_radio_waves.md) | [Chapter 1](README.md) | [Home](../README.md) | [1-3. Reflection and paths](03_reflection_and_paths.md) |
