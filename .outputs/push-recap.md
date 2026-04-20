*Push Recap — 2026-04-20*
aeon: 5 PRs merged · aeon-agent: 4 mirror commits · ~+795/-56 lines · all @aaronjmars

Features shipped: PR #41 Memory Search API (read-only REST at /api/memory/* exposing MEMORY.md, topics, logs, issues as JSON — path-safe reader + token-scored search, +480 lines across 8 new files) and PR #42 fork-contributor-leaderboard (weekly Sunday skill ranking community devs across the 30+ fork fleet by merged/open PRs, commits, new skills, stars — bots filtered, opt-out supported, first run 2026-04-26). Both were yesterday's open branches; now on main.

Notification stack hardening (3 PRs): PR #45 chunks long Telegram messages at paragraph/line boundaries with [i/N] suffix instead of slicing them at byte 3990 — feature + weekly-shiplog were losing PR links mid-paragraph. PR #44 migrates three skill notifications from ambiguous "OWNER/REPO" literals to $GITHUB_REPOSITORY so article links are clickable and point at the running repo, not the watched one.

fetch-tweets reliability (PR #43): two real bugs, two silent-failure days. (1) scripts/prefetch-xai.sh had curl --max-time 60 on Grok x_search calls that routinely take 60-120s — every run timed out, cache never written, skill fell through to dead-end WebSearch. Bumped to 180s + one retry on exit 28. (2) The pre-fetch workflow step inlined ${{ inputs.var }} into bash source, so cashtags like $AEON were expanded to empty before reaching the filter — 2/3 OR-patterns survived, most tweets dropped. Fix: route via a SKILL_VAR env var. Verified on miroshark-aeon: 0/5 → 11/11 kept, 12:32 UTC aeon-agent run posted 12 tweets.

Key changes:
- Memory Search API adds 8 routes + 480 lines of additive surface — Aeon's markdown state is now queryable without scraping raw files (PR #41)
- Telegram chunker: base64-piped, HTML-converted per-chunk, 0.3s ordered delay — no more mid-paragraph truncation (PR #45)
- fetch-tweets comes back online after 48h of silent FETCH_TWEETS_EMPTY days — 180s timeout + SKILL_VAR env restore 12-tweet yield (PR #43)

Stats: 13 files changed, +795/-56 lines (excluding 44 cron chore auto-commits on aeon-agent)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-20.md
