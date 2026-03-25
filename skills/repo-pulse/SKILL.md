---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos
var: ""
---
> **${var}** — Repo (owner/repo) to check. If empty, checks all watched repos.

## Config

This skill reads repos from `memory/watched-repos.md`.

---

Read memory/MEMORY.md and the last 7 days of memory/logs/ for previous star/fork counts to calculate deltas.
Read memory/watched-repos.md for the list of repos to track.

## Steps

1. **Fetch repo stats** for each watched repo:
   ```bash
   # Current stars, forks, watchers, open issues
   gh api repos/owner/repo --jq '{stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count}'
   ```

2. **Fetch recent stargazers** (who starred recently):
   ```bash
   # Last 10 stargazers with timestamps
   gh api repos/owner/repo/stargazers -H "Accept: application/vnd.github.star+json" --jq '.[-10:] | .[] | {user: .user.login, starred_at: .starred_at}'
   ```

3. **Fetch recent forks**:
   ```bash
   # Forks created in the last 24h
   gh api repos/owner/repo/forks --jq '[.[] | {owner: .owner.login, created_at: .created_at, full_name: .full_name}] | .[0:10]'
   ```

4. **Fetch traffic data** (requires push access to the repo):
   ```bash
   # Views in the last 14 days
   gh api repos/owner/repo/traffic/views --jq '{count, uniques, views: [.views[-3:][].timestamp]}'

   # Clones in the last 14 days
   gh api repos/owner/repo/traffic/clones --jq '{count, uniques}'

   # Top referrers
   gh api repos/owner/repo/traffic/popular/referrers --jq '.[0:5]'
   ```
   If traffic endpoints return 403 (insufficient permissions), skip traffic data and note it in the report.

5. **Calculate deltas** by comparing against the last logged values in `memory/logs/`. If no previous data exists, this is the first run — report current totals only.

6. **If no new stars AND no new forks** since the last run: log "REPO_PULSE_QUIET" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

7. **Send notification** via `./notify`:
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X (+N new)
   Forks: Y (+N new)
   Watchers: Z

   New stargazers:
   - x.com/user1 (or github.com/user1 if no X linked)
   - x.com/user2
   - x.com/user3

   New forks:
   - github.com/user/fork-name

   Traffic (14d): X views (Y unique) | Z clones
   Top referrers: google.com, github.com, twitter.com
   ```

   If there are many new stars (5+), lead with an excited tone. If it's just 1-2, keep it factual.

8. **Log** to `memory/logs/${today}.md` — include the current star and fork counts so the next run can calculate deltas.
