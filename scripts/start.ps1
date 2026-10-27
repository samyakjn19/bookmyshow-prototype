$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "Starting Postgres..."
docker compose up -d db

Write-Host "Starting API..."
Set-Location backend
if (-not (Test-Path .venv)) {
  python -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
.\.venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
