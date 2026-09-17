# ComplaintIQ - One-command launcher (PowerShell)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend  = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Venv     = Join-Path $Backend "venv"
$Pip      = Join-Path $Venv "Scripts\pip.exe"
$Uvicorn  = Join-Path $Venv "Scripts\uvicorn.exe"

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host "    ComplaintIQ - AI Complaint Center" -ForegroundColor Cyan
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try { python --version | Out-Null } catch {
    Write-Host "  [ERROR] Python not found!" -ForegroundColor Red; exit 1
}

# Setup venv
if (-not (Test-Path $Venv)) {
    Write-Host "  [SETUP] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $Venv
    Write-Host "  [SETUP] Installing backend dependencies (first run only)..." -ForegroundColor Yellow
    & $Pip install -r "$Backend\requirements.txt" --quiet
    Write-Host "  [SETUP] Done!" -ForegroundColor Green
}

# .env check
$EnvFile = Join-Path $Backend ".env"
if (-not (Test-Path $EnvFile)) {
    Copy-Item "$Backend\.env.example" $EnvFile
    Write-Host "  [WARN] .env created. Set your OPENAI_API_KEY in backend\.env" -ForegroundColor Yellow
}

Write-Host "  Starting Backend  --> http://localhost:8000" -ForegroundColor Green
Write-Host "  Starting Frontend --> http://localhost:5500" -ForegroundColor Green
Write-Host "  API Docs          --> http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "  Press Ctrl+C to stop both servers." -ForegroundColor Gray
Write-Host "  ========================================" -ForegroundColor Cyan
Write-Host ""

# Start backend job
$BackendJob = Start-Job -Name "Backend" -ScriptBlock {
    param($venv, $backend)
    & "$venv\Scripts\uvicorn.exe" main:app --reload --port 8000 --host 0.0.0.0 --app-dir $backend 2>&1
} -ArgumentList $Venv, $Backend

# Start frontend job
$FrontendJob = Start-Job -Name "Frontend" -ScriptBlock {
    param($frontend)
    python -m http.server 5500 --directory $frontend 2>&1
} -ArgumentList $Frontend

Start-Sleep -Seconds 3
Start-Process "http://localhost:5500"

Write-Host "  [OK] Both servers running! Browser opened." -ForegroundColor Green
Write-Host "  Streaming logs below (Ctrl+C to exit):" -ForegroundColor Gray
Write-Host ""

# Stream logs from both jobs
try {
    while ($true) {
        Receive-Job -Job $BackendJob  | ForEach-Object { Write-Host "  [BACKEND]  $_" -ForegroundColor Blue }
        Receive-Job -Job $FrontendJob | ForEach-Object { Write-Host "  [FRONTEND] $_" -ForegroundColor Magenta }
        Start-Sleep -Milliseconds 500
    }
} finally {
    Write-Host "`n  Stopping servers..." -ForegroundColor Yellow
    Stop-Job  $BackendJob, $FrontendJob
    Remove-Job $BackendJob, $FrontendJob -Force
    Write-Host "  Stopped. Goodbye!" -ForegroundColor Cyan
}
