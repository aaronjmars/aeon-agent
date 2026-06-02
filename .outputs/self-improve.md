*Agent Self-Improvement — 2026-06-02*

Patched `skills/repo-pulse/SKILL.md` step 2 — `CUTOFF=$(date -u -d '24 hours ago' ...)` → literal `CUTOFF=YYYY-MM-DDT00:00:00Z` computed from `${today}` minus 1 day. Daily 10:00 UTC repo-state digest now stops improvising the cutoff on every run.

Why: continues the runner-shell-guard fix class — PR #63 weekly-shiplog (May 26), PR #67 push-recap (May 28), PR #71 heartbeat (May 30 self-improve). The May-30 run explicitly listed `repo-pulse:27` among four other affected skills "left for future runs"; picked as smallest-effort next item — single-line direct substitution, no surrounding logic touched.

What changed:
- `skills/repo-pulse/SKILL.md` step 2 (+6/-3): swap `$(date ...)` for literal `YYYY-MM-DDT00:00:00Z`; rewrite paragraph to cite PRs #63/#67/#71 inline so a future cleanup doesn't drop the constraint; note the rolling-24h → midnight-of-yesterday semantic shift (10-34h window on a 10:00 UTC run) and that the step 5b same-day dedup absorbs the overlap. Mirrors push-recap PR #67's accepted trade verbatim.

Impact: zero shell-substitution improvisation on daily repo-pulse runs starting tomorrow. Three skills with the same anti-pattern still pending — repo-article:26 (7d window, daily), repo-actions:29 (14d window, even days), star-momentum-alert:69 (3 expansion sites in one loop — bigger fix).

PR: https://github.com/aaronjmars/aeon-agent/pull/77
