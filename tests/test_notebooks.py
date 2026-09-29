"""Run every notebook from top to bottom so broken lessons are caught early."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted(p for p in ROOT.glob("*/notebooks/*.ipynb") if ".venv" not in p.parts)
TIMEOUT_S = 120  # per cell


def test_there_are_notebooks() -> None:
    assert NOTEBOOKS, "chapter folders should contain notebooks/*.ipynb"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: f"{p.parent.parent.name}/{p.name}")
def test_notebook_runs(path: Path, tmp_path: Path) -> None:
    nbformat = pytest.importorskip("nbformat")
    nbclient = pytest.importorskip("nbclient")
    pytest.importorskip("ipykernel")
    nb = nbformat.read(path, as_version=4)
    client = nbclient.NotebookClient(
        nb, timeout=TIMEOUT_S, kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    )
    client.execute()
