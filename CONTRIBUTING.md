English | [日本語](CONTRIBUTING.ja.md)

# Contributing

Thank you for helping! Kids, parents, teachers and engineers are all welcome.

- **Issues are welcome.** Did you find something confusing, a typo, or a bug? Did
  you think of a new project idea? Open an issue and describe what happened.
- **Keep it kid-friendly.** Short sentences, simple words, and explain new terms.
- **Bilingual rule.** Every lesson or guide `X.md` (English) needs `X.ja.md`
  (Japanese). The Japanese should sound natural, not like a word-for-word translation.
  The tests check that both files exist.
- **Run the checks before a pull request:**

  ```bash
  uv run pytest
  uv run ruff check src tests
  uv run mypy src
  ```

- **No personal data.** Never add recordings of real people or homes, names,
  addresses, school names, or photos of faces. Recordings belong in `data/`, which is
  git-ignored.
- Code style: see "For maintainers" in [AGENTS.md](AGENTS.md).

By contributing, you agree that code is released under MIT ([LICENSE](LICENSE)) and
documents under CC BY 4.0 ([LICENSE-docs](LICENSE-docs)).
