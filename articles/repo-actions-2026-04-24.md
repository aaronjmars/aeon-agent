# Repo Action Ideas — 2026-04-24

**Repos analyzed:** aaronjmars/aeon (229 stars, 35 forks, 0 open issues), aaronjmars/aeon-agent
**Context:** Viral-moment day — @tom_doerr tweeted "autonomous agent framework with 90+ skills" and Aeon picked up 11 stars in a single day (229 total, up from 208 on Apr-22). Public status page shipped this morning (PR #141). Fork-skill-digest + onboard merged yesterday/prior day. Pipeline from Apr-22: Skill Run Analytics Widget remains the highest-priority unbuilt; Contributor Auto-Reward has all its dependencies met now. $AEON token: +441% 30d, $311.8K FDV, tweet-allocator distributing $10/day. Zero open PRs.

---

### 1. Skill Run Analytics Widget
**Type:** DX / Performance
**Effort:** Small (hours)
**Impact:** heartbeat gives binary ok/not-ok per skill. skill-health audits one skill at a time. There is no fleet-level performance view — no way to see which skills run most often, which have the highest failure rate, which haven't run in their expected window, or which are consuming the most tokens. This closes the observability gap and surfaces anomalies before they escalate to issues. The 80 autoresearch-evolution rewrites introduced new exit taxonomies (`SKIP_UNCHANGED`, `NEW_INFO`, `SKIP_QUIET`) that existing health checks may not parse correctly — the analytics widget would make that visible. Significance-gated so it only notifies when ≥1 anomaly is flagged (following the autoresearch-evolution pattern).
**How:**
1. New `skills/skill-analytics/SKILL.md` — runs `./scripts/skill-runs --json --hours 168` (7-day window), parses per-skill run counts, pass rates, failure patterns, and last exit status.
2. Produce a ranked table sorted by run-count desc with columns: skill name, 7d runs, success rate, last status, anomaly flag (red when: success rate <80%, or zero runs within expected cron window, or consecutive failures >2). Output to `articles/skill-analytics-YYYY-MM-DD.md` and a JSON spec to `dashboard/outputs/skill-analytics.json` for the json-render dashboard.
3. Register in `aeon.yml` on Wednesday cron (alongside memory-flush); send a summary notification via `./notify` only when at least one anomaly flag is raised. Silent run = correct = no noise.

---

### 2. Contributor Auto-Reward
**Type:** Community
**Effort:** Medium (1–2 days)
**Impact:** fork-contributor-leaderboard (shipped Apr-20) already scores contributors — merged upstream PRs (+10), open PRs (+3), fork commits (+1 cap 30), new skill authorship (+5 cap 5). tweet-allocator already has the full payment pipeline: wallet address lookup → queue `.pending-notify/` JSON → postprocess sends $AEON via Bankr. The gap is: no system closes the loop from leaderboard score to actual token transfer. With a growing fork community (35 forks, +21 stars this week alone) and an active tweet program paying out daily, adding automatic leaderboard rewards makes the community flywheel self-reinforcing — contributors get concrete economic signal that their work is valued.
**How:**
1. New `skills/contributor-reward/SKILL.md` — reads `memory/topics/fork-contributor-leaderboard.md` (or the leaderboard's output artifact), checks `.contributor-reward-state.json` for already-distributed rewards (idempotency), filters contributors above a configurable threshold score.
2. For each eligible contributor with a Bankr-linked wallet (from the leaderboard's existing wallet-lookup step), write a reward payload to `.pending-notify/contributor-reward-{handle}-{week}.json` using the same schema the tweet-allocator uses. The existing `scripts/postprocess-notify.sh` handles the actual send — no new infrastructure needed.
3. Register in `aeon.yml` on Monday cron (runs day after Sunday's leaderboard tallies scores); notify a summary via `./notify` listing who was rewarded and the amounts; write the distribution to `memory/logs/` and `memory/topics/contributor-reward-history.md`.

---

### 3. Twitter Thread Auto-Formatter
**Type:** Content
**Effort:** Small (hours)
**Impact:** tweet-allocator pays $10/day in $AEON to community members who tweet about the project. But the content those tweets echo is whatever individuals happen to notice — no curated signal, no narrative arc. The push-recap and repo-article skills produce long markdown output but nothing formatted for immediate Twitter use. A thread formatter reads today's biggest single event (from the log), generates a 5-7 tweet thread with a hook, 3-4 body tweets each under 280 chars, and a CTA pointing to the repo. Operators copy-paste and post; the tweet-allocator rewards anyone who amplifies. The @tom_doerr moment shows that a single good tweet can generate 11 organic stars in a day — structured content increases the rate of those moments.
**How:**
1. New `skills/tweet-thread/SKILL.md` — reads `memory/logs/${today}.md` for the highest-signal event (feature ship > repo milestone > token move); generates a structured thread: tweet 1 is the hook (what shipped), tweets 2-4 are the key details with a concrete example each, tweet 5 is a CTA (`fork us / star us / try it`).
2. Write to `articles/thread-${today}.md` with each tweet on its own numbered line (easy copy-paste); include character counts so operators can see at a glance what fits.
3. Send via `./notify` with a "Ready to post:" header — Telegram renders it as a previewable block. Register in `aeon.yml` triggered by the push-recap chain (runs after push-recap so it always has today's events); include a significance gate: only generate when a feature was shipped or a milestone crossed.

---

### 4. Repo Discovery Refresh
**Type:** Growth
**Effort:** Small (hours)
**Impact:** @tom_doerr's tweet brought 11 new stars in a day. Those stars clicked through to the repo and the first things they'd look for are: what does this thing actually do in concrete terms, how does it compare to what I already know (AutoGen, CrewAI, n8n, LangGraph), and where do I start. The current README covers setup well but has three gaps: no side-by-side comparison with alternatives, no "most impressive output" showcase, and only 3 GitHub topics (aeon, ai-agents, claude-code) vs the richer vocabulary that surfaces in discovery search. A one-shot refresh skill addresses all three with no ongoing maintenance cost.
**How:**
1. New `skills/repo-discovery-refresh/SKILL.md` — adds 5 additional GitHub topics via `gh api repos/aaronjmars/aeon/topics` PATCH: `claude`, `github-actions`, `autonomous-agent`, `llm-agents`, `autonomous-agents`. Generates `SHOWCASE.md` with the top 5 skills illustrated by actual recent output (pulled from `articles/` log entries); each entry has a one-sentence "what it does" and a 3-line output sample.
2. Appends a "Why Aeon?" comparison table to `README.md` under the existing skills table: columns are Aeon / AutoGen / CrewAI / n8n / LangGraph; rows are: runs on GitHub Actions (no server), self-heals skill failures, writes to memory, notifies via Telegram/Discord/Slack, forks inherit full config.
3. Run as workflow_dispatch (one-shot); log result to `memory/logs/`; the `./onboard` skill can reference the comparison table link in its output for new fork operators.

---

### 5. $AEON Token Pulse on Public Status Page
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** The public status page (shipped today as PR #141) shows skill health but nothing that gives community members context about the project's broader trajectory. Token price, volume, and 24h change are already fetched every run by `token-report`; the data sits in `articles/token-report-${today}.md`. A two-line extension to heartbeat's status page generation reads the latest token-report file and prepends a compact token pulse row to `docs/status.md` — price, 24h%, FDV, 24h volume. For fork operators who haven't enabled token-report, this row is silently omitted. The combined skill-health + token-health view turns the status page into a dual-use signal: operators check skill fleet health, community members check if the agent is running and what the token is doing, in one URL.
**How:**
1. Modify `skills/heartbeat/SKILL.md` — in the status page generation step, add a "Token" section: read `articles/token-report-${today}.md` if it exists, extract price / 24h% / FDV / volume via regex, render as a single-row table with a "AEON / Base" header and an "Updated" timestamp.
2. Graceful degradation: if today's token-report file doesn't exist (token-report not enabled, or hasn't run yet today), omit the token section entirely without error.
3. The status page URL (`https://aaronjmars.github.io/aeon/status/`) now serves as a linkable real-time state snapshot — usable in README badges, Twitter bios, and notification footers. Update the README Status badge tooltip to reflect that price is included.
