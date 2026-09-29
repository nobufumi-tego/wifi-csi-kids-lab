# Page template and structure rules (maintainers)

The structure follows the sibling course
[learning-math](https://github.com/nobufumi-tego/learning-math) (chapters as folders,
one topic per page, notebooks and columns next to the pages, a navigation table at the
end of every page), adapted for young learners and for two languages.

## Layout

```text
README.md / README.ja.md        home page (every page links back here)
start_here/                      first steps: what is Wi-Fi sensing, terminal & uv, AI, safety
01_waves/ ... 05_machine_learning/   one chapter per level
06_free_research/                how to turn it into a free-research project
appendix/                        math map (links into learning-math), further resources
glossary/                        words used in the lessons
docs/                            for parents & teachers, learning path, setup, Jupyter guide
docs/maintainers/, docs/tasks/, docs/decisions/   maintainer notes (not learning material)
```

Each chapter folder:

```text
NN_chapter/
  README.md, README.ja.md        chapter top: goal, time, page table, notebook table, columns
  01_topic.md, 01_topic.ja.md    one topic per page, numbered in reading order
  notebooks/01_topic.ipynb       runnable version (bilingual markdown cells, no outputs saved)
  columns/01_story.md, .ja.md    optional reading ("コラム"): history, everyday life, ethics
```

- Folder and file names: lowercase, words joined with `_`, two-digit prefix for order.
- **Every English page `X.md` has a Japanese page `X.ja.md`** (tests enforce this).
  English pages link to English pages; Japanese pages link to `.ja.md` pages.
- Japanese is natural, kid-friendly (です/ます, short sentences, simple kanji, add
  readings for hard words), not a literal translation.
- A file name mentioned in text is always a link: ``[`02_wavelength.md`](02_wavelength.md)``.
- Formulas are LaTeX (`$\lambda = c / f$`); code blocks are for code only.
- Numbers quoted from the simulator must come from actually running the code; state the
  seed next to them. No invented numbers or sources.

## Page template (English)

````markdown
English | [日本語](01_topic.ja.md)

# 1-2. Wavelength and frequency — how long is one Wi-Fi wave?

One or two sentences: what you will find out on this page.

> 💡 **Run the code on this page**: start the lab (`./start.sh` or double-click
> `start.bat`, or `uv run lab.py`) and open [`notebooks/02_wavelength.ipynb`](notebooks/02_wavelength.ipynb).
> New to the terminal? → [Terminal and uv](../start_here/02_terminal_and_uv.md)

## (sections: intuition first, then try it, then details)

...

> 🤖 **Ask your AI**
> - "..."
> - "..."

## Check yourself

1. ...

<details><summary>Answers</summary>

1. ...

</details>

## 📐 Math behind this page

> These links go to **learning-math**, a separate math course written in Japanese for
> adults. Read them when you are older, or together with a grown-up.

- Sine waves: [三角関数](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/03_trigonometry.md)

---

## 📍 Navigation

| ← Prev | 🏠 Chapter | 📚 Home | Next → |
|---|---|---|---|
| [1-1. Radio waves](01_radio_waves.md) | [Chapter 1](README.md) | [Home](../README.md) | [1-3. Reflection](03_reflection.md) |
````

## Page template (Japanese)

````markdown
[English](01_topic.md) | 日本語

# 1-2. 波長と周波数 — Wi-Fi の波 1 つの長さは？

このページでわかることを 1〜2 文で。

> 💡 **このページのコードを動かすには**: ラボを起動して（`./start.sh` か `start.bat` を
> ダブルクリック、または `uv run lab.py`）、[`notebooks/02_wavelength.ipynb`](notebooks/02_wavelength.ipynb) を開きます。
> ターミナルがはじめての人 → [ターミナルと uv](../start_here/02_terminal_and_uv.ja.md)

## （本文: まず直感、次にためす、そのあとくわしく）

> 🤖 **AI に聞いてみよう**
> - 「…」

## たしかめよう

<details><summary>こたえ</summary> ... </details>

## 📐 このページの数学をもっと知りたい人へ

> リンク先は、大人向けの数学教材 **learning-math**（日本語）です。中学生以上の人や、
> おうちの人といっしょに読んでみてください。

- 波の形（サイン）: [三角関数](https://github.com/nobufumi-tego/learning-math/blob/main/start_here/03_trigonometry.md)

---

## 📍 ナビゲーション

| ← 前 | 🏠 章 TOP | 📚 全体 TOP | 次 → |
|---|---|---|---|
| [1-1. 電波ってなに？](01_radio_waves.ja.md) | [第 1 章](README.ja.md) | [ホーム](../README.ja.md) | [1-3. はね返り](03_reflection.ja.md) |
````

Rules for the navigation table:

- Every page (chapter pages, chapter READMEs, columns, `start_here/`) ends with it.
- First page of a chapter: "← Prev" = the chapter README. Last page: "Next →" = next
  chapter's README. Chapter README: prev = last page of the previous chapter, next = its
  first page. Columns: "Next →" = back to the main page they belong to.
- "📚 Home" is the root `README.md` / `README.ja.md` (`../README.md`, `../../README.md`).

## Math links

Links into learning-math use absolute URLs
`https://github.com/nobufumi-tego/learning-math/blob/main/<path>` and point to files,
not anchors (its headings may change). The full list with the matching pages here is
[`appendix/math_map.md`](../../appendix/math_map.md); keep the two in sync.

## Checks

```bash
uv run pytest tests/ -v                 # bilingual pairs, navigation tables, notebooks run
uv run python scripts/check_links.py    # links and #anchors
```
