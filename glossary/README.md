English | [日本語](README.ja.md)

# Glossary

Words used in the lessons, in simple terms.

## Radio waves

- **Radio wave**: An invisible wave of electric and magnetic energy that travels at
  the speed of light. Wi-Fi, radio, and phones use radio waves.
- **Frequency**: How many times a wave wiggles per second, measured in hertz (Hz).
  Wi-Fi often uses about 2.4 **GHz** (2.4 billion wiggles per second).
- **Wavelength**: The length of one wiggle. Wavelength = speed of light ÷ frequency.
  For 2.4 GHz Wi-Fi it is about **12.5 cm**.
- **Amplitude**: How big the wave is (its height). In this lab, "amplitude" is the
  size of the wave on each subcarrier.
- **Phase**: Where the wave is in its wiggle (top, bottom, or in between) at a moment.
- **Reflection**: When a wave bounces off something, like a wall, a table, or a person.
- **Line of sight**: The straight path between the transmitter and the receiver
  with nothing in the way.
- **Multipath**: The wave reaches the receiver along many paths at once: straight,
  and bounced off walls, furniture, and people.
- **Interference**: When waves meet, they add up. If their tops line up, they get
  bigger. If a top meets a bottom, they cancel. Multipath causes interference.
- **Fresnel zone**: An egg-shaped area around the straight line between the
  transmitter and receiver. Movement inside it changes the signal the most.

## Wi-Fi

- **Wi-Fi**: A way for devices to talk with radio waves (standard IEEE 802.11).
- **Channel**: A "lane" of frequencies that Wi-Fi uses. This lab uses channel 11
  (around 2.462 GHz), 20 MHz wide.
- **OFDM**: A way of sending data by splitting one channel into many small
  frequencies that are sent at the same time.
- **Subcarrier**: One of those small frequencies. In this lab we use 56 subcarriers,
  numbered -28 to -1 and 1 to 28. Neighbors are 312.5 kHz apart.
- **Packet**: One small bundle of data sent by Wi-Fi. Our transmitter sends about 100 per second.
- **CSI (Channel State Information)**: Measurements of how the wave changed on its
  way, one value for each subcarrier. Moving people change the CSI.
- **RSSI**: Received Signal Strength Indicator, one number for how strong the whole
  signal is.
- **dBm**: A unit for signal power. 0 dBm = 1 milliwatt. Wi-Fi signals are much weaker,
  such as -50 dBm. Closer to 0 means stronger, and every 10 dB is 10 times the power.

## Hardware

- **ESP32**: A small, cheap computer chip with Wi-Fi. It can report CSI.
- **Firmware**: The program that runs on the ESP32. You "flash" (write) it to the board.
- **Serial port**: The connection (over USB) that the ESP32 uses to send text to your
  computer, for example `/dev/ttyUSB0` or `COM3`.
- **Automatic gain control (AGC)**: The receiver turns its "volume knob" up or down
  for each packet. This makes raw amplitude jump, so we normalize it.

## Data and analysis

- **Sampling rate**: How many measurements per second, in Hz. Here about 100 Hz.
- **Noise**: Random small changes that are not what you want to measure.
- **Normalize**: Divide by an average so that different measurements can be compared.
- **Window**: A short slice of time, for example 1 second, that we look at in one go.
- **Standard deviation**: A number for how much values spread out or wobble. Zero
  means no wobble at all.
- **Feature**: A number computed from data that describes something useful, such as
  "how much the amplitude wobbled in this window".
- **Threshold**: A dividing line. Above it we say "moving", below it "still".

## Machine learning

- **Machine learning**: Letting a computer find rules from examples instead of
  writing the rules by hand.
- **Training data**: Examples the computer learns from.
- **Test data**: Different examples used to check how well it learned. The computer
  must not see them while learning.
- **Accuracy**: The share of test examples it got right, for example 90 %.
- **Overfitting**: When a model memorizes its training data but does badly on new
  data. It's like memorizing answers instead of understanding.

## More words

For math words and symbols (Σ, λ, σ …), learning-math has a
[math symbol reference](https://github.com/nobufumi-tego/learning-math/blob/main/glossary/symbol_reference.md)
and a [Japanese–English list of math terms](https://github.com/nobufumi-tego/learning-math/blob/main/glossary/jp_en_terms.md)
(both in Japanese, written for adults).

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [Math map](../appendix/math_map.md) | [Appendix](../appendix/README.md) | [Home](../README.md) | [Home](../README.md) |
