[English](03_decision_tree.md) | 日本語

# 5-3. 決定木 — 中身を読めるモデル

**決定木**（けっていぎ）は、「はい／いいえ」で答える質問を並べたものです。フローチャートのような形をしています。
よいところは、中身を表示して、ルールが正しそうか自分の目で確かめられることです。
このページでは決定木を学習させて、**混同行列**（こんどうぎょうれつ）でまちがいを調べます。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_first_machine_learning.ipynb`](notebooks/01_first_machine_learning.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 「20 の質問」ゲーム

「それは動物？」「はい」「空を飛ぶ？」「いいえ」……と質問して正体を当てるゲームを知っていますか？
決定木は、窓の数を使ってこのゲームをします。「`change_rate` は 0.04 より大きい？」のように
質問を重ねて、答えにたどりつきます。

質問はコンピューターが自分で選びます。学習用のデータのラベルをいちばんうまく分けられる質問を、
1 つずつ選んでいきます。

## 小さな決定木を学習させる

質問は続けて 3 つまで（`max_depth=3`）にして、木を小さく読みやすくします。
[5-2](02_train_and_test.ja.md) で作った `X_train`・`y_train` などを使います。

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

tree = DecisionTreeClassifier(max_depth=3, random_state=0)
tree.fit(X_train, y_train)

names = ["motion", "motion_max", "spread", "rssi_std_db", "change_rate"]
print(export_text(tree, feature_names=names))
print("train:", accuracy_score(y_train, tree.predict(X_train)))
print("test :", accuracy_score(y_test, tree.predict(X_test)))
```

わたしたちが動かしたとき（学習用 `seed=1`、テスト用 `seed=2`、部屋 7）は、次の木になりました。

```text
|--- change_rate <= 0.04
|   |--- motion <= 0.04
|   |   |--- spread <= 0.24
|   |   |   |--- class: still
|   |   |--- spread >  0.24
|   |   |   |--- class: empty
|   |--- motion >  0.04
|   |   |--- motion_max <= 0.05
|   |   |   |--- class: wave
|   |   |--- motion_max >  0.05
|   |   |   |--- class: wave
|--- change_rate >  0.04
|   |--- class: walk
```

点数は **学習用で 0.892**、**テスト用で 0.912** でした。

読み方:

- 変化が速い（`change_rate` が 0.04 より大きい）→ `walk`
- 変化はゆっくりだけど、ゆれがある（`motion` が 0.04 より大きい）→ `wave`
  （その下の 2 つの枝はどちらも `wave` です。最後の質問は答えを変えませんでした）
- ほとんどゆれない → `empty` か `still`。どちらかは `spread` で決めています

`spread`（部屋の「指紋」）をおぼえておいてください。次のページで大事になります。

文字ではなく絵で見たいときは、`sklearn.tree.plot_tree(tree, feature_names=names, class_names=tree.classes_, filled=True)`
で、同じ木を matplotlib でかけます。

## 混同行列: どこでまちがえた？

正解率の数 1 つだけでは、*どの* 答えをまちがえたのかがわかりません。**混同行列** を見ると
わかります。行 ＝ 本当の答え、列 ＝ モデルが言った答え です。

```python
from sklearn.metrics import confusion_matrix

labels = ["empty", "still", "walk", "wave"]
print(confusion_matrix(y_test, tree.predict(X_test), labels=labels))
```

テスト用のデータ（同じ部屋）では、こうなりました。

| 本当 ↓ ／ 言った → | empty | still | walk | wave |
|---|---|---|---|---|
| empty | 60 | 0 | 0 | 0 |
| still | 20 | 39 | 0 | 1 |
| walk  | 0 | 0 | 60 | 0 |
| wave  | 0 | 0 | 0 | 60 |

左上から右下へのななめの数が、正しく答えた数です。まちがいはほとんど 1 か所に集まっています。
`still` の窓のうち 20 個が `empty` と言われました。じっと座っている人は電波をほとんど変えないので、
この 2 つを見分けるのはむずかしいのです。

> 🤖 **AI に聞いてみよう**
> - 「これがわたしの決定木の表示です。まだ説明しないで。最初の質問が何を意味するか、わたしに聞いてください」
> - 「混同行列で、`still` の窓 20 個が `empty` と言われました。どうしてだと思う？ ヒントをちょうだい」

## たしかめよう

1. `max_depth=3` は何をしていますか？
2. 混同行列で、正しく答えた数はどこにありますか？
3. 正解率の数 1 つではわからず、混同行列でわかることは何ですか？

<details><summary>こたえ</summary>

1. 続けてする質問を 3 つまでにしています。木が小さく読みやすくなります（過学習もしにくくなります）。
2. ななめ（本当の答えと言った答えが同じところ）です。
3. どのラベルとどのラベルがまざったか、です。たとえば `still` が `empty` と言われたことがわかります。

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 決定木のしくみ: [決定木とランダムフォレスト（組合せ）](https://github.com/nobufumi-tego/learning-math/blob/main/04_discrete_math/03_combinatorics.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [5-2. 学習とテスト](02_train_and_test.ja.md) | [第 5 章](README.ja.md) | [ホーム](../README.ja.md) | [5-4. 新しい部屋でためす](04_new_room.ja.md) |
