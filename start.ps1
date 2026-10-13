param(
    [ValidateSet('menu', 'local', 'lan', 'migrate', 'bootstrap', 'test', 'check', 'backup', 'restore', 'validate', 'help')]
    [string]$Action = 'menu',
    [int]$Port = 8000,
    [string]$BackupDir = ''
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

function Get-ProjectPython {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        & $pyLauncher.Source -3.14 --version *> $null
        if ($LASTEXITCODE -eq 0) {
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
        if (Test-Path -LiteralPath $candidate) {
            & $candidate --version *> $null
            if ($LASTEXITCODE -eq 0) {
                return @($candidate)
            }
        }
    }

    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand -and $pythonCommand.Source -notlike "*WindowsApps*") {
        & $pythonCommand.Source --version *> $null
        if ($LASTEXITCODE -eq 0) {
            return @($pythonCommand.Source)
        }
    }

    throw "Python 3.14 nao encontrado. Instale o Python 3.14 ou o Python Launcher (py) e tente novamente."
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

function Set-LocalEnvironment {
    $env:RAIZ_DEBUG = "True"
    $env:DJANGO_SETTINGS_MODULE = "juventude_mst.settings.local"
    $env:RAIZ_SECURE_SSL_REDIRECT = "False"
    $env:RAIZ_ENABLE_REALTIME = "False"
    $env:RAIZ_CACHE_BACKEND = "django.core.cache.backends.locmem.LocMemCache"
    $env:RAIZ_CACHE_LOCATION = ""
    if (-not $env:RAIZ_ALLOWED_HOSTS) {
        $env:RAIZ_ALLOWED_HOSTS = "127.0.0.1,localhost,testserver"
    }
}

function Invoke-ProjectScript {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptName,
        [string[]]$ScriptArgs = @()
    )

    $scriptPath = Join-Path $ProjectRoot $ScriptName
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw "Script nao encontrado: $scriptPath"
    }
    & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath @ScriptArgs
}

function Run-Local {
    Set-LocalEnvironment
    Write-Host "Iniciando em http://127.0.0.1:$Port/" -ForegroundColor Green
    Invoke-ProjectPython manage.py runserver "127.0.0.1:$Port"
}

function Run-Lan {
    Invoke-ProjectScript "start_lan.ps1" @("-Port", "$Port")
}

function Run-Migrations {
    Set-LocalEnvironment
    Invoke-ProjectPython manage.py migrate
}

function Run-Bootstrap {
    Set-LocalEnvironment
    Invoke-ProjectPython manage.py bootstrap_juventude_mst
}

function Run-Tests {
    Invoke-ProjectPython manage.py test --settings=juventude_mst.settings.test
}

function Run-Check {
    Invoke-ProjectPython manage.py check --settings=juventude_mst.settings.local
}

function Run-Backup {
    Invoke-ProjectScript "backup.ps1"
}

function Run-Restore {
    $targetBackupDir = $BackupDir
    if (-not $targetBackupDir) {
        $targetBackupDir = Read-Host "Informe a pasta do backup"
    }
    Invoke-ProjectScript "restore.ps1" @("-BackupDir", $targetBackupDir)
}

function Run-Validate {
    Invoke-ProjectScript "validate.ps1"
}

function Show-Help {
    Write-Host "Rede Raizes Socialista - start.ps1" -ForegroundColor Green
    Write-Host ""
    Write-Host "Uso:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\start.ps1"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action local -Port 8000"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action lan -Port 8000"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action check"
    Write-Host ""
    Write-Host "Acoes:"
    Write-Host "  menu       abre o menu interativo"
    Write-Host "  local      inicia em 127.0.0.1"
    Write-Host "  lan        compartilha na rede local"
    Write-Host "  migrate    aplica migrations"
    Write-Host "  bootstrap  recria dados demo"
    Write-Host "  test       roda testes"
    Write-Host "  check      roda check do Django"
    Write-Host "  backup     cria backup local"
    Write-Host "  restore    restaura backup local"
    Write-Host "  validate   valida dependencias, check e testes"
}

function Invoke-Action {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SelectedAction
    )

    switch ($SelectedAction) {
        'local' { Run-Local; return }
        'lan' { Run-Lan; return }
        'migrate' { Run-Migrations; return }
        'bootstrap' { Run-Bootstrap; return }
        'test' { Run-Tests; return }
        'check' { Run-Check; return }
        'backup' { Run-Backup; return }
        'restore' { Run-Restore; return }
        'validate' { Run-Validate; return }
        'help' { Show-Help; return }
        default { throw "Acao desconhecida: $SelectedAction" }
    }
}

function Show-Menu {
    Clear-Host
    Write-Host "Rede Raizes Socialista - menu de operacao" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pasta do projeto: $ProjectRoot"
    Write-Host "Porta atual: $Port"
    Write-Host ""
    Write-Host "1. Iniciar local em http://127.0.0.1:$Port/"
    Write-Host "2. Compartilhar na rede local"
    Write-Host "3. Aplicar migrations"
    Write-Host "4. Recriar dados demo"
    Write-Host "5. Rodar testes"
    Write-Host "6. Rodar check do Django"
    Write-Host "7. Criar backup local"
    Write-Host "8. Restaurar backup local"
    Write-Host "9. Validar projeto completo"
    Write-Host "H. Ajuda"
    Write-Host "0. Sair"
    Write-Host ""
}

function Run-Menu {
    do {
        Show-Menu
        $choice = Read-Host "Escolha uma opcao"
        switch ($choice) {
            '1' { Run-Local; break }
            '2' { Run-Lan; break }
            '3' { Run-Migrations; Pause }
            '4' { Run-Bootstrap; Pause }
            '5' { Run-Tests; Pause }
            '6' { Run-Check; Pause }
            '7' { Run-Backup; Pause }
            '8' { Run-Restore; Pause }
            '9' { Run-Validate; Pause }
            'H' { Show-Help; Pause }
            'h' { Show-Help; Pause }
            '0' { return }
            default {
                Write-Host "Opcao invalida." -ForegroundColor Yellow
                Pause
            }
        }
    } while ($true)
}

if ($Action -eq 'menu') {
    Run-Menu
} else {
    Invoke-Action $Action
}
