$ErrorActionPreference = "Stop"

Push-Location "$PSScriptRoot/../trading-engine"
try {
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
    }

    . .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}
finally {
    Pop-Location
}

Write-Host "Local backend environment is ready. Copy .env.example to .env if needed; never commit .env."
