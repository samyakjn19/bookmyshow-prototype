$ErrorActionPreference = "Stop"
Set-Location (Join-Path (Split-Path -Parent $PSScriptRoot) "backend")
.\.venv\Scripts\python.exe -m app.db.seeds.run
