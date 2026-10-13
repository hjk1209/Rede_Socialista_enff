$ErrorActionPreference = "Stop"

function Test-PythonCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PythonExe,
        [string[]]$PythonArgs = @()
    )

    # A falha de uma versao do Python e esperada durante a descoberta e nao
    # deve interromper o fallback para os demais interpretes instalados.
    $previousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $PythonExe @PythonArgs --version *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }
}

function Get-ProjectPython {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        if (Test-PythonCommand -PythonExe $pyLauncher.Source -PythonArgs @("-3.14")) {
            return @($pyLauncher.Source, "-3.14")
        }
    }

    $candidatePaths = @()
    if ($env:LOCALAPPDATA) {
        $candidatePaths += Join-Path $env:LOCALAPPDATA "Programs\Python\Python314\python.exe"
        $candidatePaths += Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"
        $candidatePaths += Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
    }
    if ($env:ProgramFiles) {
        $candidatePaths += Join-Path $env:ProgramFiles "Python314\python.exe"
        $candidatePaths += Join-Path $env:ProgramFiles "Python313\python.exe"
        $candidatePaths += Join-Path $env:ProgramFiles "Python312\python.exe"
    }

    foreach ($candidate in $candidatePaths) {
        if ((Test-Path $candidate) -and (Test-PythonCommand -PythonExe $candidate)) {
            return @($candidate)
        }
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand -and $pythonCommand.Source -notlike "*WindowsApps*") {
        if (Test-PythonCommand -PythonExe $pythonCommand.Source) {
            return @($pythonCommand.Source)
        }
    }

    throw "Python compativel nao encontrado. Instale o Python 3.12 ou superior e tente novamente."
}

function Invoke-ProjectPython {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$PythonArgs
    )

    $commandParts = @(Get-ProjectPython)
    $pythonExe = $commandParts[0]
    $resolvedArgs = @()
    if ($commandParts.Count -gt 1) {
        $resolvedArgs += $commandParts[1..($commandParts.Count - 1)]
    }
    $resolvedArgs += $PythonArgs
    & $pythonExe @resolvedArgs
}

Write-Host "Validando dependencias..." -ForegroundColor Cyan
Invoke-ProjectPython -m pip check

Write-Host "Validando configuracao Django..." -ForegroundColor Cyan
Invoke-ProjectPython manage.py check --settings=juventude_mst.settings.test

Write-Host "Verificando migracoes pendentes..." -ForegroundColor Cyan
Invoke-ProjectPython manage.py makemigrations --check --dry-run --settings=juventude_mst.settings.test

Write-Host "Rodando testes..." -ForegroundColor Cyan
Invoke-ProjectPython manage.py test --settings=juventude_mst.settings.test

Write-Host "Validacao concluida." -ForegroundColor Green
