[English](README.md) | 日本語

# Wi-Fi CSI キッズラボ

[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC_BY_4.0-lightgrey.svg)](LICENSE-DOCS)
[![CI](https://github.com/nobufumi-tego/wifi-csi-kids-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/nobufumi-tego/wifi-csi-kids-lab/actions/workflows/ci.yml)

**Wi-Fi は、きみが動いたことに気づけるでしょうか？** Wi-Fi の電波は、部屋の中で
はね返りながら進んでいます。人が歩いたり、手をふったり、息をしたりするだけで、電波は
ほんの少し変わります。Wi-Fi のチップは、その変化を **CSI（チャネル状態情報）** という
数字で測れます。

このラボでは、電波の基本から始めて、Python で CSI のデータを調べ、はじめての機械学習を
ためし、最後は**自分の自由研究**にまとめるところまで進みます。対象はだいたい
**10〜15 さい**。おうちの人と、**AI の学習パートナー**（生成 AI）といっしょに進めることを
前提にしています。

> ⚠️ **はじめに読んでください:** この教材は、個人が生成 AI といっしょに作ったもので、
> **専門家のチェックは受けていません**。まちがいがあるかもしれません。練習用のデータは、
> 部屋を単純にまねしたシミュレーターで作っています。くわしくは [免責事項](DISCLAIMER.ja.md)。

## ここでできること

- 電波・はね返り・波の足し算（干渉）を、絵と少しの Python で理解する
- CSI を自分の目で見る（Wi-Fi のパケット 1 つに 56 この数字。動くとどう変わる？）
- ESP32 ボード 2 台で送信機と受信機を作る（やらなくても OK。おうちの人といっしょに）
- 動きの検出器を作り、コンピューターに「だれもいない・じっとしている・歩いている」を見分けさせる
- 公平で正直な自由研究にまとめる

---

## 🚀 3 分ではじめる（機械はいりません）

### ステップ 1: このフォルダを手に入れる

- **かんたん:** GitHub のページの緑のボタン **`<> Code`** → **Download ZIP** をおして、
  ZIP を**展開**します（Windows なら右クリック →「すべて展開...」）。ZIP を開いただけでは動きません。
- **git を使う:** `git clone https://github.com/nobufumi-tego/wifi-csi-kids-lab.git`

### ステップ 2: ラボを起動する

| パソコン | 起動のしかた |
|---|---|
| **Windows** | [`start.bat`](start.bat) をダブルクリック |
| **Mac / Linux** | フォルダでターミナルを開いて `./start.sh` |

スクリプトが、必要なら **uv** を入れて、`uv sync` で必要なものを全部入れ、ブラウザで
JupyterLab とこのページを開きます。**はじめては数分かかります。** Ctrl+C をおさずに
待ってね。止めるときは、ターミナルの画面で **Ctrl+C を 2 回**。
（はじめての時は、おうちの人に手伝ってもらいましょう）

<details><summary>コマンドで動かしたい人・うまくいかない人へ</summary>

```bash
uv sync                                    # 必要なものを入れる（最初の 1 回）
uv run csi-lab samples                     # 練習用の記録を data/samples/ に作る
uv run csi-lab show data/samples/walk.csv  # 記録を絵にする → data/samples/walk.png
uv run lab.py                              # JupyterLab を起動する
```

くわしくは [0-2. ターミナルと uv](start_here/02_terminal_and_uv.ja.md)。
</details>

---

## 🎯 どこから始める？

| きみは… | ここから |
|---|---|
| ぜんぶはじめて | [第 0 章: はじめに](start_here/README.ja.md) |
| 電波や波が気になる | [第 1 章: 電波と波](01_waves/README.ja.md) |
| すぐにデータを見たい | [2-3. データを見てみよう](02_csi_basics/03_look_at_data.ja.md) |
| ESP32 ボード 2 台と、手伝ってくれる大人がいる | [0-4. 安全のために](start_here/04_safety.ja.md) を読んでから [第 3 章: 作ってみる](03_build/README.ja.md) |
| 自由研究のテーマをさがしている | [第 6 章: 自由研究](06_free_research/README.ja.md) |
| おうちの人・先生 | [保護者の方・先生方へ](docs/for_parents_and_teachers.ja.md) |

第 1・2・4・5 章は**機械がなくても**できます（シミュレーターが練習用のデータを作ります）。
対象学年つきの全体の順番: [学習の道すじ](docs/learning_path.ja.md)

---

## 📚 全ページ

### 🌱 [第 0 章: はじめに](start_here/README.ja.md)

| ページ |
|---|
| [0-1. Wi-Fi センシングってなに？ — きみが動いたことに気づく Wi-Fi](start_here/01_what_is_wifi_sensing.ja.md) |
| [0-2. ターミナルと uv — ラボを開こう](start_here/02_terminal_and_uv.ja.md) |
| [0-3. AI との学び方 — いつも正しいとはかぎらない学習パートナー](start_here/03_learning_with_ai.ja.md) |
| [0-4. 安全のために — 電気・電波のきまり・プライバシー](start_here/04_safety.ja.md) |

📖 コラム（読みもの）: [コラム 1. 人に気づく Wi-Fi — なぜ気をつけて使うの？](start_here/columns/01_sensing_and_privacy.ja.md)

### 🌊 [第 1 章: 電波と波 — 電波はどうやって進むの？](01_waves/README.ja.md)

| ページ |
|---|
| [1-1. 電波ってなに？ — 目に見えない波が、まわりにいっぱい](01_waves/01_radio_waves.ja.md) |
| [1-2. 波長と周波数 — Wi-Fi の波 1 つの長さは？](01_waves/02_wavelength_and_frequency.ja.md) |
| [1-3. はね返りと通り道 — Wi-Fi はいくつもの道を同時に通る](01_waves/03_reflection_and_paths.ja.md) |
| [1-4. 波の足し算（干渉） — 人が動くと Wi-Fi が変わるわけ](01_waves/04_interference.ja.md) |

🧪 ノートブック（動かす）: [`01_waves.ipynb`](01_waves/notebooks/01_waves.ipynb)
📖 コラム（読みもの）: [コラム 1: なぜ 2.4 GHz なの？ — Wi-Fi のにぎやかなご近所](01_waves/columns/01_why_2_4ghz.ja.md)

### 📶 [第 2 章: CSI の基本 — データを見てみよう](02_csi_basics/README.ja.md)

| ページ |
|---|
| [2-1. サブキャリア — Wi-Fi は 56 車線の高速道路](02_csi_basics/01_subcarriers.ja.md) |
| [2-2. CSI ってなに？ — 数 1 つのかわりに 56 こ](02_csi_basics/02_what_is_csi.ja.md) |
| [2-3. データを見てみよう — まねっこの記録を作って絵にする](02_csi_basics/03_look_at_data.ja.md) |
| [2-4. 自動音量調整 — はじめに平均で割るわけ](02_csi_basics/04_automatic_gain.ja.md) |

🧪 ノートブック（動かす）: [`01_look_at_csi.ipynb`](02_csi_basics/notebooks/01_look_at_csi.ipynb)

### 🔧 [第 3 章: 作ってみる — 自分の送信機と受信機](03_build/README.ja.md)

| ページ |
|---|
| [3-1. 用意するもの — ボード 2 台と、その話し方](03_build/01_parts.ja.md) |
| [3-2. プログラムを書き込む — ボードを S と R にする](03_build/02_flash_firmware.ja.md) |
| [3-3. 記録する — はじめての本物の CSI](03_build/03_record.ja.md) |
| [3-4. こまったときは — うまくいかないとき](03_build/04_troubleshooting.ja.md) |


### 🔍 [第 4 章: 動きを見つける — 動きの検出器を作ろう](04_analysis/README.ja.md)

| ページ |
|---|
| [4-1. 動きの数字 — 正規化して、ゆれを測る](04_analysis/01_motion_number.ja.md) |
| [4-2. しきい値で決める — そして、正解を数える](04_analysis/02_threshold.ja.md) |
| [4-3. うまくいかないところ — その理由は？](04_analysis/03_what_goes_wrong.ja.md) |
| [4-4. 呼吸を見つける — Wi-Fi でゆっくりしたリズムがわかる？](04_analysis/04_breathing.ja.md) |

🧪 ノートブック（動かす）: [`01_motion_detector.ipynb`](04_analysis/notebooks/01_motion_detector.ipynb)

### 🤖 [第 5 章: はじめての機械学習](05_machine_learning/README.ja.md)

| ページ |
|---|
| [5-1. 特徴量とラベル — 記録を表にする](05_machine_learning/01_features_and_labels.ja.md) |
| [5-2. 学習とテスト — 練習問題でテストしてはいけない理由](05_machine_learning/02_train_and_test.ja.md) |
| [5-3. 決定木 — 中身を読めるモデル](05_machine_learning/03_decision_tree.ja.md) |
| [5-4. 新しい部屋でためす — むずかしくて正直なテスト](05_machine_learning/04_new_room.ja.md) |

🧪 ノートブック（動かす）: [`01_first_machine_learning.ipynb`](05_machine_learning/notebooks/01_first_machine_learning.ipynb)

### 🔬 [第 6 章: 自由研究](06_free_research/README.ja.md)

| ページ |
|---|
| [6-1. 研究の進め方 — 公平な答えにたどりつく 7 つのステップ](06_free_research/01_how_to_do_research.ja.md) |
| [6-2. テーマのアイデア — はじめの一歩になる 10 の問い](06_free_research/02_project_ideas.ja.md) |
| [6-3. まとめシート — 自由研究をまとめよう](06_free_research/research_sheet.ja.md) |


### 📎 付録

- [数学マップ](appendix/math_map.ja.md) — 各ページの数学を learning-math のどこで学べるか
- [付録](appendix/README.ja.md) — もっと知りたい人へ
- [用語集](glossary/README.ja.md) — レッスンに出てくることば

---

## 🤖 AI といっしょに学ぶ

このフォルダを、AI のコーディング道具（たとえば **Claude Code**、**Codex**、**Gemini CLI**）で
開きましょう。道具は [`AGENTS.md`](AGENTS.md) を読みます。そこには「先生役として教えてね」と
書いてあるので、AI は先にきみの考えを聞いたり、答えの前にヒントを出したり、安全に気をつけたり
します。コマンド `/explain-simply <知りたいこと>`、`/check-understanding <テーマ>`、
`/research-buddy <アイデア>` も使えます。コツは [0-3. AI との学び方](start_here/03_learning_with_ai.ja.md)。

## 📐 数学をもっと知りたい人へ

数学を先に知っている必要はありません。もっとくわしく知りたくなったら、
[数学マップ](appendix/math_map.ja.md) から、同じ作者の **[learning-math](https://github.com/nobufumi-tego/learning-math)** の
対応するページへ進めます。learning-math は**大人向けの日本語の数学教材**です。
おうちの人といっしょに読むか、中学生以上になってから読んでみてください。

## 🛡️ 安全のために

何かを作る前に [0-4. 安全のために](start_here/04_safety.ja.md) を読みましょう。電源は USB だけ、
**技適マーク**のあるボードを使う、**同意した人だけを記録する**。記録は自分のパソコンの
[`data/`](data/README.ja.md) に置き、git にはコミットしません。

## ライセンス

- プログラム（`src/`・`tests/`・`firmware/`・スクリプト・ノートブックのコード）: **MIT** — [LICENSE-CODE](LICENSE-CODE)
- レッスンなどの文章: **CC BY 4.0** — [LICENSE-DOCS](LICENSE-DOCS)
- まとめ: [LICENSE](LICENSE) ・ 協力してくれる人へ: [CONTRIBUTING](CONTRIBUTING.ja.md)
