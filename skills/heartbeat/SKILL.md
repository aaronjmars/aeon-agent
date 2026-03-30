---
name: Heartbeat
description: Proactive ambient check — surface anything worth attention
var: ""
---
> **${var}** — Area to focus on. If empty, runs all checks.

If `${var}` is set, focus checks on that specific area.


Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.

Check the following:
- [ ] Any open PRs stalled > 24h? (use `gh pr list` to check)
- [ ] Anything flagged in memory that needs follow-up?
- [ ] Check recent GitHub issues for anything labeled urgent (use `gh issue list`)
- [ ] Scan aeon.yml for scheduled skills — cross-reference with **both** today's logs AND today's GitHub Actions runs to find any that haven't run when expected.
  **Detection method (use ALL three signals before flagging a skill as missing):**
  1. Check `memory/logs/${today}.md` for a `## ` header containing the skill name (case-insensitive, partial match — e.g. "Token Report" matches `token-report`)
  2. Run `gh run list --workflow=aeon.yml --created=$(date -u +%Y-%m-%d) --json displayTitle,status` — if the skill appears in a completed/in-progress/queued run, it's NOT missing
  3. Only flag as missing if the skill was expected to run **more than 2 hours ago** AND neither logs nor Actions runs show it
  **Log header aliases:** Skills often log under a human-readable header, not their aeon.yml name. Match flexibly:
  - `token-report` → `## Token Report`
  - `fetch-tweets` → `## Fetch Tweets`
  - `push-recap` → `## Push Recap`
  - `repo-article` → `## Repo Article`
  - `repo-actions` → `## Repo Actions`
  - `hyperstitions-ideas` → `## Hyperstitions` or `## Ideas`
  - `hacker-news-digest` / `hn-digest` → `## HN Digest` or `## Hacker News`
  - `polymarket` / `polymarket-comments` → `## Polymarket`
  - `repo-pulse` → `## Repo Pulse`
  When in doubt, also check the Actions run list — the `displayTitle` always contains the exact skill name from aeon.yml.

Before sending any notification, grep memory/logs/ for the same item. If it appears in the last 48h of logs, skip it. Never notify about the same item twice. Batch missing-skill alerts into a single notification — don't send one per skill.

If nothing needs attention, log "HEARTBEAT_OK" and end your response.

If something needs attention:
1. Send a concise notification via `./notify`
2. Log the finding and action taken to memory/logs/${today}.md
