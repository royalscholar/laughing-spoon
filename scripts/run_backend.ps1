$ErrorActionPreference = "Stop"

$env:BOT_MODE = "paper"
$env:LIVE_TRADING_ENABLED = "false"
$env:MANUAL_APPROVAL_REQUIRED = "true"
$env:KILL_SWITCH_ACTIVE = "false"

Push-Location "$PSScriptRoot/../trading-engine"
try {
    if (Test-Path ".venv/Scripts/Activate.ps1") {
        . .\.venv\Scripts\Activate.ps1
    }

    uvicorn main:app --reload
}
finally {
    Pop-Location
}
