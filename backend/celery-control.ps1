param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('start', 'stop', 'close', 'restart', 'status')]
    [string]$Action
)

$ErrorActionPreference = 'Stop'

$BackendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RunDir = Join-Path $BackendDir '.run'
$LogDir = Join-Path $BackendDir 'logs'
$WorkerPidFile = Join-Path $RunDir 'celery-worker.pid'
$BeatPidFile = Join-Path $RunDir 'celery-beat.pid'
$WorkerOutLog = Join-Path $LogDir 'celery-worker.out.log'
$WorkerErrLog = Join-Path $LogDir 'celery-worker.err.log'
$BeatOutLog = Join-Path $LogDir 'celery-beat.out.log'
$BeatErrLog = Join-Path $LogDir 'celery-beat.err.log'

function Ensure-Dirs {
    if (-not (Test-Path $RunDir)) { New-Item -Path $RunDir -ItemType Directory | Out-Null }
    if (-not (Test-Path $LogDir)) { New-Item -Path $LogDir -ItemType Directory | Out-Null }
}

function Get-PythonCommand {
    $venvPython = Join-Path $BackendDir '.venv\Scripts\python.exe'
    if (Test-Path $venvPython) {
        return $venvPython
    }
    return 'python'
}

function Get-RunningProcessFromPidFile {
    param([string]$PidFile)

    if (-not (Test-Path $PidFile)) {
        return $null
    }

    $pidText = (Get-Content -Path $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ([string]::IsNullOrWhiteSpace($pidText)) {
        Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
        return $null
    }

    $pidValue = 0
    if (-not [int]::TryParse($pidText, [ref]$pidValue)) {
        Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
        return $null
    }

    $proc = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
    if ($null -eq $proc) {
        Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
        return $null
    }

    return $proc
}

function Find-CeleryProcessByRole {
    param([ValidateSet('worker', 'beat')][string]$Role)

    try {
        $matched = Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
            $cmd = $_.CommandLine
            if ([string]::IsNullOrWhiteSpace($cmd)) { return $false }
            $hasCelery = $cmd -match '(?i)\bcelery\b'
            $hasApp = $cmd -match '(?i)(^|\s)-A\s+celery_app(\s|$)'
            $hasRole = $cmd -match ("(?i)\b" + $Role + "\b")
            return $hasCelery -and $hasApp -and $hasRole
        } | Select-Object -First 1

        if ($null -eq $matched) {
            return $null
        }

        return Get-Process -Id $matched.ProcessId -ErrorAction SilentlyContinue
    } catch {
        return $null
    }
}

function Resolve-CeleryProcess {
    param(
        [ValidateSet('worker', 'beat')][string]$Role,
        [string]$PidFile
    )

    $proc = Get-RunningProcessFromPidFile -PidFile $PidFile
    if ($proc) {
        return $proc
    }

    $proc = Find-CeleryProcessByRole -Role $Role
    if ($proc) {
        Ensure-Dirs
        Set-Content -Path $PidFile -Value $proc.Id
    }
    return $proc
}

function Start-Celery {
    Ensure-Dirs

    $workerProc = Resolve-CeleryProcess -Role 'worker' -PidFile $WorkerPidFile
    $beatProc = Resolve-CeleryProcess -Role 'beat' -PidFile $BeatPidFile
    if ($workerProc -and $beatProc) {
        Write-Host "Celery is already running. worker=$($workerProc.Id), beat=$($beatProc.Id)"
        return
    }

    $pythonCmd = Get-PythonCommand

    if (-not $workerProc) {
        $worker = Start-Process -FilePath $pythonCmd `
            -ArgumentList '-m celery -A celery_app worker --loglevel=info -Q salt,scheduler' `
            -WorkingDirectory $BackendDir `
            -RedirectStandardOutput $WorkerOutLog `
            -RedirectStandardError $WorkerErrLog `
            -PassThru
        Set-Content -Path $WorkerPidFile -Value $worker.Id
        Write-Host "Started celery worker. pid=$($worker.Id)"
    } else {
        Write-Host "Celery worker already running. pid=$($workerProc.Id)"
    }

    if (-not $beatProc) {
        $beat = Start-Process -FilePath $pythonCmd `
            -ArgumentList '-m celery -A celery_app beat --loglevel=info' `
            -WorkingDirectory $BackendDir `
            -RedirectStandardOutput $BeatOutLog `
            -RedirectStandardError $BeatErrLog `
            -PassThru
        Set-Content -Path $BeatPidFile -Value $beat.Id
        Write-Host "Started celery beat. pid=$($beat.Id)"
    } else {
        Write-Host "Celery beat already running. pid=$($beatProc.Id)"
    }
}

function Stop-Celery {
    $workerProc = Resolve-CeleryProcess -Role 'worker' -PidFile $WorkerPidFile
    $beatProc = Resolve-CeleryProcess -Role 'beat' -PidFile $BeatPidFile

    if ($workerProc) {
        Stop-Process -Id $workerProc.Id -Force
        Write-Host "Stopped celery worker. pid=$($workerProc.Id)"
    } else {
        Write-Host 'Celery worker is not running.'
    }

    if ($beatProc) {
        Stop-Process -Id $beatProc.Id -Force
        Write-Host "Stopped celery beat. pid=$($beatProc.Id)"
    } else {
        Write-Host 'Celery beat is not running.'
    }

    Remove-Item -Path $WorkerPidFile -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $BeatPidFile -Force -ErrorAction SilentlyContinue
}

function Show-CeleryStatus {
    $workerProc = Resolve-CeleryProcess -Role 'worker' -PidFile $WorkerPidFile
    $beatProc = Resolve-CeleryProcess -Role 'beat' -PidFile $BeatPidFile

    if ($workerProc) {
        Write-Host "worker: running (pid=$($workerProc.Id))"
    } else {
        Write-Host 'worker: stopped'
    }

    if ($beatProc) {
        Write-Host "beat: running (pid=$($beatProc.Id))"
    } else {
        Write-Host 'beat: stopped'
    }
}

switch ($Action) {
    'start' { Start-Celery }
    'stop' { Stop-Celery }
    'close' { Stop-Celery }
    'restart' { Stop-Celery; Start-Celery }
    'status' { Show-CeleryStatus }
}
