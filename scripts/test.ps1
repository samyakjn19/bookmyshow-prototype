$ErrorActionPreference = "Stop"
Set-Location (Join-Path (Split-Path -Parent $PSScriptRoot) "backend")
.\.venv\Scripts\pytest.exe -q
