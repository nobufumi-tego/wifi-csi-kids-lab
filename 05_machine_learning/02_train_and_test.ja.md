[English](02_train_and_test.md) | 日本語

# 5-2. 学習とテスト — 練習問題でテストしてはいけない理由

100 点を取るモデルが、いつもよいモデルとは限りません。このページでは、**公平に** テストする方法と、
**過学習**（かがくしゅう）とは何かを学びます。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 練習問題のたとえ

練習問題をまる暗記して、テストにまったく同じ問題が出たらどうなるでしょう。
100 点が取れますが、それで「わかっている」とは言えませんね。機械も同じです。
だから、**テスト用のデータはいつも別に取っておきます**。

## 3 つのデータ

| データ | 作り方 | わかること |
|---|---|---|
| **学習用（train）** | `seed=1`、部屋 7 | モデルが学ぶ例 |
| **テスト用（test）** | `seed=2`、部屋 7 | **同じ部屋** での新しい記録 |
| **新しい部屋** | `seed=2`、`room_seed=99` | **家具の置き方がちがう** 部屋での新しい記録 |

`seed` を変えると、記録が変わります（だれがいつ動くか、雑音など）。`room_seed` を変えると
家具が動いて、部屋そのものが変わります。部屋 7 はシミュレーターのいつもの部屋です。

```python
from csi_lab import simulate_sequence
from csi_lab.features import window_features

steps = [("empty", 60), ("still", 60), ("walk", 60), ("wave", 60)]

def make(seed, room_seed=7):
    w = window_features(simulate_sequence(steps, seed=seed, room_seed=room_seed))
    return w.features, w.labels

X_train, y_train = make(seed=1)
X_test, y_test = make(seed=2)
X_room, y_room = make(seed=2, room_seed=99)
```

データは **記録ごと** に分けます。1 つの記録の窓をばらばらに混ぜて分けてはいけません。
となりどうしの窓はとてもにているので、片方を「学習用」、となりを「テスト用」にすると、
答えをのぞき見しているのと同じになってしまいます。

## 正解率

いちばんかんたんな点数は **正解率**（せいかいりつ、accuracy）です。モデルが正しく答えた窓の割合です。

$$\text{正解率} = \frac{\text{正しく答えた数}}{\text{窓の数}}$$

正解率 0.9 は、10 個の窓のうち 9 個が正しかった、という意味です。

## 過学習

質問をいくつでもしてよい決定木を学習させてみます（決定木は次のページでくわしく学びます）。

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(random_state=0)   # 制限なし
tree.fit(X_train, y_train)
print("train:", accuracy_score(y_train, tree.predict(X_train)))
print("test :", accuracy_score(y_test, tree.predict(X_test)))
```

わたしたちが動かしたとき（seed は上と同じ）は、**学習用で 1.000**、**テスト用で 0.954** でした。

学習用で満点なのは、**注意のサイン** です。勝ったわけではありません。
モデルは「この記録にだけある細かいところ」まで覚えてしまったのかもしれません。
練習問題のまる暗記と同じです。これを **過学習** といいます。
公平な点数はテスト用のほうです。報告するのもいつもこちらです。

> 🤖 **AI に聞いてみよう**
> - 「過学習を、学校のテストのたとえで説明して。そのあと問題を 2 つ出して」
> - 「1 つの記録の窓をばらばらに混ぜて学習用とテスト用に分けると、なぜだめなの？ 先にヒントだけちょうだい」

## たしかめよう

1. 学習に使ったデータではなく、別の記録でテストするのはなぜですか？
2. 学習用のデータで 100% 取れました。よろこんでいいですか？
3. `seed` と `room_seed` のちがいは何ですか？

<details><summary>こたえ</summary>

1. 学習に使ったデータでテストしても、まる暗記したかどうかしかわかりません。新しい記録なら、見たことのないものに対応できるかがわかります。
2. まだです。過学習かもしれません。テスト用の点数（あとで「新しい部屋」の点数も）を見ましょう。
3. `seed` は同じ部屋での別の記録を作ります。`room_seed` は部屋そのもの（家具の置き方）を変えます。

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 学習のしくみと過学習: [損失関数と過学習](https://github.com/nobufumi-tego/learning-math/blob/main/06_ml_math_bridge/01_loss_functions.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [5-1. 特徴量とラベル](01_features_and_labels.ja.md) | [第 5 章](README.ja.md) | [ホーム](../README.ja.md) | [5-3. 決定木](03_decision_tree.ja.md) |
