@echo off
echo ========================================================
echo Starting AI Tech Consultant - Unified Master Web App
echo Freeing port 8000 if in use...
powershell -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" 2>nul
echo Master Web App URL : http://localhost:8000
echo ========================================================

python app.py
