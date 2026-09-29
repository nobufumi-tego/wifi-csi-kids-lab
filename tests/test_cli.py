from __future__ import annotations

from pathlib import Path

import pytest

from csi_lab import SCENARIOS, load_csv
from csi_lab.cli import main


def test_samples_and_show(tmp_path: Path) -> None:
    out = tmp_path / "samples"
    assert main(["samples", "--out", str(out)]) == 0
    for name in [*SCENARIOS, "story"]:
        assert (out / f"{name}.csv").is_file()
    story = load_csv(out / "story.csv")
    assert {"empty", "walk", "still", "wave"} <= set(story.labels)
    assert main(["show", str(out / "walk.csv")]) == 0
    assert (out / "walk.png").is_file()


def test_show_missing_file_is_a_clear_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["show", str(tmp_path / "none.csv")]) == 1
    assert "not found" in capsys.readouterr().err


def test_capture_rejects_bad_seconds(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["capture", "--label", "x", "--seconds", "0", "--port", "dummy"]) == 1
    assert "positive" in capsys.readouterr().err
