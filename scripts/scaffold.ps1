# Creates the .NET solution and projects. Run once from the repo root.
$ErrorActionPreference = "Stop"

dotnet new sln -n Vouch

dotnet new classlib -n Vouch.Core           -o src/Vouch.Core
dotnet new classlib -n Vouch.Infrastructure -o src/Vouch.Infrastructure
dotnet new webapi   -n Vouch.Api            -o src/Vouch.Api
dotnet new worker   -n Vouch.Worker         -o src/Vouch.Worker
dotnet new xunit    -n Vouch.Tests          -o tests/Vouch.Tests

dotnet sln add src/Vouch.Core src/Vouch.Infrastructure src/Vouch.Api src/Vouch.Worker tests/Vouch.Tests

dotnet add src/Vouch.Infrastructure reference src/Vouch.Core
dotnet add src/Vouch.Api            reference src/Vouch.Core src/Vouch.Infrastructure
dotnet add src/Vouch.Worker         reference src/Vouch.Core src/Vouch.Infrastructure
dotnet add tests/Vouch.Tests        reference src/Vouch.Core src/Vouch.Infrastructure

Remove-Item -ErrorAction SilentlyContinue src/Vouch.Core/Class1.cs, src/Vouch.Infrastructure/Class1.cs

Write-Host "Done. Next: dotnet build"
