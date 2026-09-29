"""Markdown / Jupyter notebook 内の相対リンクとアンカーの生死をチェックする.

このリポジトリは「ファイル名は必ずリンクにする」「章末にナビゲーションブロックを置く」
という規約 (AGENTS.md 参照) で運用しているため、リンクの数が多く、
見出しを書き換えたときにアンカーが静かに壊れやすい。

    uv run python scripts/check_links.py           # チェックのみ (壊れていたら exit 1)
    uv run python scripts/check_links.py --quiet   # 問題があるものだけ表示

CI (`.github/workflows/ci.yml`) から push / PR 毎に自動実行される。
由来: learning-math リポジトリの同名スクリプト (MIT)。

## 検出するもと
1. **リンク先ファイルが存在しない** — `[text](path/to/missing.md)`
2. **アンカーが見つからない** — `[text](file.md#見出し)` の `#見出し` が実在しない

## 検出しないもの
- 外部 URL (`http://`, `https://`, `mailto:`) — ネットワークに依存させないため
- `EXCLUDE_DIRS` 配下 (`.git`, `.ipynb_checkpoints` など)
- `TEMPLATE_FILES` (AGENTS.md など。`prev.md` `<相対パス>` のような雛形を含むため)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# 走査対象の拡張子
TARGET_SUFFIXES: tuple[str, ...] = (".md", ".ipynb")

# 走査から除外するディレクトリ名
EXCLUDE_DIRS: frozenset[str] = frozenset(
    {".git", ".ipynb_checkpoints", "node_modules", ".venv", "__pycache__", ".pio"}
)

# リンクの雛形 (prev.md, <相対パス> など) を含むため除外するファイル
TEMPLATE_FILES: frozenset[str] = frozenset(
    {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "docs/maintainers/page_template.md"}
)

# チェックしないリンクの接頭辞 (外部リンクはネットワーク依存なので対象外)
EXTERNAL_PREFIXES: tuple[str, ...] = ("http://", "https://", "mailto:", "data:", "tel:")

# Markdown のインラインリンク `[text](target)`
LINK_PATTERN: re.Pattern[str] = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# ATX 見出し `## 見出し`
HEADING_PATTERN: re.Pattern[str] = re.compile(r"^(#{1,6})\s+(.*)$")

# アンカー生成で「そのまま残す」文字 (空白は後段でハイフンに変換)
ANCHOR_KEPT_CHARS: frozenset[str] = frozenset({" ", "-", "_"})

# アンカー生成で残す Unicode 一般カテゴリの先頭文字 (Letter / Number / Mark)
ANCHOR_KEPT_CATEGORIES: frozenset[str] = frozenset({"L", "N", "M"})

# カテゴリ的には Mark だが、アンカーには残さない不可視文字。
# 絵文字の異体字セレクタ (U+FE00-U+FE0F) と ZWJ (U+200D)。
# 「🗣️」のような絵文字は本体が Symbol として落ちるのに、
# 付随する VS16 だけが Mark として残ってしまうため明示的に除外する。
INVISIBLE_CHARS: frozenset[str] = frozenset(
    [chr(cp) for cp in range(0xFE00, 0xFE10)] + ["‍", "️", "​"]
)


@dataclass(frozen=True)
class Problem:
    """リンクの問題 1 件.

    Attributes:
        source: リンクが書かれているファイル (リポジトリルートからの相対パス)。
        link: 元のリンク文字列。
        kind: "missing-file" または "missing-anchor"。
        hint: 修正のヒント (近そうな候補など)。空文字なら候補なし。
    """

    source: str
    link: str
    kind: str
    hint: str = ""


def github_anchor(heading_text: str) -> str:
    """見出しテキストから GitHub 互換のアンカー文字列を作る.

    GitHub (github-slugger) の規則に合わせて、
    小文字化 → 文字・数字・結合文字・空白・ハイフン・アンダースコア以外を除去
    → 空白をハイフンに変換、という順で処理する。

    Args:
        heading_text: `#` を除いた見出し本文 (例: "3. 共役モデル① Bernoulli–Beta")。

    Returns:
        アンカー文字列 (先頭の `#` は含まない)。
    """
    lowered = heading_text.strip().lower()
    kept = [
        ch
        for ch in lowered
        if ch not in INVISIBLE_CHARS
        and (ch in ANCHOR_KEPT_CHARS or unicodedata.category(ch)[0] in ANCHOR_KEPT_CATEGORIES)
    ]
    return "".join(kept).replace(" ", "-")


def strip_inline_markdown(text: str) -> str:
    """見出し中のインライン記法を落として、アンカー計算用の素のテキストにする.

    GitHub は `## **太字** の見出し` の `**` を除いてからアンカーを作る。
    リンク `[表示](url)` は表示テキストだけが残る。

    Args:
        text: 見出し本文。

    Returns:
        記法を落としたテキスト。
    """
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # [表示](url) -> 表示
    text = re.sub(r"[*_`~]", "", text)  # 強調・コード・打消し
    return text


def collect_anchors(md_path: Path) -> set[str]:
    """Markdown ファイル内のすべての見出しアンカーを集める.

    同じ見出しが複数あるとき GitHub は `-1`, `-2` と連番を振るので、
    それも候補に加える。

    Args:
        md_path: 対象の Markdown ファイル。

    Returns:
        アンカー文字列の集合。
    """
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    in_code_block = False

    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = HEADING_PATTERN.match(line)
        if match is None:
            continue

        base = github_anchor(strip_inline_markdown(match.group(2)))
        if not base:
            continue

        count = seen.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        seen[base] = count + 1

    return anchors


def extract_markdown_text(path: Path) -> str:
    """ファイルから Markdown 本文を取り出す.

    `.ipynb` の場合は markdown セルだけを連結する
    (code セルの文字列リテラルを誤検出しないため)。

    Args:
        path: `.md` または `.ipynb` のパス。

    Returns:
        Markdown テキスト。読めなかった場合は空文字。
    """
    if path.suffix == ".ipynb":
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return ""
        return "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
            if cell.get("cell_type") == "markdown"
        )
    return path.read_text(encoding="utf-8")


def iter_target_files(root: Path) -> list[Path]:
    """走査対象のファイルを列挙する.

    Args:
        root: リポジトリのルートディレクトリ。

    Returns:
        ソート済みのファイルパス一覧。
    """
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.suffix not in TARGET_SUFFIXES or not path.is_file():
            continue
        if EXCLUDE_DIRS & set(path.relative_to(root).parts):
            continue
        if path.relative_to(root).as_posix() in TEMPLATE_FILES:
            continue
        files.append(path)
    return files


def suggest_anchor(wanted: str, available: set[str]) -> str:
    """壊れたアンカーに近い候補を探す.

    「見出しに語を付け足した (統計学入門 -> 統計学入門-赤本)」という
    このリポジトリで実際に起きたパターンを主に拾う。

    Args:
        wanted: リンクが指していたアンカー。
        available: そのファイルに実在するアンカーの集合。

    Returns:
        候補が 1 つに絞れたら `#候補`、絞れなければ空文字。
    """
    candidates = sorted(a for a in available if a.startswith(wanted) or wanted.startswith(a))
    if not candidates:
        candidates = sorted(a for a in available if wanted in a or a in wanted)
    if len(candidates) == 1:
        return f"もしかして: #{candidates[0]}"
    if candidates:
        return "候補: " + ", ".join(f"#{c}" for c in candidates[:3])
    return ""


def check_file(path: Path, root: Path) -> list[Problem]:
    """1 ファイル分のリンクをチェックする.

    Args:
        path: チェック対象のファイル。
        root: リポジトリのルート (相対パス表示用)。

    Returns:
        見つかった問題の一覧。
    """
    problems: list[Problem] = []
    source = path.relative_to(root).as_posix()
    text = extract_markdown_text(path)

    for link in LINK_PATTERN.findall(text):
        if link.startswith(EXTERNAL_PREFIXES):
            continue

        path_part, _, fragment = link.partition("#")
        target = (path.parent / path_part).resolve() if path_part else path.resolve()

        if not target.exists():
            problems.append(Problem(source, link, "missing-file"))
            continue

        # アンカーを検証できるのは Markdown だけ (.ipynb の見出しは GitHub 上で
        # アンカーが付かないことがあるため対象外)
        if not fragment or target.suffix != ".md":
            continue

        anchors = collect_anchors(target)
        if fragment not in anchors:
            problems.append(
                Problem(source, link, "missing-anchor", suggest_anchor(fragment, anchors))
            )

    return problems


def main() -> int:
    """エントリポイント.

    Returns:
        終了コード。問題がなければ 0、あれば 1。
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="リポジトリのルート (既定: このスクリプトの 1 つ上)",
    )
    parser.add_argument("--quiet", action="store_true", help="問題だけを表示する")
    args = parser.parse_args()

    root: Path = args.root.resolve()
    files = iter_target_files(root)

    problems: list[Problem] = []
    for path in files:
        problems.extend(check_file(path, root))

    if not args.quiet:
        print(f"走査: {len(files)} ファイル (.md / .ipynb)")

    missing_files = [p for p in problems if p.kind == "missing-file"]
    missing_anchors = [p for p in problems if p.kind == "missing-anchor"]

    if missing_files:
        print(f"\n❌ リンク先ファイルが存在しない: {len(missing_files)} 件")
        for problem in missing_files:
            print(f"   {problem.source}: {problem.link}")

    if missing_anchors:
        print(f"\n⚠️  アンカーが見つからない: {len(missing_anchors)} 件")
        for problem in missing_anchors:
            suffix = f"   ({problem.hint})" if problem.hint else ""
            print(f"   {problem.source}: {problem.link}{suffix}")

    if problems:
        print(f"\n合計 {len(problems)} 件の問題が見つかりました。")
        return 1

    if not args.quiet:
        print("✅ リンク切れ・アンカー切れはありません")
    return 0


if __name__ == "__main__":
    sys.exit(main())
