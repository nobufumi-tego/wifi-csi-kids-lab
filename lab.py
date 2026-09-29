"""Start JupyterLab with this repository's settings / このリポジトリの設定で JupyterLab を起動する.

Sets ``JUPYTERLAB_SETTINGS_DIR`` to ``.jupyter/lab/user-settings`` so that:

- ``.md`` files open as a formatted page (Markdown Preview), not as plain text
- JupyterLab does not fetch news from the internet

Usage / 使い方::

    uv run lab.py                  # start JupyterLab
    uv run lab.py README.ja.md     # start and open a page

The start scripts (start.sh / start.ps1 / start.bat) call this for you.
Stop: press Ctrl+C twice in the terminal. / 止めるときはターミナルで Ctrl+C を 2 回。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SETTINGS_SUBDIR: tuple[str, ...] = (".jupyter", "lab", "user-settings")


def main() -> int:
    """Start JupyterLab with the repository settings.

    Returns:
        JupyterLab's exit code (0 = normal).
    """
    repo_root = Path(__file__).parent.resolve()
    settings_dir = repo_root.joinpath(*SETTINGS_SUBDIR)
    env = os.environ.copy()
    if settings_dir.is_dir():
        env["JUPYTERLAB_SETTINGS_DIR"] = str(settings_dir)
    else:
        print(f"Settings not found, using defaults: {settings_dir}", file=sys.stderr)

    print("Starting JupyterLab... / JupyterLab を起動します")
    print("-" * 60)
    print("To stop: press Ctrl+C twice here. Closing the browser tab does NOT stop it.")
    print("止めるとき: ここで Ctrl+C を 2 回。ブラウザを閉じるだけでは止まりません。")
    print("-" * 60)
    cmd = [sys.executable, "-m", "jupyter", "lab", *sys.argv[1:]]
    try:
        return subprocess.run(cmd, env=env, cwd=repo_root, check=False).returncode
    except FileNotFoundError:
        print("JupyterLab is not installed. Run: uv sync / まず uv sync を実行してください",
              file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nJupyterLab stopped. / 終了しました")
        return 0


if __name__ == "__main__":
    sys.exit(main())
