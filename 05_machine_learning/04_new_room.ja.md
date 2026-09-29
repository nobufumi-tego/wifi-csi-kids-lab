[English](04_new_room.md) | 日本語

# 5-4. 新しい部屋でためす — むずかしくて正直なテスト

学習した部屋でうまくいくモデルは、よいスタートです。では **一度も見たことのない部屋** では
どうなるでしょう？ このページではそれをためし、ほかのモデルともくらべます。
そして、うまくいかなかったところもふくめて、結果を正直に報告する方法を学びます。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## ほかのモデル

決定木のほかに、よく使われるモデルを 2 つためします。

- **ランダムフォレスト** ＝ たくさんの決定木がそれぞれ答えを出して、多数決をする
- **k 近傍法**（きんぼうほう、KNN）＝「この窓にいちばんにている学習用の窓を 5 つ探して、
  その中でいちばん多い答えをまねする」。窓は「点」でした（5-1）。「にている」は「近い」ということです

[5-2](02_train_and_test.ja.md) で作った `X_train`・`X_test`・`X_room` などを使います。

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

models = {
    "tree (depth 3)": DecisionTreeClassifier(max_depth=3, random_state=0),
    "tree (no limit)": DecisionTreeClassifier(random_state=0),
    "random forest": RandomForestClassifier(random_state=0),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:16s} train={accuracy_score(y_train, model.predict(X_train)):.3f} "
          f"test={accuracy_score(y_test, model.predict(X_test)):.3f} "
          f"new room={accuracy_score(y_room, model.predict(X_room)):.3f}")
```

結果です（学習用 `seed=1` 部屋 7、テスト用 `seed=2` 部屋 7、新しい部屋 `seed=2` `room_seed=99`）。

| モデル | 学習用 | テスト用（同じ部屋） | 新しい部屋 |
|---|---|---|---|
| 決定木（深さ 3） | 0.892 | 0.912 | 0.562 |
| 決定木（制限なし） | 1.000 | 0.954 | 0.458 |
| ランダムフォレスト | 1.000 | 0.950 | 0.496 |
| k 近傍法（k=5） | 0.967 | 0.896 | 0.308 |

同じ部屋では、どのモデルも 0.9 くらいかそれ以上です。ところが新しい部屋では、どのモデルも
**大きく下がります**。答えが 4 つなら、でたらめに答えても 4 回に 1 回（0.25）くらいは当たります。
新しい部屋の k 近傍法は、でたらめとあまり変わりません。

## なぜ失敗した？ 混同行列が教えてくれる

```python
from sklearn.metrics import confusion_matrix

tree = models["tree (depth 3)"]
labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_room, tree.predict(X_room), labels=labels))
```

新しい部屋での決定木（深さ 3）:

| 本当 ↓ ／ 言った → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 43 | 0 | 0 | 17 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 45 | 15 |

新しい部屋では、決定木は **一度も `still` と答えていません**。`empty` か `wave` と言っています。
なぜでしょう？ [5-3](03_decision_tree.ja.md) で、決定木は `empty` と `still` を `spread` で見分けていました。
`spread` は **部屋の「指紋」** のようなものです。家具が変わると指紋も変わるので、
学んだルールが合わなくなったのです。さらに、`wave` の窓の多くが `walk` に見えています。

## 2 つの直し方をためした。どちらもだめだった

1. 部屋の指紋である **`spread` を使わずに** 学習し直す → 新しい部屋の正解率 **0.487**
2. いろいろな部屋を見せるために、**3 つの部屋**（`room_seed` 7・11・23）で学習する
   → 新しい部屋の正解率 **0.388**

（どちらも深さ 3 の決定木、学習用は `seed=1`、新しい部屋は `seed=2` `room_seed=99`）

これは *あなた* の失敗ではありません。**見たことのない部屋** で Wi-Fi センシングをうまく動かすのは、
研究者が今も取り組んでいるむずかしい問題です。部屋によって変わらない新しい特徴量など、
あなたの自由研究で新しいアイデアをためせるかもしれません。

## 正直に報告しよう

モデルについて書くときは、いつも次のことを書きましょう。

- **どうやってテストしたか**: 同じ記録？ 同じ部屋？ 別の日？
- **どんなデータか**: シミュレーター？ 本物のボード？ シミュレーターは **現実よりきれい** なので、
  本物の記録ではふつう点数が下がります
- **うまくいかなかったこと** も書く。「同じ部屋で 0.912、新しい部屋で 0.562」のほうが、
  ただ「91%」と書くよりずっと役に立ちます

> 🤖 **AI に聞いてみよう**
> - 「決定木が同じ部屋では 91%、新しい部屋では 56% でした。答えは言わないで。理由を考えるのに役立つ質問をしてください」
> - 「家具が動いても変わらないかもしれない特徴量のアイデアを 3 つ、1 文ずつのヒントでちょうだい」

## たしかめよう

1. 新しい部屋で、決定木が一度も `still` と答えなかったのはなぜですか？
2. 答えが 4 つのとき、でたらめに答えると正解率はだいたいいくつですか？
3. だれかが「わたしのモデルは正解率 95%」と書きました。どんな質問をするとよいですか？

<details><summary>こたえ</summary>

1. `empty` と `still` を `spread` で分けていたからです。`spread` は部屋そのものを表すので、家具が変わる（`room_seed=99`）とルールがこわれました。
2. だいたい 0.25（4 回に 1 回）です。
3. たとえば:「見たことのないデータでテストした？」「同じ部屋？ 新しい部屋？」「シミュレーター？ 本物？」「どのラベルをまちがえやすい？」

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 推定と過学習: [推定と過学習](https://github.com/nobufumi-tego/learning-math/blob/main/03_probability_statistics/06_estimation.md)
- 機械が学ぶしくみ: [機械が学ぶしくみ（勾配降下法）](https://github.com/nobufumi-tego/learning-math/blob/main/05_optimization/02_gradient_descent.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [5-3. 決定木](03_decision_tree.ja.md) | [第 5 章](README.ja.md) | [ホーム](../README.ja.md) | [第 6 章: 自由研究](../06_free_research/README.ja.md) |
