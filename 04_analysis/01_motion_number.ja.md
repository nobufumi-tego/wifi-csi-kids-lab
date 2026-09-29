[English](01_motion_number.md) | 日本語

# 4-1. 動きの数字 — 正規化して、ゆれを測る

何も動かなければ、それぞれのサブキャリアの値はほとんど変わりません。何かが動くと **ゆれます**。
このページでは、そのゆれを 1 秒ごとに 1 つの数字にします。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb) を開きます。
> ターミナルがはじめての人 → [0-2. ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 1. まず、正規化する

ESP32 の受信機には、自動で音量を合わせる「つまみ」（自動利得制御）があります。
このつまみは、部屋で何も動いていなくても、**パケットごとに** 音量を上げ下げします
（[2-4. 自動の音量調整](../02_csi_basics/04_automatic_gain.ja.md) を見てね）。

そこで、それぞれのパケットを **そのパケット自身の平均** で割ります。すると、どのパケットも平均が 1 になり、
サブキャリアどうしの **形** だけが残ります。人が動くと変わるのは、この形のほうです。

```python
from csi_lab import simulate
from csi_lab.features import normalize_per_packet

rec = simulate("still", duration_s=30, seed=1)
raw_avg = rec.amplitude.mean(axis=1)                    # パケットごとの平均
norm_avg = normalize_per_packet(rec.amplitude).mean(axis=1)

print("正規化前: パケットの平均のゆれ =", raw_avg.std())
print("正規化後: パケットの平均のゆれ =", norm_avg.std())
```

`seed=1` では、正規化前のパケットの平均は標準偏差で約 0.89 ゆれていましたが、正規化後は
ほぼ 0（約 $10^{-16}$）になりました。音量つまみの影響が消えたということです。

## 2. 窓に分けて、ゆれを測る

記録を 1 秒ずつに切り分けます。この 1 切れを **窓**（まど）とよびます。窓の中で、それぞれの
サブキャリアがどれくらいゆれたかを **標準偏差**（値が平均からどれくらい散らばっているか）で測ります。
値 $x_1, \dots, x_n$ の平均を $\bar{x}$ とすると、

$$
\sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2}
$$

$\sigma$（シグマ）が大きい ＝ ゆれが大きい、ということです。窓の **動きの数字** は、56 本の
サブキャリアの $\sigma$ の平均です。

```python
import numpy as np
from csi_lab import simulate
from csi_lab.features import motion_score

for name in ["empty", "still", "walk", "wave"]:
    rec = simulate(name, duration_s=30, seed=1)
    start_s, motion = motion_score(rec)          # 1 秒の窓ごとに 1 つの数
    print(f"{name:6s} 中央値={np.median(motion):.4f}  最大={motion.max():.4f}")
```

結果（シミュレーター、`seed=1`、それぞれ 30 秒）:

| 場面 | 中央値 | 最大 |
|---|---|---|
| empty（だれもいない） | 0.0305 | 0.0311 |
| still（じっと座る） | 0.0302 | 0.0427 |
| walk（歩く） | 0.0935 | 0.1385 |
| wave（手をふる） | 0.0385 | 0.0647 |

歩くと、じっと座っているときの 3 倍くらいゆれます。手をふるのは、じっと座っているときより
少し大きいだけです。

## 3. 窓ごとに、もっとたくさんの数字

`window_features` は、窓ごとに 5 つの数字をくれます。第 5 章では、これをぜんぶ使います。

| 名前 | 意味 |
|---|---|
| `motion` | サブキャリアのゆれの平均（上の動きの数字） |
| `motion_max` | いちばんゆれたサブキャリアのゆれ |
| `spread` | サブキャリアどうしがどれくらいちがうか（部屋の「指もん」） |
| `rssi_std_db` | 電波の強さ（RSSI）のゆれ |
| `change_rate` | パケットからパケットへ、振幅がどれくらい速く変わるか |

```python
from csi_lab import simulate
from csi_lab.features import window_features

w = window_features(simulate("walk", duration_s=10, seed=1))
print(w.names)
print(w.features.shape)      # (窓の数, 5)
print(w.labels[:3])
```

> 🤖 **AI に聞いてみよう**
> - 「ESP32 には自動利得制御があります。テレビの音量を例にして、パケットごとに平均で割ると
>   なぜ役に立つのかを説明してください。コードは書かずに、わたしに質問しながら教えてください」
> - 「標準偏差ってなに？ クラスのみんなの身長を例にして教えて」

## たしかめよう

1. なぜパケットごとに平均で割るのですか？
2. 1 秒の窓の標準偏差が大きいとき、何が起きていると考えられますか？
3. 表の中で、「still」といちばん見分けにくいのはどの場面ですか？

<details><summary>こたえ</summary>

1. 受信機の自動利得制御が、パケットごとに音量を変えてしまうから。平均で割るとその影響が消えて、
   部屋が原因の変化だけが残る
2. その 1 秒の間に振幅が大きくゆれた、つまり何かが動いた可能性が高い
3. 「wave」。動きの数字が「still」より少し大きいだけだから

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- ゆれの大きさ: [標準偏差（記述統計）](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/05_descriptive_stats.md)
- ばらつきのもう一つの測り方: [分散](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/03_expectation_variance.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [第 4 章](README.ja.md) | [第 4 章](README.ja.md) | [ホーム](../README.ja.md) | [4-2. しきい値で決める](02_threshold.ja.md) |
