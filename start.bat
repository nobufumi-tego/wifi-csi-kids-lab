@echo off
REM ====================================================================
REM   wifi-csi-kids-lab: one-click start (Windows)
REM   Double-click this file in Explorer.
REM
REM   This file is pure ASCII on purpose: CMD reads .bat files with the
REM   system codepage (CP932 on Japanese Windows), so Japanese text here
REM   would break. Japanese messages come from start.ps1.
REM
REM   It runs start.ps1 without changing your PowerShell settings
REM   (-ExecutionPolicy Bypass applies only to this run). No admin rights.
REM   Stop Jupyter Lab: press Ctrl+C twice in this window.
REM ====================================================================
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1"
echo.
echo ====================================================================
echo  Finished. Press any key to close this window.
echo ====================================================================
pause >nul
