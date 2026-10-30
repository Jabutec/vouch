# Creates the .NET solution and projects, one stage at a time.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\scaffold.ps1 [-Stage 1|2|3|5]
# Safe to re-run: existing projects are left alone.
param([int]$Stage = 1)
$ErrorActionPreference = "Stop"

if (-not (Test-Path "Vouch.sln") -and -not (Test-Path "Vouch.slnx")) {
    dotnet new sln -n Vouch | Out-Null
}

# Creates a project if missing. Returns $true when it was created.
function New-Proj($template, $name, $path) {
    if (Test-Path $path) { return $false }
    dotnet new $template -n $name -o $path | Out-Null
    dotnet sln add $path | Out-Null
    return $true
}

if ($Stage -ge 1) {
    if (New-Proj classlib Vouch.Core src/Vouch.Core) {
        Remove-Item src/Vouch.Core/Class1.cs -ErrorAction SilentlyContinue
    }
    if (New-Proj xunit Vouch.Tests tests/Vouch.Tests) {
        dotnet add tests/Vouch.Tests reference src/Vouch.Core | Out-Null
    }
}

if ($Stage -ge 2) {
    if (New-Proj webapi Vouch.Api src/Vouch.Api) {
        dotnet add src/Vouch.Api reference src/Vouch.Core | Out-Null
    }
}

if ($Stage -ge 3) {
    if (New-Proj classlib Vouch.Infrastructure src/Vouch.Infrastructure) {
        Remove-Item src/Vouch.Infrastructure/Class1.cs -ErrorAction SilentlyContinue
        dotnet add src/Vouch.Infrastructure reference src/Vouch.Core | Out-Null
        dotnet add src/Vouch.Api reference src/Vouch.Infrastructure | Out-Null
        dotnet add tests/Vouch.Tests reference src/Vouch.Infrastructure | Out-Null
    }
}

if ($Stage -ge 5) {
    if (New-Proj worker Vouch.Worker src/Vouch.Worker) {
        dotnet add src/Vouch.Worker reference src/Vouch.Core src/Vouch.Infrastructure | Out-Null
    }
}

Write-Host "Stage $Stage scaffold done. Next: dotnet build; dotnet test"
