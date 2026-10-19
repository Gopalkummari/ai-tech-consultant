# PowerShell Launcher for AI Tech Consultant Master Web App
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting AI Tech Consultant - Unified Master Web App" -ForegroundColor Green
Write-Host "Freeing port 8000 if previously occupied..." -ForegroundColor DarkGray
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { 
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue 
}
Write-Host "Master Web App URL : http://localhost:8000" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

python app.py
