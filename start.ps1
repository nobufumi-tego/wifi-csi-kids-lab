# wifi-csi-kids-lab: one-click start (Windows PowerShell) / ワンクリック起動
#
# Easiest: double-click start.bat in Explorer. / いちばん簡単なのは start.bat のダブルクリック
#
# 1. installs uv if missing (user folder, no admin rights) / uv がなければ入れる
# 2. installs the Python packages (uv sync)               / 必要なものを入れる
# 3. starts JupyterLab and opens the README               / JupyterLab で README を開く
#
# Stop: Ctrl+C twice. / 止めるとき: Ctrl+C を 2 回

$ErrorActionPreference = "Stop"
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::InputEncoding  = [System.Text.Encoding]::UTF8
    $OutputEncoding           = [System.Text.Encoding]::UTF8
} catch { }
Set-Location -Path $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Wi-Fi CSI Kids Lab" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv (https://astral.sh/uv/install.ps1) / uv を入れます..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:PATH"
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "uv was installed but not found. Close this window and start again." -ForegroundColor Red
        Write-Host "uv が見つかりません。ウィンドウを閉じて、もう一度起動してください。" -ForegroundColor Red
        exit 1
    }
}
Write-Host "uv: $(uv --version)" -ForegroundColor Green

Write-Host ""
Write-Host "Installing packages. The first time takes a few minutes. Please wait." -ForegroundColor Yellow
Write-Host "必要なものを入れています。はじめては数分かかります。「応答なし」と出ても待ってね。" -ForegroundColor Yellow
uv sync

$page = "README.md"
if ((Get-Culture).Name -like "ja*") { $page = "README.ja.md" }
Write-Host ""
Write-Host "Starting JupyterLab. Your browser will open. / ブラウザが開きます。" -ForegroundColor Cyan
uv run lab.py $page
