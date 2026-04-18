---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos
var: ""
tags: [dev]
---
> **${var}** — Repo (owner/repo) to check. If empty, checks all watched repos.

## Config

This skill reads repos from `memory/watched-repos.md` but **skips agent/monitoring repos** (repos that contain "aeon-agent" or "miroshark-aeon" in their name). Only track the actual project repos — not the agent repos that run the skills.

---

Read memory/MEMORY.md and the last 3 days of memory/logs/ for previous star/fork counts to calculate deltas.
Read memory/watched-repos.md for the list of repos to track. Skip any repo whose name ends with "-aeon" or contains "aeon-agent" — those are agent repos, not project repos.

## Steps

1. **Fetch repo stats** for each watched repo:
   ```bash
   gh api repos/owner/repo --jq '{stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count}'
   ```

2. **Compute the 24h cutoff timestamp** FIRST — this is critical:
   ```bash
   CUTOFF=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)
   ```
   Use this `$CUTOFF` for ALL time filtering below. Do NOT use "today's date" — use exactly 24 hours ago from now.

3. **Fetch the most recent stargazers** — use `--paginate` and filter by the 24h cutoff:
   ```bash
   gh api repos/owner/repo/stargazers -H "Accept: application/vnd.github.star+json" --paginate --jq '.[] | {user: .user.login, starred_at: .starred_at}' | tail -30
   ```
   From this list, keep only entries where `starred_at` >= `$CUTOFF` (24 hours ago). NOT "since midnight today" — since exactly 24 hours ago.

4. **Fetch recent forks** (sorted by newest):
   ```bash
   gh api "repos/owner/repo/forks?sort=newest&per_page=10" --jq '.[] | {owner: .owner.login, created_at: .created_at, full_name: .full_name}'
   ```
   Keep only forks where `created_at` >= `$CUTOFF`.

5. **Determine if there's activity to report.** Check BOTH:
   - **New stargazers from step 3**: any with `starred_at` >= the 24h cutoff
   - **New forks from step 4**: any with `created_at` >= the 24h cutoff

5b. **Same-day dedup — compute delta since last run today.** Repo-pulse may run multiple times per day; rolling 24h windows overlap heavily, so unfiltered re-notification is spam. Scan `memory/logs/${today}.md` for prior `## Repo Pulse` sections on the same repo. Parse out previously-reported stargazer handles (from "New stars (24h):" lines) and fork `full_name`s (from "New forks (24h):" lines). Compute the delta:
   - `delta_stars = today's 24h stargazers − previously-reported handles today`
   - `delta_forks = today's 24h forks − previously-reported full_names today`

   **Notification rule:**
   - **First run today** (no prior `## Repo Pulse` for this repo in today's log) → notify using the full 24h list (existing behavior).
   - **Subsequent run, delta is empty** → log `REPO_PULSE_QUIET — no new stars or forks since last run today` and skip notification.
   - **Subsequent run, delta has entries** → notify using `delta_stars` / `delta_forks` only (not the full 24h list), with a "Since last run" framing so the recipient knows these are incremental.

   Only log "REPO_PULSE_QUIET" and skip notification if the first-run 24h view is empty, OR a subsequent-run delta is empty.

6. **Send notification** via `./notify`:

   **First-run format** (full 24h view):
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X total (+N new)
   Forks: Y total (+N new)

   New stargazers:
   github.com/user1 | github.com/user2 | github.com/user3

   New forks:
   github.com/user1/repo | github.com/user2/repo
   ```

   **Subsequent-run format** (delta only, when `delta_stars` or `delta_forks` is non-empty):
   ```
   *Repo Pulse — ${today} (since last run)*
   [owner/repo]

   Stars: X total (+N since last run)
   Forks: Y total (+N since last run)

   New stargazers (since last run):
   github.com/user1 | github.com/user2

   New forks (since last run):
   github.com/user1/repo
   ```

   Format rules:
   - List stargazers on one line separated by ` | ` (not one per line)
   - Same for forks
   - Omit "New stargazers" section entirely if there are none
   - Omit "New forks" section entirely if there are none
   - Do NOT include traffic data, watchers, or open issues

7. **Log** to `memory/logs/${today}.md` — ALWAYS include the exact current counts AND the list of handles/forks so the next same-day run can compute its delta correctly:
   ```
   ## Repo Pulse
   - **aaronjmars/repo**: stargazers_count=X, forks_count=Y
   - **New stars (24h):** N (handle1, handle2, ...)
   - **New forks (24h):** N (owner1/repo, owner2/repo, ...)
   - **Notification sent:** yes/no (reason if no, e.g. "delta empty since last run today")
   ```
