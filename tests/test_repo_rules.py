"""Rules for the repository itself: bilingual pages, navigation tables, links, no recordings."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
#: English-only on purpose (instructions for AI tools).
ENGLISH_ONLY = {"AGENTS.md", "CLAUDE.md", "GEMINI.md"}
#: Maintainer notes, not learning material (no Japanese pair / navigation needed).
MAINTAINER_PREFIXES = (
    "docs/maintainers/", "docs/tasks/", "docs/decisions/", ".githooks/", ".github/",
    ".claude/", ".gemini/", "firmware/",
)
#: Top-level files that are not part of the page-to-page navigation.
NO_NAV_FILES = {"README.md", "README.ja.md", "CONTRIBUTING.md", "CONTRIBUTING.ja.md",
                "DISCLAIMER.md", "DISCLAIMER.ja.md"}
NAV_HEADINGS = {".md": "## 📍 Navigation", ".ja.md": "## 📍 ナビゲーション"}


def _files(pattern: str) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", pattern],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("git is not available")
    return [ROOT / p for p in out.split() if (ROOT / p).exists()]


def _learning_pages() -> list[Path]:
    pages = []
    for p in _files("*.md"):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(MAINTAINER_PREFIXES) or rel in ENGLISH_ONLY:
            continue
        pages.append(p)
    return pages


def test_every_english_page_has_a_japanese_page() -> None:
    missing = [
        str(p.relative_to(ROOT))
        for p in _learning_pages()
        if not p.name.endswith(".ja.md") and not p.with_name(p.stem + ".ja.md").exists()
    ]
    assert not missing, f"add a .ja.md version for: {missing}"


def test_every_japanese_page_has_an_english_page() -> None:
    orphans = [
        str(p.relative_to(ROOT))
        for p in _learning_pages()
        if p.name.endswith(".ja.md")
        and not p.with_name(p.name[: -len(".ja.md")] + ".md").exists()
    ]
    assert not orphans, f"add an English version for: {orphans}"


def test_every_page_ends_with_a_navigation_table() -> None:
    missing = []
    for p in _learning_pages():
        rel = p.relative_to(ROOT).as_posix()
        if rel in NO_NAV_FILES:
            continue
        heading = NAV_HEADINGS[".ja.md"] if p.name.endswith(".ja.md") else NAV_HEADINGS[".md"]
        if heading not in p.read_text(encoding="utf-8"):
            missing.append(rel)
    assert not missing, f"add the navigation table (docs/maintainers/page_template.md): {missing}"


def test_links_and_anchors() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_links.py"), "--quiet"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_no_recordings_are_committed() -> None:
    data_files = [p for p in _files("data/*") if p.name not in {"README.md", "README.ja.md"}]
    assert not data_files and not _files("*.csv"), "recordings must stay on your own computer"
