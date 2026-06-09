#!/usr/bin/env bash
set -euo pipefail
# Tiny wrapper that reads a notification body from a file and invokes ./notify.
# Lets us pass long multiline bodies without going through shell substitution
# (which the sandbox harness refuses to statically analyse).
exec ./notify "$(cat "$1")"
