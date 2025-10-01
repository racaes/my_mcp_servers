Param(
    [string]$EnvName = ".venv",
    [switch]$Force
)

$venvPath = Join-Path -Path (Get-Location) -ChildPath $EnvName

function Stop-VenvPythonProcesses {
    param(
        [string]$PathPrefix
    )

    $procs = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.Path -and ($_.Path.StartsWith($PathPrefix, [System.StringComparison]::OrdinalIgnoreCase))
    }

    foreach ($proc in $procs) {
        try {
            Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            Write-Host "Stopped python process $($proc.Id) locking $PathPrefix" -ForegroundColor Yellow
        } catch {
            Write-Warning "Failed to stop process $($proc.Id): $_"
        }
    }

    return $procs
}

if ($env:VIRTUAL_ENV) {
    try {
        $activePath = (Resolve-Path $env:VIRTUAL_ENV -ErrorAction Stop).Path
        $targetPath = $venvPath
        if ($activePath -eq $targetPath) {
            Write-Host "The target virtual environment ($targetPath) is currently active. Please run 'deactivate' before re-creating it." -ForegroundColor Red
            return
        }
    } catch {
        Write-Verbose "Unable to resolve currently active virtual environment path: $_"
    }
}

if (Test-Path $venvPath -PathType Container) {
    if (-not $Force) {
        Write-Host "Virtual environment already exists at $venvPath. Use -Force to recreate." -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Removing existing environment at $venvPath" -ForegroundColor Yellow
    try {
        Remove-Item -Recurse -Force $venvPath -ErrorAction Stop
    } catch {
        Write-Warning "Initial removal failed: $_"
        $stopped = Stop-VenvPythonProcesses -PathPrefix $venvPath
        if ($stopped.Count -eq 0) {
            Write-Warning "No python processes matched $venvPath. Manual cleanup may be required."
        }

        Remove-Item -Recurse -Force $venvPath -ErrorAction Stop
    }
}

Write-Host "Creating virtual environment at $venvPath" -ForegroundColor Cyan
python -m venv $venvPath

$venvPython = Join-Path $venvPath "Scripts/python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Failed to locate python executable at $venvPython. Did virtual environment creation succeed?" -ForegroundColor Red
    exit 1
}

Write-Host "Activating environment and installing dependencies" -ForegroundColor Cyan
$activate = Join-Path $venvPath "Scripts/Activate.ps1"
& $activate

if (Test-Path "pyproject.toml") {
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install ".[dev]"
} elseif (Test-Path "requirements.txt") {
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r requirements.txt
} else {
    Write-Host "No pyproject.toml or requirements.txt found. Install dependencies manually." -ForegroundColor Yellow
}
