[English](README.md) | 日本語

# Wi-Fi CSI キッズラボ

**Wi-Fi は、きみが動いたことに気づけるでしょうか？** Wi-Fi の電波は、部屋の中で
はね返りながら進んでいます。人が歩いたり、手をふったり、息をしたりするだけで、
電波はほんの少し変わります。Wi-Fi のチップは、その変化を
**CSI（チャネル状態情報）** という数字で測れます。

このラボでは、電波の基本から始めます。そして Python でデータを調べ、はじめての機械学習を
ためし、最後は自分の自由研究にまとめるところまで進みます。

対象はだいたい **10〜15 さい**です。おうちの人と、**AI の学習パートナー**（生成 AI）と
いっしょに進めることを前提にしています。

## 学ぶ順番

| レベル | 内容 | 必要なもの |
|---|---|---|
| [1・電波](lessons/1-waves/README.ja.md) | 電波ってなに？ どうしてはね返ったり、まざったりするの？ | パソコン |
| [2・CSI の基本](lessons/2-csi-basics/README.ja.md) | Python で CSI のデータを見てみよう（練習用のデータ） | パソコン |
| [3・作ってみる](lessons/3-build/README.ja.md) | ESP32 を 2 台用意して、自分で CSI を記録しよう | ESP32 ボード 2 台と USB ケーブル |
| [4・調べる](lessons/4-analysis/README.ja.md) | CSI から「動きの数字」を作って、動きを見つけよう | パソコン（自分の記録があればなお良い） |
| [5・機械学習](lessons/5-machine-learning/README.ja.md) | 「だれもいない・じっとしている・歩いている」をコンピューターに見分けさせよう | パソコン |

レベル 1・2・4・5 は、**機械がなくても**できます。シミュレーターが練習用の記録を
作ってくれるからです。本物のデータを測りたくなったら、レベル 3 に進みましょう。

## 5 分ではじめる（機械はいりません）

1. **uv** を入れます。Python の準備をしてくれる道具です。
   <https://docs.astral.sh/uv/getting-started/installation/>
   （ソフトを入れるときは、おうちの人に手伝ってもらいましょう）
2. このフォルダでターミナルを開いて、次のように打ちます。

   ```bash
   uv sync                                   # このラボに必要なものを入れる
   uv run csi-lab samples                    # 練習用の記録を data/samples/ に作る
   uv run csi-lab show data/samples/walk.csv # 記録を絵にして walk.png に保存する
   ```

3. `data/samples/walk.png` を開いてみましょう。上の絵に出るしま模様が、人が歩いたあとです。
4. ノートブック（ブラウザでコードとメモを書けるもの）を使うときは、次のように打ちます。

   ```bash
   uv sync --extra notebook
   uv run jupyter lab notebooks/
   ```

> **注意:** 練習用のデータは、部屋を単純にまねして作ったものです。本物の部屋はもっと
> ごちゃごちゃしているので、自分で測ったデータはもっとゆれて見えます。それがふつうです。
> そこがおもしろいところでもあります。

## AI といっしょに学ぶ

このフォルダを、AI のコーディング道具（たとえば **Claude Code**、**Codex**、
**Gemini CLI**）で開きましょう。これらの道具は [`AGENTS.md`](AGENTS.md) を読みます。
そこには「先生役として教えてね」と書いてあります。だから AI は、先にきみの考えを聞いたり、
答えの前にヒントを出したり、安全に気をつけたりします。
上手な質問のしかたは [AI との学び方](guides/learning-with-ai.ja.md) を見てください。

## ほかの資料

- [安全ガイド](guides/safety.ja.md): 電気、日本の電波のきまり（技適）、プライバシー。**レベル 3 の前に必ず読みましょう。**
- [おうちの人・先生へ](guides/for-parents-and-teachers.ja.md)
- [自由研究のテーマ例](projects/README.ja.md)
- [用語集](glossary.ja.md): レッスンに出てくることば
- [data フォルダについて](data/README.ja.md)
- [協力してくれる人へ](CONTRIBUTING.ja.md)

## ライセンス

- プログラム（`src/`・`tests/`・`firmware/`・ノートブックのコード）: **MIT**。[LICENSE](LICENSE) を見てください。
- レッスン・ガイドなどの文章: **CC BY 4.0**。[LICENSE-docs](LICENSE-docs) を見てください。
