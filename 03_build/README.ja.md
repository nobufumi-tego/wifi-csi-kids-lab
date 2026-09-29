[English](README.md) | 日本語

# 第 3 章: 作ってみる — 自分の送信機と受信機

ESP32 のボードを 2 台プログラムして、1 台を **送信機（S）**、もう 1 台を **受信機（R）** にします。
そして、自分の部屋の本物の CSI を記録します。

> 👪 **この章は、おうちの人や先生といっしょに進めてください。** 始める前に
> [0-4. 安全のために](../start_here/04_safety.ja.md) をいっしょに読みましょう。

> ✅ **この章はとばしても大丈夫です。** 第 4 章と第 5 章は、シミュレーターが作る練習用の記録で
> できます。ボードが手に入ったら、またここにもどってきましょう。

## この章でできるようになること

- 2 台のボードとパソコンが、どうやって話しているかを説明できる
- Arduino IDE で、ESP32 にプログラム（ファームウェア）を書き込める
- `uv run csi-lab capture` で CSI を記録し、`uv run csi-lab show` で絵にできる
- 実験ノートをつけて、公平で、くり返せる実験ができる

**だれと:** おうちの人といっしょに ・ **時間:** 2 時間くらい（はじめてのソフトの準備に、
いちばん時間がかかります）

## ページ

| # | ページ | わかること |
|---|---|---|
| 3-1 | [`01_parts.ja.md`](01_parts.ja.md) | 用意するもの、技適マーク、2 台の話し方 |
| 3-2 | [`02_flash_firmware.ja.md`](02_flash_firmware.ja.md) | Arduino IDE 2 を入れて、S に `csi_tx`、R に `csi_rx` を書き込む |
| 3-3 | [`03_record.ja.md`](03_record.ja.md) | 部屋を準備して、はじめての本物の記録をとる |
| 3-4 | [`04_troubleshooting.ja.md`](04_troubleshooting.ja.md) | うまくいかないときに確かめること |

## ノートブック

この章では、ノートブックではなく Arduino IDE とターミナルを使います。自分の記録ができたら、
[第 4 章](../04_analysis/README.ja.md) のノートブックで `load_csv` を使って開けます。

## ファームウェア

2 つのプログラムは [`firmware/`](../firmware/README.ja.md) にあります。
[`csi_tx.ino`](../firmware/csi_tx/csi_tx.ino)（送信機）と
[`csi_rx.ino`](../firmware/csi_rx/csi_rx.ino)（受信機）です。

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [2-4. 自動の音量調整](../02_csi_basics/04_automatic_gain.ja.md) | [第 3 章](README.ja.md) | [ホーム](../README.ja.md) | [3-1. 用意するもの](01_parts.ja.md) |
