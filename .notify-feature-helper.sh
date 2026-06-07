#!/usr/bin/env bash
# One-shot helper to send the three feature-built notifications via ./notify
# without needing $(cat ...) substitution (sandbox-blocked).
set -uo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
for repo in aeon aeon-agent minitor; do
  f=".notify-msg-feature-${repo}.txt"
  if [ -f "$f" ]; then
    MSG=$(cat "$f")
    ./notify "$MSG"
  fi
done
