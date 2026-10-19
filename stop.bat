@echo off
echo Stopping all running instances on ports 8001, 8002, 8003...
powershell -Command "Get-NetTCPConnection -LocalPort 8001, 8002, 8003 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" 2>nul
echo All 3 tasks stopped.
