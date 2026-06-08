---
name: repo-pulse
description: Daily report on new stars, forks, and traffic for watched repos — enriched with each new starrer/forker's profile (name, company, bio, location, followers)
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

2. **Compute the cutoff timestamp** FIRST — this is critical.

   The runner hook blocks shell command/variable expansion (`$(...)`, `$VAR`) — do **not** use `$(date ...)` for the cutoff. Instead, pass `CUTOFF` as a literal ISO timestamp that you compute from `${today}` minus 1 day (e.g. if today is `2026-06-02`, write `CUTOFF=2026-06-01T00:00:00Z`). This matches the pattern weekly-shiplog (PR #63), push-recap (PR #67), and heartbeat (PR #71) use for the same reason.
   ```bash
   # Cutoff = midnight UTC of yesterday, computed from ${today} (literal — not $(date ...))
   CUTOFF=YYYY-MM-DDT00:00:00Z
   ```
   Use this `$CUTOFF` for ALL time filtering below. The window is slightly wider than 24h (10–34h on a 10:00 UTC run, depending on time-of-run), but the same-day dedup in step 5b absorbs the overlap.

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

5c. **Enrich new stargazers and forkers (profile lookup).** Before formatting the notification, look up *who* each new account is — a bare handle (`github.com/xyz123`) tells the operator nothing; `@ Vercel · 2.3k followers` tells them a launch is landing. For each new stargazer handle and each new fork owner you are about to report (the first-run 24h set, or the subsequent-run delta set), make one read-only call:

   ```bash
   gh api users/$LOGIN --jq '{login, name, company, bio, location, blog, twitter_username, followers, public_repos, hireable, created_at}'
   ```

   Rules:
   - **Cap at 25 new accounts per run** (stargazers + forkers combined). If there are more, enrich the first 25 in `starred_at` / `created_at` order and append a final `…and N more` line un-enriched. Bounds both API calls and message length.
   - **Skip empty fields** — most accounts have `null` company/bio/location. Omit a segment rather than printing a blank.
   - **One-line summary per account**, joining the present fields with ` · ` in this order:
     `${name or login} · @ ${company} · ${location} · ${followers}f · ${public_repos} repos · "${bio trimmed to ~80 chars}"`
     Drop any segment whose source field is empty (e.g. no company → no `@ …` segment). Use `${twitter_username}` / `${blog}` only in the article/log, not the notification, to keep messages short.
   - **Low-signal flag** — if `followers <= 2` AND `public_repos == 0` AND `created_at` is within the last 30 days, append ` ⚠ new/low-signal`. A soft fake-star tell that complements `star-milestone`'s burst check; annotate, don't suppress.
   - **Sandbox note** — `gh api users/$LOGIN` is read-only and the `gh` CLI handles auth internally (no curl, no env-var headers), so it works in the Actions sandbox. If a lookup fails (deleted/renamed account), fall back to the bare handle for that entry and continue.

6. **Send notification** via `./notify`:

   **First-run format** (full 24h view):
   ```
   *Repo Pulse — ${today}*
   [owner/repo]

   Stars: X total (+N new)
   Forks: Y total (+N new)

   New stargazers:
   - github.com/alice — Alice Chen · @ Vercel · San Francisco · 2.3k followers · 87 repos · "building dev tools"
   - github.com/bob — @ Stripe · 480 followers
   - github.com/carol — 4 followers · joined 6d ago ⚠ new/low-signal

   New forks:
   - github.com/dave/repo — Dave Kim · @ Acme · 1.1k followers
   ```

   **Subsequent-run format** (delta only, when `delta_stars` or `delta_forks` is non-empty):
   ```
   *Repo Pulse — ${today} (since last run)*
   [owner/repo]

   Stars: X total (+N since last run)
   Forks: Y total (+N since last run)

   New stargazers (since last run):
   - github.com/alice — Alice Chen · @ Vercel · 2.3k followers
   - github.com/bob — @ Stripe · 480 followers

   New forks (since last run):
   - github.com/dave/repo — Dave Kim · @ Acme · 1.1k followers
   ```

   Format rules:
   - **One enriched line per stargazer/forker** (from step 5c): `- github.com/${handle} — ${summary}`. The `github.com/${handle}` prefix MUST stay first so the handle is still parseable; the profile summary follows after ` — `.
   - If step 5c produced no summary for an account (all fields empty or lookup failed), fall back to the bare `- github.com/${handle}` line.
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

   **New account profiles (24h):**
   - github.com/alice (star) — Alice Chen · @ Vercel · San Francisco · 2.3k followers · 87 repos · twitter.com/alice · "building dev tools"
   - github.com/dave (fork) — Dave Kim · @ Acme · 1.1k followers
   ```
   Keep the `**aaronjmars/repo**: stargazers_count=X, forks_count=Y` line and the bare-handle `New stars/forks (24h)` lines **exactly** as shown — `star-momentum-alert` and the same-day dedup parse them. The `**New account profiles (24h):**` block is additive enrichment (the fuller form from step 5c, including `twitter`/`blog`); tag each entry `(star)` or `(fork)`. Omit the block entirely if there are no new accounts.
