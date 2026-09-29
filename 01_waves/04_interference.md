English | [日本語](04_interference.ja.md)

# 1-4. Adding waves (interference) — why a moving person changes Wi-Fi

When waves from different paths meet at the receiver, they add up. Sometimes they help
each other, sometimes they cancel. On this page you will see how that works, and why it
lets Wi-Fi notice a person moving — the main idea of this whole lab.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/01_waves.ipynb`](notebooks/01_waves.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## Two stones in a pond

Drop **two** stones into a pond at once. Where a top meets a top, the water rises extra
high: the waves **help** each other. Where a top meets a bottom, the water stays flat:
the waves **cancel**. This is called **interference**.

```text
 help:    /\  +  /\   =   /\        cancel:   /\  +       =   ____
         /  \   /  \     /  \                /  \   \  /
                        /    \                       \/
```

## What decides help or cancel?

At the receiver, the straight wave and the bounced wave meet. Whether they help or
cancel depends on **how much longer** the bounced path is, compared with the wavelength
$\lambda$ (about 12.5 cm):

| Extra length of the bounced path | Tops meet… | Result |
|---|---|---|
| $0,\ \lambda,\ 2\lambda,\ \dots$ (a whole number of wavelengths) | tops | help (stronger) |
| $\tfrac{1}{2}\lambda,\ 1\tfrac{1}{2}\lambda,\ \dots$ | bottoms | cancel (weaker) |
| anything in between | a bit of both | in between |

The receiver gets the **sum** of all paths. In math, "add up all of them" is written
with the symbol $\Sigma$ (sigma):

$$
\text{received} = \sum_{\text{paths}} \text{wave on that path}
$$

## Try it: add two waves in Python

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 3, 600)                    # position, in wavelengths
shift = 0.5                                   # extra path length, in wavelengths
wave_a = np.sin(2 * np.pi * x)                # straight path
wave_b = np.sin(2 * np.pi * (x - shift))      # bounced path

plt.plot(x, wave_a, label="path A")
plt.plot(x, wave_b, label="path B")
plt.plot(x, wave_a + wave_b, label="A + B", linewidth=3)
plt.legend()
plt.xlabel("position (wavelengths)")
plt.show()
```

Change `shift` to `0`, `0.25`, `0.5`, and `1.0`. When is the thick line (A + B)
biggest? When does it almost disappear?

## A moving person switches between help and cancel

Remember the person at $(1.5, y)$ from [1-3](03_reflection_and_paths.md). For
cancel to turn into help, the bounced path only needs to change by **half a
wavelength**, about 6 cm (0.0609 m at channel 11). Using the path formula, we computed
how far the person has to move to do that:

| Person starts at | Moves away from the line by | Path changes by |
|---|---|---|
| $y = 1.0$ m | 5.4 cm | half a wavelength |
| $y = 0.5$ m | 8.9 cm | half a wavelength |

A few centimeters! So while someone walks, the received signal goes **up and down, up
and down**. When nobody moves, all paths stay the same, and the signal stays almost
steady.

> **This is the whole idea of Wi-Fi sensing:** watch how the signal wobbles, and you can
> tell that something moved — without a camera.

## Different "lanes" see different results

Wi-Fi does not send just one wave. It sends many waves side by side, each at a slightly
different frequency, so each has a slightly different wavelength (you will meet these
"lanes" in [Chapter 2](../02_csi_basics/README.md)). The same room can make one lane
help and another lane cancel.

We computed an example: a straight wave of size 1 plus a bounced wave of size 0.5, at
channel 11, for three lanes (numbers −28, 0 and +28):

| Person at | Lane −28 | Lane 0 | Lane +28 |
|---|---|---|---|
| $y = 1.0$ m | 1.49 | 1.50 | 1.50 |
| $y = 2.0$ m | 0.76 | 0.60 | 0.51 |

(1.5 = fully helping, 0.5 = fully canceling.) At $y = 2$ m the lanes disagree, because
the extra 2 m of path is 16.37 wavelengths for one lane but 16.48 for another. Measuring
**every lane** gives much more information than one number.

> 🤖 **Ask your AI**
> - "Explain interference using water waves, for a 5th grader. Then ask me a question to
>   check that I understood."
> - "If the wavelength is 12.5 cm, how much does a path need to change to go from
>   'helping' to 'canceling'? Show me how to work it out step by step."
> - "Why could a person standing still be hard to notice with Wi-Fi, while a walking
>   person is easy? Give me hints, not the answer."

## Check yourself

1. Two paths differ by half a wavelength. Do they help or cancel?
2. About how far must the bounced path change to switch from cancel to help?
3. Why does the signal wobble when a person walks through the room?

<details><summary>Answers</summary>

1. They cancel: the top of one meets the bottom of the other.
2. About half a wavelength: roughly 6 cm.
3. The path bouncing off the person keeps changing length, so it keeps switching between
   helping and canceling the other paths.

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Sine waves: [三角関数](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/03_trigonometry.md)
- Adding waves, Fourier transform demo: [波の合成・フーリエ変換のデモ](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/notebooks/03_trigonometry_usecases.ipynb)
- Σ: adding many things: [総和 Σ](https://github.com/nobufumi-tego/learning-math/blob/main/00_notation/05_summation_product.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [1-3. Reflection and paths](03_reflection_and_paths.md) | [Chapter 1](README.md) | [Home](../README.md) | [Chapter 2: CSI basics](../02_csi_basics/README.md) |
