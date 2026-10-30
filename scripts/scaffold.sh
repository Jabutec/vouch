#!/usr/bin/env bash
# Creates the .NET solution and projects, one stage at a time.
# Usage: ./scripts/scaffold.sh [stage]   (stage: 1, 2, 3 or 5; default 1)
# Safe to re-run: existing projects are left alone.
set -euo pipefail
STAGE="${1:-1}"

if [ ! -f Vouch.sln ] && [ ! -f Vouch.slnx ]; then
  dotnet new sln -n Vouch >/dev/null
fi

# new_proj <template> <name> <path>; returns 0 when created, 1 when it already existed
new_proj() {
  if [ -d "$3" ]; then return 1; fi
  dotnet new "$1" -n "$2" -o "$3" >/dev/null
  dotnet sln add "$3" >/dev/null
  return 0
}

if [ "$STAGE" -ge 1 ]; then
  if new_proj classlib Vouch.Core src/Vouch.Core; then rm -f src/Vouch.Core/Class1.cs; fi
  if new_proj xunit Vouch.Tests tests/Vouch.Tests; then
    dotnet add tests/Vouch.Tests reference src/Vouch.Core >/dev/null
  fi
fi

if [ "$STAGE" -ge 2 ]; then
  if new_proj webapi Vouch.Api src/Vouch.Api; then
    dotnet add src/Vouch.Api reference src/Vouch.Core >/dev/null
  fi
fi

if [ "$STAGE" -ge 3 ]; then
  if new_proj classlib Vouch.Infrastructure src/Vouch.Infrastructure; then
    rm -f src/Vouch.Infrastructure/Class1.cs
    dotnet add src/Vouch.Infrastructure reference src/Vouch.Core >/dev/null
    dotnet add src/Vouch.Api reference src/Vouch.Infrastructure >/dev/null
    dotnet add tests/Vouch.Tests reference src/Vouch.Infrastructure >/dev/null
  fi
fi

if [ "$STAGE" -ge 5 ]; then
  if new_proj worker Vouch.Worker src/Vouch.Worker; then
    dotnet add src/Vouch.Worker reference src/Vouch.Core src/Vouch.Infrastructure >/dev/null
  fi
fi

echo "Stage $STAGE scaffold done. Next: dotnet build && dotnet test"
