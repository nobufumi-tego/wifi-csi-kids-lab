# wifi-csi-kids-lab — 進行中の作業

種類: プロジェクト

<!-- 保守者のメモ。学習者向けではない（学習者向けは README / lessons）。 -->

## いま何をしているか

小中学生向けの公開教材の初版（Lv1〜5・ガイド・合成データ・ESP32 ファーム）を作成した。
設計は `docs/decisions/0001-public-kids-lab-design.md`。
構成を learning-math に合わせて章フォルダ化した（`docs/decisions/0002-learning-math-structure.md`）。

## 次の一手

- [ ] 実機（ESP32 2 台）で `firmware/` を書き込み、`csi-lab capture` で記録できるか確かめる
      （初版はコンパイル確認のみ。旧実装とは別に書き直したため未実測）
- [ ] Arduino-ESP32 コア 3.x でコンパイルできるか確かめる（Arduino IDE の既定は 3.x）
- [ ] 子ども（対象年齢）に第1〜2章を試してもらい、つまずいた所を直す
- [ ] start.bat / start.ps1 を Windows 実機で試す（Linux でしか確認していない）

## 待ち

（なし）
