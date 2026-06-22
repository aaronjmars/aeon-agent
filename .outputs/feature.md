*Feature Built — 2026-06-22 — aaronjmars/aeon-agent*

skill-runs now validates --hours instead of dying on a cryptic date error.

The skill-runs audit script took --hours and fed it straight into date math with no checks. Pass it something that isn't a positive integer — "abc", "-5" — and it blew up deep in the GNU/BSD date branch under set -euo pipefail, with an error that pointed nowhere near the actual mistake. Now it checks the value right after parsing and fails with a clear message.

Why this matters:
skill-runs is the audit backbone — heartbeat, skill-health, and cost-report all lean on it. A bad arg producing an opaque date error is exactly the kind of failure that wastes a debugging cycle. Five lines turn it into an obvious "Invalid --hours" message.

What was built:
- scripts/skill-runs: a positive-integer regex guard right after arg parsing; on a bad value it prints "Invalid --hours: '<value>' (expected a positive integer)" to stderr and exits 1, matching the existing "Unknown arg" style

How it works:
A single [[ =~ ^[1-9][0-9]*$ ]] test before any date arithmetic runs. It rejects non-numeric, negative, and zero-hour inputs and short-circuits with a clear exit before the GNU/BSD date branch can fail confusingly. No behavior change for valid input.

What's next:
Same validation pattern could extend to any future numeric flags on the audit scripts, but --hours is the only one today.

PR: https://github.com/aaronjmars/aeon-agent/pull/112
