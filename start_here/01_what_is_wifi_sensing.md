English | [日本語](01_what_is_wifi_sensing.ja.md)

# 0-1. What is Wi-Fi sensing? — Wi-Fi that notices you moved

Wi-Fi is made for sending videos and messages. But the same radio waves can also
tell that someone in the room moved. This page explains the idea as a story. No code.

## A room full of bouncing waves

Imagine a dark room with a flashlight on one side and a light meter on the other. The
light meter sees the light that comes **straight** from the flashlight, and also light
that **bounces** off the walls, the table, the shelf, and you.

Wi-Fi radio waves behave in a similar way. You cannot see them, but they bounce off
walls, furniture, and people. The receiver gets **many copies** of the same wave, each
arriving by a different path.

```text
   S (sender) ─────────────────────► R (receiver)     straight path
        \                           ↗
         \──► wall ──►  person ──/                     bounced paths
```

## When you move, the mix changes

The copies add up at the receiver. Sometimes they help each other and the wave gets
bigger. Sometimes they cancel and it gets smaller. When a person walks, the paths
that bounce off the person get longer or shorter, so the mix keeps changing.

A Wi-Fi chip can report this mix in detail. That report is called **CSI** (Channel
State Information). You will meet it in [Chapter 2](../02_csi_basics/README.md).

## What Wi-Fi sensing can and can't do

With the tools in this lab (two small ESP32 boards and a computer), you can try to find out:

- Is the room **empty**, or is someone there?
- Is someone **moving** or sitting **still**?
- Can we see slow, regular movement like **breathing**? (In our pretend data, yes.
  In a real room, it is much harder.)

What you should **not** expect:

- It does not make pictures like a camera.
- It does not know **who** someone is.
- It is easily confused: a door, a fan, a pet, or another person can all change the waves.
- It is **not** a medical device or a security alarm.

## Why we need to be careful

Even without a camera, Wi-Fi sensing can tell whether someone is home and roughly
what they are doing. That is private information. So in this lab we always:

- ask everyone in the room before recording,
- keep recordings on our own computer,
- never measure other people's homes.

The details are on the [safety page](04_safety.md). The column
[Wi-Fi that notices people](columns/01_sensing_and_privacy.md) talks more about it.

> 🤖 **Ask your AI**
> - "Where else do waves bounce and mix in everyday life? Give me three examples."
> - "Why can't Wi-Fi sensing tell who a person is? Give me a hint first."

## Check yourself

1. Why does the receiver get many copies of the same wave?
2. Why does the mix of waves change when a person walks?
3. Name one thing Wi-Fi sensing in this lab can't do.

<details><summary>Answers</summary>

1. The wave bounces off walls, furniture and people, so it reaches the receiver along many different paths.
2. The paths that bounce off the person get longer or shorter, so the copies add up differently.
3. For example: it can't make pictures, can't tell who someone is, and is not a medical device.

</details>

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Chapter 0](README.md) | [Chapter 0](README.md) | [Home](../README.md) | [0-2. Terminal and uv](02_terminal_and_uv.md) |
