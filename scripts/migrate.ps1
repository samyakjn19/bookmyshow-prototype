$ErrorActionPreference = "Stop"
$backend = Join-Path (Split-Path -Parent $PSScriptRoot) "backend"
Set-Location $backend
$env:PYTHONPATH = $backend
.\.venv\Scripts\alembic.exe upgrade head
