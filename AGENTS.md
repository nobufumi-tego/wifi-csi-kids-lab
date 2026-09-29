# wifi-csi-kids-lab — <一行で「何のためのリポジトリか」>

（何を解決するために作ったかを2〜3行。目的が書けないうちは、
まだプロジェクトとして立てる段階ではないかもしれない）

## Commands

```sh
# （動かし方・テスト・ビルド。まだ無ければこの節ごと消す）
```

## Architecture

```
docs/tasks/       進行中の作業（current.md）と後回し（backlog.md）
docs/decisions/   設計判断の記録（ADR・書き換えない）
```

## Watch out for（このリポは push される＝外に出る）

- **実在の連絡先・実名を書かない。** `~/.claude/hooks/pii-guard.py` が検査対象にする
- **機微案件のフォルダ名も書かない。** 名前だけで「誰の何の記録か」が特定できるため
- APIキー・秘密鍵は書かない。環境変数経由にする

## 関連

- グローバル規約: `~/.claude/CLAUDE.md`
- 運用フロー: `~/claude-code-ops/docs/operation-flow.md`
