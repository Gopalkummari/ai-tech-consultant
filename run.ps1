# PowerShell Single-Command Runner for AI Tech Consultant Capstone
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting AI Tech Consultant Capstone Suite" -ForegroundColor Green
Write-Host "Freeing ports 8001, 8002, 8003 if previously in use..." -ForegroundColor DarkGray
Get-NetTCPConnection -LocalPort 8001, 8002, 8003 -ErrorAction SilentlyContinue | ForEach-Object { 
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue 
}
Write-Host "Task 1 (Knowledge Brain)  : http://localhost:8001" -ForegroundColor Yellow
Write-Host "Task 2 (The Inbox Agent)  : http://localhost:8002" -ForegroundColor Yellow
Write-Host "Task 3 (Meeting to Scope) : http://localhost:8003" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

Start-Process python -ArgumentList "task1-brain/main.py"
Start-Sleep -Seconds 2

Start-Process node -ArgumentList "task2-inbox/dist/index.js"
Start-Sleep -Seconds 2

Start-Process python -ArgumentList "task3-scoper/main.py"
Start-Sleep -Seconds 2

Write-Host "All 3 services are running concurrently!" -ForegroundColor Green
Write-Host "To execute the 60-test evaluation suite: python evaluate_all.py" -ForegroundColor Cyan
