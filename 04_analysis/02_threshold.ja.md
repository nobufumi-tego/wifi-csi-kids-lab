[English](02_threshold.md) | 日本語

# 4-2. しきい値で決める — そして、正解を数える

**しきい値** は「止まっている」と「動いている」の境目の線です。当てずっぽうで決めずに、
測って決めましょう。そのあと、状況が移り変わる記録で検出器を試します。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_motion_detector.ipynb`](notebooks/01_motion_detector.ipynb) を開きます。
> ターミナルがはじめての人 → [0-2. ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 1. しきい値はデータから決める

**だれも動いていない** ときを記録（またはシミュレーション）して、その中でいちばん大きい
動きの数字を見つけ、少し余裕を足します。

```python
from csi_lab import simulate
from csi_lab.features import motion_score

_, still_motion = motion_score(simulate("still", duration_s=30, seed=1))
threshold = still_motion.max() * 1.2      # 20 % の余裕
print("しきい値 =", round(threshold, 3))
```

`seed=1` では「still」の最大値が約 0.043 だったので、しきい値は約 0.051 になりました。

## 2. お話のような記録で試す

次は、状況が **移り変わる** 記録で検出器を試します。
だれもいない → 歩く → 座ってじっとする → 歩く → 手をふる → だれもいない、という流れです。
これは `data/samples/story.csv`（`uv run csi-lab samples` で作れます）と同じ流れです。

```python
import numpy as np
from csi_lab import simulate_sequence
from csi_lab.features import window_features, detect_motion

story = simulate_sequence(
    [("empty", 20), ("walk", 20), ("still", 20), ("walk", 10), ("wave", 20), ("empty", 10)],
    seed=100,
)
w = window_features(story)
motion = w.features[:, w.names.index("motion")]
predicted = detect_motion(motion, threshold=0.051)       # True = 「動いている」
truth = np.isin(w.labels, ["walk", "wave"])              # 本当に起きていたこと

print("正解率:", (predicted == truth).mean())
for label in ["empty", "still", "walk", "wave"]:
    sel = w.labels == label
    print(f"{label:6s} 窓の数={sel.sum():3d}  「動いている」と答えた割合 {predicted[sel].mean():.0%}")
```

## 3. 正解率

$$
\text{正解率} = \frac{\text{当たった数}}{\text{窓の数}}
$$

NumPy で自分で計算しているので、魔法ではないことがわかります。

この seed では正解率は **0.87**（100 この窓のうち 87 こが正解）でした。ラベルごとに見てみましょう。

| ラベル | 窓の数 | 「動いている」と答えた割合 |
|---|---|---|
| empty | 30 | 0 % |
| walk  | 30 | 100 % |
| still | 20 | 5 % |
| wave  | 20 | 40 % |

（シミュレーター、`seed=100`、しきい値 0.051 での結果）

87 % という 1 つの数字は、たくさんのことをかくしています。「walk」はいつも見つかるのに、
「wave」は 40 % しか見つかっていません。合計だけでなく、**いつもラベルごとに見ましょう**。

> 🤖 **AI に聞いてみよう**
> - 「わたしの検出器は 87 % 当たります。それがよいのかどうか、わたしに質問しながら考えさせて」
> - 「しきい値を当てずっぽうではなく、データから決めるほうがいいのはなぜ？」

## たしかめよう

1. しきい値を当てずっぽうではなく「だれも動いていない記録」から決めるのはなぜですか？
2. 正解率とは何ですか？
3. 検出器の正解率が 87 % でした。これはよい結果ですか？ ほかに何を知りたいですか？

<details><summary>こたえ</summary>

1. 「止まっている」ときの数字がどれくらいになるかは、部屋やハードウェアによってちがうから。
   データを見れば **この** 部屋での本当の大きさがわかるが、当てずっぽうだと大きく外れるかもしれない
2. 当たった数 ÷ 窓の数
3. 場合による！ ラベルごとに見よう。どの場面を見のがしているか？ 87 % の中に、よくまちがえる
   ラベル（ここでは「wave」）がかくれていることがある。それに、試したのはシミュレーターで、本物の部屋ではない

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 雑音の広がり方: [正規分布](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/02_distributions.md)
- その差は本物か偶然か: [仮説検定](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/07_hypothesis_testing.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [4-1. 動きの数字](01_motion_number.ja.md) | [第 4 章](README.ja.md) | [ホーム](../README.ja.md) | [4-3. うまくいかないところ](03_what_goes_wrong.ja.md) |
