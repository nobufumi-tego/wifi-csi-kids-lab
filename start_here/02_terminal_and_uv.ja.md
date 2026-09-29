[English](02_terminal_and_uv.md) | 日本語

# 0-2. ターミナルと uv — ラボを開こう

このページでは、自分のパソコンでラボを開く方法を説明します。**ターミナル**、**uv**、
**JupyterLab** という 3 つの助っ人が出てきます。ソフトを入れる作業があるので、
はじめてのときは、おうちの人に手伝ってもらいましょう。

## ステップ 1. ラボをパソコンに持ってくる

- **かんたんな方法**: GitHub のページで、緑の **`<> Code`** ボタン →
  **Download ZIP** をおします。そのあと ZIP を**展開**します（Windows なら右クリック →
  「すべて展開...」）。ZIP をダブルクリックして中を見るのは、展開とはちがいます。
- **git を知っている人**: `git clone https://github.com/nobufumi-tego/wifi-csi-kids-lab.git`

## ステップ 2. ワンクリックでラボを起動する

| パソコン | すること |
|---|---|
| Windows | ラボのフォルダの **`start.bat`** をダブルクリック |
| Mac / Linux | ラボのフォルダでターミナルを開いて `./start.sh` と打つ |
| どれでも（uv が入っていれば） | `uv run lab.py` |

起動スクリプトは、必要なら **uv** を入れて、ラボで使うものを全部入れて
（`uv sync` 1 回で全部入ります）、ブラウザで **JupyterLab** を開きます。
はじめては数分かかります。Ctrl+C をおさずに待ちましょう。

**ラボを止めるとき:** ターミナルの画面をクリックして **Ctrl+C を 2 回**おします。
ブラウザのタブを閉じるだけでは止まりません。

## ターミナルってなに？

ターミナルは、クリックする代わりに**命令（コマンド）を文字で打つ**画面です。
1 行打って Enter をおすと、コンピューターが返事をします。たとえば、

```bash
uv run csi-lab samples
```

は、「uv を使って、ラボの道具 `csi-lab` で練習用の記録を作って」という意味です。
コマンドを覚える必要はありません。何を打つかはレッスンに書いてあります。
それに、動かす**前に**「このコマンドは何をするの？」と AI に聞くこともできます。

## uv ってなに？

**uv** は、Python の準備をしてくれる助っ人です。ちょうどよい版の Python と、
使う道具（NumPy、pandas、matplotlib、scikit-learn、JupyterLab など）を、
ラボの中の `.venv` というフォルダに入れます。パソコンのほかの部分は変えません。

| コマンド | すること |
|---|---|
| `uv sync` | ラボに必要なものを全部入れる・新しくする |
| `uv run <なにか>` | ラボの Python でプログラムを動かす |
| `uv run lab.py` | JupyterLab を開く |

## JupyterLab の基本

JupyterLab はブラウザの中で開きます。読むページと、動かせるコードをならべて使えます。

- **ファイルブラウザ**（左がわ）: フォルダをクリックして開きます。どの章にも
  `notebooks/` フォルダがあります。
- **`.md` のページ**は、読みやすい形で開きます（ラボ全体をここで読めます）。
- **`.ipynb` のノートブック**は「セル」でできています。セルをクリックして
  **Shift + Enter** をおすと、そのセルが動いて次のセルへ進みます。上から順に動かしましょう。
- ようすがおかしくなったら、**Kernel → Restart Kernel and Run All Cells** をためします。

## エラーが出たら

エラーはこわく見えますが、**助けてくれるお手紙**です。**いちばん下**から読みましょう。
最後の行に、何がいけなかったかが書いてあることが多いです。

```text
FileNotFoundError: file not found: data/samples/walk.csv
```

これは「ファイルがまだない」という意味です。`uv run csi-lab samples` をわすれたのかもしれません。
こまったら、エラーを**全部**コピーして AI の学習パートナーに見せましょう
（聞き方は [0-3](03_learning_with_ai.ja.md) にあります）。

> 🤖 **AI に聞いてみよう**
> - 「`uv sync` は何をするの？ 小学 5 年生にわかるように教えて」
> - 「このエラーが出ました: …。最後の行はどういう意味？ まずヒントをちょうだい」

## たしかめよう

1. JupyterLab を止めるには、どうする？
2. ノートブックのセルを 1 つ動かすには、どうする？
3. エラーは、どこから読むといい？

<details><summary>こたえ</summary>

1. ターミナルの画面で Ctrl+C を 2 回おします。ブラウザを閉じるだけではだめです。
2. セルをクリックして、Shift + Enter をおします。
3. いちばん下からです。最後の行に原因が書いてあることが多いです。

</details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- [ペンタと学ぶターミナル基礎](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/README.md)
- [uv の役割](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/08_uv_keeps_pet_healthy.md)
- [エラーメッセージの読み方](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/00_pet_terminal/columns/05_reading_errors.md)
- [Jupyter Lab ビギナーガイド](https://github.com/nobufumi-tego/learning-math/blob/main/docs/jupyter_lab_guide.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [0-1. Wi-Fi センシングってなに？](01_what_is_wifi_sensing.ja.md) | [第 0 章](README.ja.md) | [ホーム](../README.ja.md) | [0-3. AI との学び方](03_learning_with_ai.ja.md) |
