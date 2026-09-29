[English](README.md) | 日本語

# レベル 5: はじめての機械学習

## このレッスンのゴール

- **自分で書くルール**（レベル 4）から、**コンピューターが学ぶルール** へ進む
- **練習に使ったデータでテストしてはいけない** 理由がわかる
- **決定木**（けっていぎ）を学習させて、見つけたルールを読める
- **ランダムフォレスト** や **k 近傍法** とくらべられる
- **混同行列** の読み方と、**過学習** とは何かがわかる
- 「新しい部屋」でのテストもふくめて、結果を **正直に** 報告できる

**時間:** 90 分くらい（2 日に分けても OK）
**必要なもの:** レベル 4 を終えていること。機械学習用の追加パッケージを 1 回だけ入れます。

```bash
uv sync --extra ml
```

ノートブック版: [`notebooks/03-first-machine-learning.ipynb`](../../notebooks/03-first-machine-learning.ipynb)

---

## 1. ルールを書く から ルールを学ぶ へ

レベル 4 では、**あなたが** 数（`motion`）を 1 つとしきい値を 1 つ選びました。「動いた／動いていない」ならそれで
うまくいきましたが、今度は `empty`・`still`・`walk`・`wave` の 4 つを答えさせたいのです。
窓ごとに数が 5 つもあると、ルールを手で書くのは大変です。機械学習を使うと、コンピューターが
**例を見てルールを見つけて** くれます。

1 秒の窓 1 つが、表の 1 行になります。

```python
from csi_lab import simulate_sequence
from csi_lab.features import window_features

steps = [("empty", 60), ("still", 60), ("walk", 60), ("wave", 60)]
w = window_features(simulate_sequence(steps, seed=1))

print(w.names)          # 列の名前（特徴量）
print(w.features[:3])   # 最初の 3 行
print(w.labels[:3])     # その 3 行の正解
```

- **特徴量**（`w.features`）＝ 問題用紙: それぞれの窓の様子を表す数
- **ラベル**（`w.labels`）＝ 解答: 本当に起きていたこと

## 2. 練習に使ったデータでテストしない

練習問題をまる暗記して、テストにまったく同じ問題が出たらどうなるでしょう。
100 点が取れますが、それで「わかっている」とは言えませんね。機械も同じです。
だから、テスト用のデータはいつも別に取っておきます。

ここでは 3 つのデータを使います。

| データ | 作り方 | わかること |
|---|---|---|
| **学習用（train）** | `seed=1`、部屋 7 | モデルが学ぶ例 |
| **テスト用（test）** | `seed=2`、部屋 7 | 新しい記録・**同じ部屋** |
| **新しい部屋** | `seed=2`、`room_seed=99` | 新しい記録・**家具の配置がちがう** |

```python
def make(seed, room_seed=7):
    w = window_features(simulate_sequence(steps, seed=seed, room_seed=room_seed))
    return w.features, w.labels

X_train, y_train = make(seed=1)
X_test, y_test = make(seed=2)
X_room, y_room = make(seed=2, room_seed=99)
```

1 つの記録の窓をばらばらに混ぜて分けるのではなく、**記録ごとに** 分けるのが大切です。
となり合う窓はとてもよく似ているので、混ぜるとカンニングしているのと同じになってしまいます。

## 3. 読める決定木

**決定木** は「`motion` は 0.04 より大きい？」のような「はい／いいえ」の質問の並びです。
いいところは、印刷してルールが納得できるか自分の目で確かめられることです。

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(max_depth=3, random_state=0)
tree.fit(X_train, y_train)

print(export_text(tree, feature_names=list(w.names)))
print("学習用     :", accuracy_score(y_train, tree.predict(X_train)))
print("テスト用   :", accuracy_score(y_test, tree.predict(X_test)))
print("新しい部屋 :", accuracy_score(y_room, tree.predict(X_room)))
```

わたしたちが試したときは、木はまず `change_rate`（変化が速い → `walk`）を聞き、次に `motion` を聞き、
`empty` と `still` を見分けるのに `spread` を使っていました。`spread` をおぼえておいてください。すぐに大事になります。

## 4. ほかのモデル: ランダムフォレストと k 近傍法

- **ランダムフォレスト** ＝ たくさんの決定木が多数決をするもの
- **k 近傍法（KNN）** ＝「学習用の中からいちばん似ている窓を 5 つ探して、その答えをまねする」もの

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

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

結果（シミュレーター、seed は上のとおり）:

| モデル | 学習用 | テスト用（同じ部屋） | 新しい部屋 |
|---|---|---|---|
| 決定木（深さ 3） | 0.892 | 0.912 | 0.562 |
| 決定木（深さ制限なし） | 1.000 | 0.954 | 0.458 |
| ランダムフォレスト | 1.000 | 0.950 | 0.496 |
| k 近傍法（k=5） | 0.967 | 0.896 | 0.308 |

## 5. 過学習（かがくしゅう）

深さ制限なしの決定木とランダムフォレストは、学習用データで **100 %** を取りました。これは勝利ではなく
注意のサインです。*この* 記録の細かいところまで暗記してしまったのかもしれません。これを **過学習** と言います。
教科を理解するかわりに、練習テストを暗記してしまうようなものです。
公平な点数はテスト用の列です。「新しい部屋」の列は、きびしいけれど正直な点数です。

## 6. 混同行列: どこでまちがえた？

正解率 1 つだけでは、*どの* 答えがまちがっているのかがわかりません。**混同行列** を見るとわかります。
行 ＝ 本当の答え、列 ＝ モデルが答えたもの です。

```python
from sklearn.metrics import confusion_matrix

labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_test, tree.predict(X_test), labels=labels))
print(confusion_matrix(y_room, tree.predict(X_room), labels=labels))
```

深さ 3 の決定木の結果です。

同じ部屋（テスト用）:

| 本当 ↓ ／ 答え → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 20 | 39 | 0 | 1 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 0 | 60 |

新しい部屋:

| 本当 ↓ ／ 答え → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 43 | 0 | 0 | 17 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 45 | 15 |

新しい部屋では、木は一度も `still` と答えていません。`empty` か `wave` と答えています。なぜでしょう？
木は `spread` を使っていました。これは **部屋の指紋** のような数です。家具が変われば指紋も変わるので、
学んだルールが合わなくなったのです。さらに新しい部屋では、`wave` の多くが `walk` に見えてしまっています。

## 7. 正直に報告しよう

- シミュレーターは **本物よりきれい** です。本物の記録では、ふつうはもっと点数が下がります。
- **どうやってテストしたか** を必ず書きましょう。同じ記録？ 同じ部屋？ ちがう日？
- **うまくいかなかったこと** も書きましょう。わたしたちは 2 つのかんたんな直し方を試しました。
  `spread` を使わない方法と、3 つの部屋（7・11・23）で学習させる方法です。どちらも新しい部屋では
  よくなりませんでした（0.487 と 0.388）。
  **一度も見たことのない部屋** で Wi-Fi センシングをうまく動かすことは、研究者も取り組んでいるむずかしい問題です。
  あなたの自由研究で、アイデアを試してみてもいいかもしれません！

> **AI に聞いてみよう**
> 「わたしの決定木は、同じ部屋では 91 % なのに新しい部屋では 56 % です。答えは言わずに、
> 理由を自分で見つけられるような質問をしてください。」

> **AI に聞いてみよう**
> 「過学習を学校のテストを例にして説明してください。そのあと、わたしに 2 問クイズを出してください。」

## たしかめよう

1. 学習用のデータではなく、別の記録でテストするのはなぜですか？
2. 学習用データで 100 % を取ったモデルがあります。よろこんでいいですか？
3. 混同行列を見ると、正解率 1 つだけではわからない何がわかりますか？
4. 新しい部屋で決定木がうまくいかなかったのはなぜですか？

<details>
<summary>答え</summary>

1. 学習用データでテストしても、モデルが暗記したかどうかしかわかりません。新しい記録なら、見たことのないものに対応できるかがわかります。
2. まだです。過学習しているかもしれません。テスト用（と新しい部屋）の点数を確かめましょう。
3. どのラベルとどのラベルが取りちがえられているか、です。たとえば `still` が `empty` とまちがえられている、などです。
4. 部屋そのものの様子を表す `spread` にたよっていたからです。家具が変わる（`room_seed=99`）とその数が変わるので、ルールが通用しなくなりました。

</details>

## つぎへ

➡ [自由研究のすすめかた](../../projects/README.ja.md) ― 学んだことを使って、自分の問いに答えてみましょう。
