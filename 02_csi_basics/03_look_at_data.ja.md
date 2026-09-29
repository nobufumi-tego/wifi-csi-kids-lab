[English](03_look_at_data.md) | 日本語

# 2-3. データを見てみよう — まねっこの記録を作って絵にする

いよいよ、自分の目で CSI を見てみましょう。まだ機材がないので、ラボの **シミュレーター**
を使います。送信機と受信機を 3 m はなして置いた部屋をまねしてくれます。このページでは、
記録を作り、絵にして、表計算ソフトと Python で開きます。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/01_look_at_csi.ipynb`](notebooks/01_look_at_csi.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## 記録はどんな形？

記録は表です。**1 行が 1 パケット** です。送信機は 1 秒に 100 パケット送るので、30 秒で
約 3,000 行になります。

| time_s | rssi_dbm | label | sc-28 | sc-27 | … | sc28 |
|---|---|---|---|---|---|---|
| 0.000 | -54 | walk | 47.539 | 46.615 | … | … |
| 0.009 | -56 | walk | 48.332 | 49.396 | … | … |

- `time_s`: 始まってからの秒
- `rssi_dbm`: 電波の強さ（0 に近いほど強い。[2-2](02_what_is_csi.ja.md) を見てね）
- `label`: そのとき何をしていたか
- `sc-28` 〜 `sc28`: それぞれの車線の振幅

（この 2 行は、下のコマンドで作った `walk.csv` の最初の部分です。）

## ステップ 1: まねっこの記録を作る

ラボのフォルダでターミナルを開いて、次のように打ちます。

```bash
uv run csi-lab samples
```

`data/samples/` の中に、次のファイルができます。

| ファイル | 何が起きているか |
|---|---|
| `empty.csv` | 部屋にだれもいない |
| `still.csv` | 人が線からはなれて、じっと座っている |
| `walk.csv` | 人が線を横切って行ったり来たりする |
| `breathe.csv` | 人が線の近くに座って、息をしている |
| `wave.csv` | 人が座って手をふる |
| `story.csv` | 時間とともに様子が変わる |

これは、かんたんなしくみで作った **まねっこ** のデータです。本物の部屋はもっと複雑です。
[第 3 章](../03_build/README.ja.md) で本物のデータとくらべます。

## ステップ 2: 絵にする

```bash
uv run csi-lab show data/samples/empty.csv
uv run csi-lab show data/samples/walk.csv
```

ファイルのとなりに絵（`empty.png`、`walk.png`）ができます。2 つを開いてみましょう。

- **上（ヒートマップ）:** 右に行くほど時間が進み、上に行くほど車線の番号が大きくなります。色が振幅です。
- **まん中:** 1 秒ごとの「動きの数」（[第 4 章](../04_analysis/README.ja.md) で自分で作ります）。
- **下:** RSSI。

2 つの絵は、どこがちがいますか？ ヒートマップの中の **たてのしま模様** をさがしてみましょう。

## ステップ 3: 表計算ソフトで開く

`data/samples/walk.csv` を Excel や Google スプレッドシート、LibreOffice で開いてみましょう。
1 行目は `#` で始まっていて、ファイルについてのメモです（`source=simulated scenario=walk ...`）。
`sc10` の列で折れ線グラフを作ってみましょう。

## ステップ 4: Python で読みこむ

```python
from csi_lab import load_csv

rec = load_csv("data/samples/walk.csv")
print(rec.n_packets, "packets")
print(round(rec.duration_s, 1), "seconds")
print(round(rec.rate_hz, 1), "packets per second")

df = rec.to_dataframe()   # pandas の表。列は CSV と同じ
print(df.head())
print(df["sc10"].describe())
```

`csi-lab samples` で作ったサンプル（walk のファイルは seed 2）では、
**2963 パケット、30.0 秒、1 秒に 98.8 パケット** になりました。ちょうど 3,000 や 100 では
ありません。本物の受信機と同じように、シミュレーターはわざとパケットを約 1% 落としている
からです。

## ステップ 5: いくつかの車線を絵にする

```python
from csi_lab import load_csv
from csi_lab.plot import plot_subcarriers

for name in ["empty", "walk"]:
    rec = load_csv(f"data/samples/{name}.csv")
    fig = plot_subcarriers(rec, [-20, -5, 10, 25])
    fig.savefig(f"data/samples/{name}-lanes.png")
```

2 つの絵をくらべましょう。どちらのほうが、よくゆれていますか？

> 🤖 **AI に聞いてみよう**
> - 「1 行が Wi-Fi の 1 パケットで、振幅の列が 56 こある表があります。そのヒートマップの読み方を教えて。コードは書かずに、ヒントだけちょうだい」
> - 「walk.png のヒートマップに、たてのしま模様があります。何がしま模様を作っていると思う？ わたしが自分で気づけるように、質問しながら教えて」
> - 「`df.describe()` で何がわかるの？ count・mean・std・min・max をやさしく説明して」

## たしかめよう

1. 記録の 1 行は、何をあらわしている？
2. 記録を絵にして保存するコマンドは？
3. walk の記録が 3,000 行より少しだけ少ないのはなぜ？

<details><summary>こたえ</summary>

1. パケット 1 つ。
2. `uv run csi-lab show <ファイル>`。
3. パケットがいくつか落ちている（本物の受信機のように、シミュレーターがわざと約 1% 落としている）し、
   時間の間かくもぴったり同じではないから。

</details>

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [2-2. CSI ってなに？](02_what_is_csi.ja.md) | [第 2 章](README.ja.md) | [ホーム](../README.ja.md) | [2-4. 自動音量調整](04_automatic_gain.ja.md) |
