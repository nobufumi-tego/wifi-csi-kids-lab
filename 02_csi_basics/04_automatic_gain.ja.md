[English](04_automatic_gain.md) | 日本語

# 2-4. 自動音量調整 — はじめに平均で割るわけ

ESP32 は、パケットごとに自分で音量のつまみを上げたり下げたりします。そのため、部屋の中で
何も動いていなくても、そのままの数はとびはねます。このページでは、そのとびはねを
見てから、Python 1 行で消します。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_look_at_csi.ipynb`](notebooks/01_look_at_csi.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 自動の音量つまみ

強い電波と弱い電波では、数の大きさがとてもちがってしまいます。使いやすい大きさに
そろえるために、ESP32 には自動の音量つまみがあります。**自動利得制御（じどうりとく
せいぎょ、AGC）** といいます。パケットごとに、音量を少し上げたり下げたりします。

こまるのは、つまみが動いただけで、**部屋の中で何も動いていなくても** そのままの振幅が
とびはねてしまうことです。

## とびはねを見てみよう

[2-3](03_look_at_data.ja.md) の「だれもいない部屋」のサンプルを使って、パケットごとに
56 本の車線の振幅の平均を計算します。

```python
from csi_lab import load_csv

rec = load_csv("data/samples/empty.csv")
packet_average = rec.amplitude.mean(axis=1)    # パケット（行）ごとの平均
print(packet_average.min(), packet_average.max())
```

`csi-lab samples` で作った `empty.csv`（seed 0）では、だれもいないのに、平均が
**25.6 から 31.8** までばらつきました。

## 消す: パケットごとに、その平均で割る

直し方は、パケットごとに、そのパケットの 56 本の平均で割ることです。すると、どの行も
平均がちょうど 1 になります。

$$
\text{正規化した振幅} = \frac{\text{1 本の車線の振幅}}{\text{そのパケットの 56 本の平均}}
$$

```python
from csi_lab.features import normalize_per_packet

norm = normalize_per_packet(rec.amplitude)     # どの行も平均が 1 になる
print(norm.mean(axis=1).std())                 # ほぼ 0。とびはねが消えた
```

結果は約 $1 \times 10^{-16}$ でした。コンピューターの計算のごくわずかなずれをのぞけば、0 です。

## 残るもの: 形

割ったあとは、全体の大きさ（音量）が消えます。残るのは車線どうしの **形**、つまり、
どの車線が強くて、どの車線が弱いかです。部屋や、部屋にいる人が変えるのは、この形です
（[1-4](../01_waves/04_interference.ja.md) を思い出しましょう）。`csi-lab show` の
ヒートマップは、もうこれをしてあります。

> 🤖 **AI に聞いてみよう**
> - 「受信機が自分で音量を変えるのはなぜ？ マイクやカメラの自動の明るさ調整にたとえて説明して」
> - 「表のどの行も、その行の平均で割ると、何が変わって何が変わらない？ 数 3 つの小さな例で教えて」
> - 「コンピューターにとって 1e-16 がほぼ 0 なのはなぜ？」

## たしかめよう

1. 自動利得制御（AGC）ってなに？
2. 何も動いていないのに、そのままの振幅がとびはねるのはなぜ？
3. `normalize_per_packet` をしたあと、どの行も平均はいくつになる？

<details><summary>こたえ</summary>

1. 受信機の自動の音量つまみ。パケットごとに音量を上げたり下げたりする。
2. つまみそのものが、パケットごとに動くから。
3. 1。残るのは車線どうしの形で、部屋が変えるのはこの形。

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 平均などの要約: [記述統計](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/05_descriptive_stats.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [2-3. データを見てみよう](03_look_at_data.ja.md) | [第 2 章](README.ja.md) | [ホーム](../README.ja.md) | [第 3 章: 作ってみる](../03_build/README.ja.md) |
