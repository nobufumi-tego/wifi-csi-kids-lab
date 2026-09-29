English | [日本語](CONTRIBUTING.ja.md)

# Contributing

Thank you for helping! Kids, parents, teachers and engineers are all welcome.

- **Issues are welcome.** Did you find something confusing, a typo, or a bug? Did
  you think of a new project idea? Open an issue and describe what happened.
- **Keep it kid-friendly.** Short sentences, simple words, and explain new terms.
- **Follow the page template.** Chapters are folders (`01_waves/` …), one topic per
  page, with a language-switch line at the top and a navigation table at the end.
  See [`docs/maintainers/page_template.md`](docs/maintainers/page_template.md).
- **Bilingual rule.** Every page `X.md` (English) needs `X.ja.md` (Japanese). The
  Japanese should sound natural, not like a word-for-word translation. The tests check
  that both files exist and that every page has its navigation table.
- **Run the checks before a pull request:**

  ```bash
  uv run pytest tests/ -v
  uv run ruff check src/ tests/ lab.py scripts/
  uv run mypy src/ lab.py scripts/
  uv run python scripts/check_links.py   # links and #anchors
  ```

- **No personal data.** Never add recordings of real people or homes, names,
  addresses, school names, or photos of faces. Recordings belong in `data/`, which is
  git-ignored.
- Code style: see "For maintainers" in [AGENTS.md](AGENTS.md).

By contributing, you agree that code is released under MIT ([LICENSE-CODE](LICENSE-CODE)) and
documents under CC BY 4.0 ([LICENSE-DOCS](LICENSE-DOCS)). Overview: [LICENSE](LICENSE).
