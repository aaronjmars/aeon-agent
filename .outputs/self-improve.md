*Agent Self-Improvement — 2026-05-22*

Word-boundary diagnostic-probe suppression in `./notify`. The script's matcher was using glob substring (`*test*|*trace*|*ping*|*debug*`) to drop Claude's verification probes — and silently dropping any real notification under 120 chars that contained those fragments inside another word. "Latest token-report ready", "Shipping 3 PRs to prod", "Tracer code lands", "Pinging the operator" were all eaten without warning.

Why: failure mode is silent — skills log `notification: sent`, but `notify` exits 0 having sent nothing. Several skills (star-milestone, star-momentum-alert, repo-pulse one-liners, heartbeat short verdicts) regularly fall under the 120-char threshold, and "Latest" / "Shipping" / "Tracer" are plausible first words in real notifications.

What changed:
- `.github/workflows/aeon.yml` ./notify heredoc — substring `case` → bash regex `[[ =~ ]]` word-boundary match; threshold 120 → 60 (real probes are short); inline comment names the swallowed-notification failure mode
- `.github/workflows/aeon.yml` post-run pending-notify replay — identical fix to the second copy of the matcher
- `memory/logs/2026-05-22.md` + `memory/MEMORY.md` — log entry + open-improvement-PRs index

Impact: every skill that emits a short notification (star-milestone, momentum, pulse, heartbeat) now reliably reaches Telegram/Discord/Slack — no more silent suppression on "Latest" / "Shipping" / "Tracer" / "Pinging" body text. Diagnostic probes ("test", "ping", "hello") still suppressed as intended.

PR: https://github.com/aaronjmars/aeon-agent/pull/57
