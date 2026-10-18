@echo off
echo ========================================================
echo Starting AI Tech Consultant Capstone Suite
echo Task 1 (Knowledge Brain)  : http://localhost:8001
echo Task 2 (The Inbox Agent)  : http://localhost:8002
echo Task 3 (Meeting to Scope) : http://localhost:8003
echo ========================================================

start "Task 1 - Knowledge Brain" python task1-brain/main.py
timeout /t 2 /nobreak >nul

start "Task 2 - Inbox Agent" node task2-inbox/dist/index.js
timeout /t 2 /nobreak >nul

start "Task 3 - Meeting Scoper" python task3-scoper/main.py
timeout /t 2 /nobreak >nul

echo All 3 tasks started successfully!
echo Run 'python evaluate_all.py' to run the 60-test evaluation suite.
