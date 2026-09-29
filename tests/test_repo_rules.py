"""Rules for the repository itself: bilingual docs, working links, no recordings."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
#: Files that are English-only on purpose (instructions for AI tools / maintainers).
ENGLISH_ONLY = {"AGENTS.md", "CLAUDE.md", "GEMINI.md"}
#: Folders with maintainer notes (Japanese, not part of the learning material).
MAINTAINER_DIRS = {"docs", ".githooks", ".github", "firmware"}
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")


def _tracked(pattern: str) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", pattern],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git is not available")
    return [ROOT / p for p in out.split()]


def _learning_docs() -> list[Path]:
    docs = []
    for p in _tracked("*.md"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in MAINTAINER_DIRS or rel.name in ENGLISH_ONLY:
            continue
        docs.append(p)
    return docs


def test_every_english_doc_has_a_japanese_version() -> None:
    missing = [
        str(p.relative_to(ROOT))
        for p in _learning_docs()
        if not p.name.endswith(".ja.md") and not p.with_name(p.stem + ".ja.md").exists()
    ]
    assert not missing, f"add a .ja.md version for: {missing}"


def test_every_japanese_doc_has_an_english_version() -> None:
    orphans = [
        str(p.relative_to(ROOT))
        for p in _learning_docs()
        if p.name.endswith(".ja.md") and not p.with_name(p.name[: -len(".ja.md")] + ".md").exists()
    ]
    assert not orphans, f"add an English version for: {orphans}"


def test_relative_links_point_to_existing_files() -> None:
    broken = []
    for p in _tracked("*.md"):
        for target in LINK.findall(p.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target):
                continue  # http:, https:, mailto:
            if not (p.parent / target).exists():
                broken.append(f"{p.relative_to(ROOT)} -> {target}")
    assert not broken, "broken links:\n" + "\n".join(broken)


def test_no_recordings_are_committed() -> None:
    data_files = [p for p in _tracked("data/*") if p.name not in {"README.md", "README.ja.md"}]
    csvs = _tracked("*.csv")
    assert not data_files and not csvs, "recordings must stay on your own computer"
