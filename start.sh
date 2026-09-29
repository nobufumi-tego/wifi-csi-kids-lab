#!/usr/bin/env bash
# wifi-csi-kids-lab: one-click start (Mac / Linux) / ワンクリック起動
#
#   ./start.sh
#
# 1. installs uv if missing (user folder, no admin rights) / uv がなければ入れる
# 2. installs the Python packages (uv sync)               / 必要なものを入れる
# 3. starts JupyterLab and opens the README               / JupyterLab で README を開く
#
# Stop: Ctrl+C twice. / 止めるとき: Ctrl+C を 2 回
# "Permission denied"? run: chmod +x start.sh

set -euo pipefail
cd "$(dirname "$0")"

echo "============================================================"
echo "  Wi-Fi CSI Kids Lab"
echo "============================================================"

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv (https://astral.sh/uv/install.sh) / uv を入れます..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    if ! command -v uv >/dev/null 2>&1; then
        echo "uv was installed but not found. Close this terminal, open a new one, and run ./start.sh again."
        echo "uv が見つかりません。ターミナルを開き直して、もう一度 ./start.sh を実行してください。"
        exit 1
    fi
fi
echo "uv: $(uv --version)"

echo ""
echo "Installing packages. The first time takes a few minutes. Please wait, do not press Ctrl+C."
echo "必要なものを入れています。はじめては数分かかります。Ctrl+C をおさずに待ってね。"
uv sync

page="README.md"
case "${LANG:-}" in ja*) page="README.ja.md" ;; esac
echo ""
echo "Starting JupyterLab. Your browser will open. / ブラウザが開きます。"
exec uv run lab.py "$page"
