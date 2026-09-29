[English](CONTRIBUTING.md) | 日本語

# 協力してくれる人へ

手伝ってくれてありがとうございます。子ども、おうちの人、先生、エンジニア、だれでも大歓迎です。

- **Issue（気づいたことの報告）を歓迎します。** わかりにくいところ、書きまちがい、
  うまく動かないところを見つけたら教えてください。新しい自由研究のアイデアも歓迎です。
  何が起きたかを書いて、Issue を作ってください。
- **子どもにわかる言葉で書きます。** 文は短くし、やさしい言葉を使い、新しい言葉には説明をつけます。
- **ページのひな形に合わせます。** 章はフォルダ（`01_waves/` など）で、1 ページに 1 つの話題。
  いちばん上に言語の切りかえ、いちばん下にナビゲーションの表を置きます。
  くわしくは [`docs/maintainers/page_template.md`](docs/maintainers/page_template.md)（英語）を見てください。
- **2 か国語のきまりがあります。** 英語版 `X.md` には、日本語版 `X.ja.md` を必ずつけます。
  日本語は、英語をそのまま訳した文ではなく、自然な文にします。両方のファイルがそろっているか、
  どのページにもナビゲーションの表があるかは、テストで確かめます。
- **プルリクエストの前に、次のチェックを動かします。**

  ```bash
  uv run pytest tests/ -v
  uv run ruff check src/ tests/ lab.py scripts/
  uv run mypy src/ lab.py scripts/
  uv run python scripts/check_links.py   # リンクと #見出し へのリンクの確認
  ```

- **個人の情報は入れません。** 本物の人や家の記録、名前、住所、学校名、顔の写真は
  入れないでください。記録は `data/` に置きます。`data/` は git の管理から外してあります。
- プログラムの書き方は、[AGENTS.md](AGENTS.md) の「For maintainers」を見てください。

協力してもらったものは、プログラムは MIT（[LICENSE-CODE](LICENSE-CODE)）、文章は CC BY 4.0
（[LICENSE-DOCS](LICENSE-DOCS)）で公開されます。まとめは [LICENSE](LICENSE) にあります。
